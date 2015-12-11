import sublime, sublime_plugin
import json
import re

class MvDoCompletions(sublime_plugin.EventListener):
	"""
	MvDO File / Function Attribute Completions
	| Smartly determine which "Functions" to autocomplete based on chosen "File"
	| <mvt:do file="g.Module_Library_DB" value="Product_Load_ID(), Category_Load_ID() ..." />
	"""
	def __init__(self):
		
		mvlsk_path = sublime.packages_path() + '/mvdo_completions/mv-lsk.json'
		self.mvlsk_data = self.read_mvlsk_json(mvlsk_path)


	def on_query_completions(self, view, prefix, locations):
		# Only trigger in an <mvt:do> Tag
		if not view.match_selector(locations[0], 'text.html.mvt meta.tag.inline.do.mvt'):
			return []

		# determine what <mvt:do> attribute you're in
		if (view.match_selector(locations[0], 'text.html.mvt meta.tag.inline.do.mvt source.mvt.embedded.html source.mvt.attribute-value.file')):
			mvdo_attribute = 'file'
		elif (view.match_selector(locations[0], 'text.html.mvt meta.tag.inline.do.mvt source.mvt.embedded.html source.mvt.attribute-value.value')):
			mvdo_attribute = 'value'
		else:
			return []
		
		return self.get_completions(view, prefix, locations, mvdo_attribute)


	def get_completions(self, view, prefix, locations, mvdo_attribute):
		completion_list = []

		if (mvdo_attribute == 'file'):
			completion_list = self.get_file_completions(view, locations[0], prefix)
		elif (mvdo_attribute == 'value'):
			attribute_file = self.get_current_file_attribute(view, locations[0], prefix)
			completion_list = self.get_value_completions(view, locations[0], prefix, attribute_file)

		return (completion_list, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)


	"""
	Custom Methods
	"""
	def read_mvlsk_json(self, path):
		with open( path ) as data_file:
			data = json.load(data_file)
		return data


	def get_file_completions(self, view, pt, prefix):
		file_completions = [ ( file['distro_path'] + '\tFile', file['distro_path'].replace('$', '\\$') ) for file in self.mvlsk_data ]
		return set(file_completions)

		
	def get_value_completions(self, view, pt, prefix, attribute_file):
		value_completions = []

		for file in self.mvlsk_data:
			if (attribute_file == file['distro_path']):
				for function in file['functions']:
					parameters = self.build_function_parameters(function['parameters'])
					value_completions.append( (function['name'] + '\tFunc', function['name'] + parameters) )

		return value_completions


	def get_current_file_attribute(self, view, pt, prefix):
		# limit the search left/right to 200 characters
		_LIMIT = 200

		# left side of the string
		left_start = pt
		left_end = max(0, left_start - _LIMIT)
		left_angle_pos = False
		i = left_start
		while i >= left_end:
			c = view.substr(i)
			if (c == '<'):
				left_angle_pos = i
				break
			i -= 1

		# right side of the string
		right_start = pt + len(prefix)
		right_end = right_start + _LIMIT
		right_angle_pos = False
		i = right_start
		while i <= right_end:
			c = view.substr(i)
			if (c == '>'):
				right_angle_pos = i
				break
			i += 1

		mvdo_tag_region = sublime.Region(left_angle_pos, right_angle_pos)
		attribute_file_all_locations = view.find_by_selector( 'text.html.mvt meta.tag.inline.do.mvt source.mvt.embedded.html source.mvt.attribute-value.file' )
		attribute_file = ''

		for attribute_file_location in attribute_file_all_locations:
			if (mvdo_tag_region.contains(attribute_file_location)):
				attribute_file = view.substr(attribute_file_location)

		return attribute_file.replace('"', '')


	def build_function_parameters(self, parameters):
		if (len(parameters) == 0):
			return ''

		parameters_map = []
		count = 0
		for parameter in parameters:
			count += 1
			if (count == len(parameters)):
				count = 0
			parameters_map.append( '${' + str(count) + ':' + parameter + '}' )

		sep = ', '
		return '( ' + sep.join(parameters_map) + ' )'


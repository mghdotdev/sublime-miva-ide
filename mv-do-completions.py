import sublime, sublime_plugin
import json
import re
import os
from os.path import dirname, realpath

# Define Path to JSON Cache
__FUNCTIONS_MERCHANT_PATH__ = dirname(realpath(__file__)) + os.sep + '/functions-merchant.json'

class MvDoCompletions(sublime_plugin.EventListener):
	"""
	MvDO File / Function Attribute Completions
	| Smartly determine which "Functions" to autocomplete based on chosen "File"
	| <mvt:do file="g.Module_Library_DB" value="Product_Load_ID(), Category_Load_ID() ..." />
	"""
	def __init__(self):
		self.functions_merchant_data = self.read_data_file(__FUNCTIONS_MERCHANT_PATH__)
		self.quick_panel_data = {}
		self.mode = '';

	def on_query_completions(self, view, prefix, locations):
		
		currentPoint = locations[0]
		previousPoint = max(0, locations[0] - 1)

		self.mode = ''

		# Only Trigger in a <MvDO> Tag or Function File Terminator
		if not view.match_selector( currentPoint, 'text.mv text.html.basic meta.tag.inline.do.mv' ) and not ( view.score_selector( previousPoint, 'puncuation.terminator.function-file-ending.mv' ) > 0 ) and not ( view.score_selector( previousPoint, 'function-file.mv' ) > 0 ):
			return []

		if view.match_selector( currentPoint, 'text.mv text.html.basic meta.tag.inline.do.mv attribute-content.file.mv string.quoted.double.mv text.mv source.mv.expr' ):
			self.mode = 'file'
		elif view.match_selector( currentPoint, 'text.mv text.html.basic meta.tag.inline.do.mv attribute-content.value.mv string.quoted.double.mv text.mv source.mv.expr' ):
			is_variable = view.match_selector( previousPoint, 'variable.language' )
			if ( is_variable ):
				return []
			self.mode = 'value'
		elif view.score_selector( previousPoint, 'puncuation.terminator.function-file-ending.mv' ) > 0:
			self.mode = 'terminator_value'
		elif view.score_selector( previousPoint, 'function-file.mv' ) > 0:
			self.mode = 'terminator_file'
		else:
			return []

		return self.get_completions( view, prefix, locations, self.mode )


	def on_post_text_command(self, view, command_name, *args):

		# print( 'mode is...', self.mode )

		if (command_name == 'commit_completion' or command_name == 'insert_best_completion'):

			for r in view.sel():

				in_value_attribute = view.match_selector(r.begin(), 'text.mv text.html.basic meta.tag.inline.do.mv attribute-content.value.mv string.quoted.double.mv text.mv source.mv.expr')
				
				if (in_value_attribute):
					prev_pt = max(0, r.begin() - 1)
					is_variable = view.match_selector(prev_pt, 'variable.language')
					if (is_variable is False):
						file_attribute_val = self.get_current_file_attribute_val(view, r.begin(), '')
						if (file_attribute_val == ''):
							value_attribute_val = self.get_current_value_attribute_val(view, r.begin(), '')
							function_name = self.get_function_name(view, value_attribute_val)
							if function_name is not False:
								file_name = self.get_file_name(view, function_name)
								if file_name is not False:
									if type(file_name) is list:
										self.quick_panel_data = { "view": view, "pt": r.begin(), "file_name": file_name }
										view.window().show_quick_panel(file_name, self.choose_file_name, sublime.MONOSPACE_FONT)
									elif type(file_name) is str:
										self.insert_file_name(view, r.begin(), file_name)


	def get_completions( self, view, prefix, locations, mode ):
		
		completion_list = []

		if (mode == 'file'):
			completion_list = self.get_file_completions( view, locations[0], prefix )

		elif (mode == 'value'):
			file_attribute_val = self.get_current_file_attribute_val( view, locations[0], prefix )
			completion_list = self.get_value_completions( view, locations[0], prefix, file_attribute_val )

		elif (mode == 'terminator_file'):
			completion_list = self.get_file_completions( view, locations[0], prefix )

		elif (mode == 'terminator_value'):
			terminator_file_val = '';
			completion_list = self.get_value_completions( view, locations[0], prefix, terminator_file_val )

		return ( completion_list, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS )

	"""
	Custom Methods
	"""
	def read_data_file( self, path ):
		with open( path ) as data_file:
			data = json.load( data_file )
		return data
		

	def get_file_completions(self, view, pt, prefix):
		file_completions = [ ( file['distro_path'] + '\tFile', file['distro_path'].replace('$', '\\$') ) for file in self.functions_merchant_data ]
		return set(file_completions)


	def get_value_completions(self, view, pt, prefix, file_attribute_val):
		value_completions = []

		for file in self.functions_merchant_data:
			if (file_attribute_val == file['distro_path'] or file_attribute_val == ''):
				for function in file['functions']:
					parameters = self.build_function_parameters(function['parameters'])
					value_completions.append( (function['name'] + '\tFunc', function['name'] + parameters) )

		return set(value_completions)


	def build_function_parameters(self, parameters):
		if (len(parameters) == 0):
			return '()'

		parameters_map = []
		count = 0
		for parameter in parameters:
			count += 1
			if (count == len(parameters)):
				count = 0
			parameters_map.append( '${' + str(count) + ':' + parameter + '}' )

		sep = ', '
		return '( ' + sep.join(parameters_map) + ' )'

	def get_current_file_attribute_val(self, view, pt, prefix):
		
		mvdo_tag_region = self.get_mvdo_tag_region(view, pt, prefix)
		if (mvdo_tag_region is False):
			return ''

		file_attribute_all_locations = view.find_by_selector( 'text.mv text.html.basic meta.tag.inline.do.mv attribute-content.file.mv string.quoted.double.mv text.mv source.mv.expr' )
		file_attribute_val = ''
		for file_attribute_location in file_attribute_all_locations:
			if (mvdo_tag_region.contains(file_attribute_location)):
				file_attribute_val = view.substr(file_attribute_location)

		file_attribute_val = file_attribute_val.replace('{', '')
		file_attribute_val = file_attribute_val.replace('}', '')
		file_attribute_val = file_attribute_val.strip()
		return file_attribute_val

	def get_current_value_attribute_val(self, view, pt, prefix):
		
		mvdo_tag_region = self.get_mvdo_tag_region(view, pt, prefix)
		if (mvdo_tag_region is False):
			return ''

		value_attribute_all_locations = view.find_by_selector( 'text.mv text.html.basic meta.tag.inline.do.mv attribute-content.value.mv string.quoted.double.mv text.mv source.mv.expr' )
		value_attribute_val = ''
		for attribute_value_location in value_attribute_all_locations:
			if (mvdo_tag_region.contains(attribute_value_location)):
				value_attribute_val = view.substr(attribute_value_location)

		value_attribute_val = value_attribute_val.replace('{', '')
		value_attribute_val = value_attribute_val.replace('}', '')
		value_attribute_val = value_attribute_val.strip()
		return value_attribute_val


	def get_mvdo_tag_region(self, view, pt, prefix):
		# limit the search left/right to 500 characters
		_LIMIT = 500

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

		if (left_angle_pos is False or right_angle_pos is False):
			return False

		return sublime.Region(left_angle_pos, right_angle_pos)


	def get_function_name(self, view, value_attribute_val):
		match = re.match(r'([a-z0-9_]+)\s*?\(', value_attribute_val, re.I)
		if match:
			return match.group(1)
		else:
			return False


	def get_file_name(self, view, function_name):
		files = []
		for file in self.functions_merchant_data:
			for function in file['functions']:
				if function_name == function['name']:
					files.append(file['distro_path'])
		
		files = set(files)
		if (len(files) == 0):
			return False
		elif (len(files) == 1):
			return next(iter(files))
		else:
			return list(files)


	def choose_file_name(self, index):
		self.insert_file_name(self.quick_panel_data['view'], self.quick_panel_data['pt'], self.quick_panel_data['file_name'][index])
		self.quick_panel_data = {}


	def insert_file_name(self, view, pt, file_name):
		mvdo_tag_region = self.get_mvdo_tag_region(view, pt, '')
		if (mvdo_tag_region is False):
			return ''

		file_attribute_all_locations = view.find_by_selector( 'text.mv text.html.basic meta.tag.inline.do.mv attribute-content.file.mv string.quoted.double.mv text.mv source.mv.expr' )
		for file_attribute_location in file_attribute_all_locations:
			if (mvdo_tag_region.contains(file_attribute_location)):
				file_attribute_pt = file_attribute_location.begin() + 2
				view.run_command('insert_file_name', {
					"args": {
						"file_attribute_pt": file_attribute_pt,
						"file_name": file_name
					}
				})

class InsertFileNameCommand(sublime_plugin.TextCommand):
	def run(self, edit, args):
		self.view.insert(edit, args['file_attribute_pt'], args['file_name'])

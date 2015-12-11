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
		
		return self.get_completions(view, prefix, locations, mvdo_attribute)

	def get_completions(self, view, prefix, locations, mvdo_attribute):
		
		completion_list = []
		flags = 0

		if (mvdo_attribute == 'file'):
			completion_list = self.get_file_completions(view, locations[0], prefix)

		return (completion_list, flags)

	"""
	Custom Methods
	"""
	def read_mvlsk_json(self, path):
		with open( path ) as data_file:
			data = json.load(data_file)
		return data

	def get_file_completions(self, view, locations, prefix):
		file_completions = [(file['distro_path'] + '\tFile', re.escape(file['distro_path'])) for file in self.mvlsk_data]
		return set(file_completions)
			



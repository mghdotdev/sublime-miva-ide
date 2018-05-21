import sublime, sublime_plugin
import json
import os
from os.path import dirname, realpath

# Define Path to JSON Cache
__VARIABLES_MERCHANT_PATH__ = dirname(realpath(__file__)) + os.sep + '/variables-merchant.json'

class VariablesMerchantCompletions(sublime_plugin.EventListener):
	"""
	Variable Completions
	| Smartly determine which variable names to autocomplete based on chosen "scope"(global/system)
	"""
	def __init__(self):
		self.variables_merchant_data = self.read_data_file(__VARIABLES_MERCHANT_PATH__)
		self.quick_panel_data = {}

	def on_query_completions(self, view, prefix, locations):
		prev_pt = max(0, locations[0] - 1)
		if (not ((view.match_selector(locations[0], 'source.mvt') or view.match_selector(locations[0], 'source.mv.expr')) and view.match_selector(prev_pt, 'variable.language'))):
			return None

		if (view.match_selector(prev_pt, 'variable.language.global')):
			variable_scope = 'Global'
		elif (view.match_selector(prev_pt, 'variable.language.system')):
			variable_scope = 'System'
		else:
			variable_scope = None

		return (self.get_completions(view, prefix, locations[0], variable_scope), sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

	"""
	Custom Methods
	"""
	def read_data_file(self, path):
		with open( path ) as data_file:
			data = json.load(data_file)
		return data

	def get_completions(self, view, prefix, pt, variable_scope):
		if (variable_scope in self.variables_merchant_data):
			completions_list = [ ( name + '\t' + variable_scope + ' Var', name ) for name in self.variables_merchant_data[variable_scope] ]
		else:
			completions_list = []

		return list(set(completions_list))
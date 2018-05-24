import sublime, sublime_plugin
import json
import os
from os.path import dirname, realpath

# Define Path to JSON Cache
__VARIABLES_MERCHANT_PATH__ = dirname( realpath( __file__ ) ) + os.sep + '/variables-merchant.json'

class MivaVariableCompletions( sublime_plugin.EventListener ):
	"""
	Variable Completions
	| Smartly determine which variable names to autocomplete based on chosen "scope"(global/system)
	"""
	def __init__( self ):
		self.variables_merchant_data = self.read_data_file( __VARIABLES_MERCHANT_PATH__ )

	def on_query_completions( self, view, prefix, locations ):
		prev_pt = max( 0, locations[0] - 1 )
		if ( not ((view.match_selector( locations[0], 'source.mvt' ) or view.match_selector( locations[0], 'source.mv.expr' )) and view.match_selector( prev_pt, 'variable.language' )) ):
			return None

		if ( view.match_selector( prev_pt, 'variable.language.global' ) ):
			variable_scope = 'global'
			dyn_lookup = True
		elif ( view.match_selector( prev_pt, 'variable.language.system' ) ):
			variable_scope = 'system'
		elif ( view.match_selector( prev_pt, 'variable.language.local' ) ):
			variable_scope = 'local'
			dyn_lookup = True
		else:
			variable_scope = ''

		return ( self.get_completions( view, variable_scope, dyn_lookup ), sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS )

	"""
	Custom Methods
	"""
	def read_data_file( self, path ):
		with open( path ) as data_file:
			data = json.load( data_file )
		return data

	def get_completions( self, view, variable_scope, dyn_lookup ):
		if ( variable_scope in self.variables_merchant_data ):
			completions_list = [ ( name + '\t' + 'runtime var', name ) for name in self.variables_merchant_data[ variable_scope ] ]
		else:
			completions_list = []

		if ( dyn_lookup == True ):
			referenced_points = view.find_by_selector( 'variable.language.' + variable_scope + '.name' )
			for referenced_point in referenced_points:
				referenced_variable = view.substr( referenced_point )
				completions_list.append( ( referenced_variable + '\t' + 'referenced var', referenced_variable ) )

		return list( set( completions_list ) )
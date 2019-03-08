import sublime, sublime_plugin, re

class MvtPosCalculatorCommand( sublime_plugin.TextCommand ):
	def run( self, edit ):
		
		selections = self.view.sel()

		for selection in selections:

			# get region from start of file to first point in selection
			search_region = sublime.Region( 0, selection.a )

			# get actual text of region
			search_text = self.view.substr( search_region )

			# find all matches of "open" tags
			open_tags = re.findall( r'(?i)(<mvt:foreach)', search_text )
			close_tags = re.findall( r'(?i)(<\/mvt:foreach)', search_text )
			
			# calculate the difference between the number of open and closed tags
			open_close_difference = len( open_tags ) - len( close_tags )

			# check the difference
			if ( open_close_difference >= 1 ):

				# generate output string
				output = 'l.pos' + str( open_close_difference );

				# Replace the Variable selection with the generated l.posX
				self.view.replace( edit, selection, output )

			else:

				# Output error message
				self.view.set_status( mvt_error_status_key, 'No valid <mvt:foreach> tags detected' )
				threading.Timer( 3, self.view.erase_status, args=[mvt_error_status_key] ).start()

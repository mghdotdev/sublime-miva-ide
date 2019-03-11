import sublime, sublime_plugin, re, threading

miva_error_status_key = 'miva_pos_calculator_error'

class MvtPosCalculatorCommand( sublime_plugin.TextCommand ):
	def run( self, edit ):
		
		selections = self.view.sel()

		for selection in selections:

			# get region from start of file to first point in selection
			search_region = sublime.Region( 0, selection.a )

			# get actual text of region
			search_text = self.view.substr( search_region )

			# check what language you are in
			is_mvt = self.view.match_selector( selection.a, 'text.mvt' )
			is_mv = self.view.match_selector( selection.a, 'text.mv' )

			# find all matches of "open" tags
			if ( is_mvt ):
				open_tags = re.findall( r'(?i)(<)(mvt:)(foreach|while)', search_text )
				close_tags = re.findall( r'(?i)(<\/)(mvt:)(foreach|while)', search_text )
			elif ( is_mv ):
				open_tags = re.findall( r'(?i)(<Mv)(FOR|WHILE)', search_text )
				close_tags = re.findall( r'(?i)(<\/Mv)(FOR|WHILE)', search_text )
			else:
				continue
			
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
				self.view.set_status( miva_error_status_key, 'No valid <mvt:foreach> tags detected' )
				threading.Timer( 3, self.view.erase_status, args=[miva_error_status_key] ).start()

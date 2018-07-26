import sublime, sublime_plugin, re, threading

# Global Variables
mvt_copy_status_key = 'mvt_convert_and_copy'
mvt_error_status_key = 'mvt_variable_entity_error'

def variable_to_entity(string_value, mvt_entity_encoding):
	# Define the RegEx for "local" and "global" variables
	regex_local = '^l\.settings\:(.+?)$'
	regex_global = '^g\.(.+?)$'

	# Test the RegEx
	local_match = re.match(regex_local, string_value)
	global_match = re.match(regex_global, string_value)

	# If a "local" variable is found, convert it to an entity
	if local_match is not None:

		# Strip `l.settings:` from the match
		varname = local_match.group(1)
		varname_len = len(varname)

		# Generate Entity String
		output = '&mvt' + mvt_entity_encoding + ':%s;' % (varname)

	elif global_match is not None:

		# Strip `g.` from the match
		varname = global_match.group(1)
		varname_len = len(varname)

		# Generate Entity String
		output = '&mvt:global:%s;' % (varname)

	else:
		return False

	return output


def entity_to_variable(string_value):
	# Define the RegEx for "local" and "global" entities
	regex_local = '^&mvt[a-z]?:(?!global:)(.+?);$'
	regex_global = '^&mvt[a-z]?:global:(.+?);$'

	# Test the RegEx
	local_match = re.match(regex_local, string_value)
	global_match = re.match(regex_global, string_value)

	# If a "local" variable is found, convert it to an entity
	if local_match is not None:

		# Strip `&mvt:*;` from the match
		varname = local_match.group(1)
		varname_len = len(varname)

		# Generate Entity String
		output = 'l.settings:%s' % (varname)

	elif global_match is not None:

		# Strip `&mvt:global:*;` from the match
		varname = global_match.group(1)
		varname_len = len(varname)

		# Generate Entity String
		output = 'g.%s' % (varname)

	else:
		return False

	return output


class MvtConvertAndCopy(sublime_plugin.TextCommand):
	def run(self, edit):
		
		# Copy to Clipboard and Convert Entity => Variable |OR| Variable => Entity
		#
		# @param {Regionset} self
		# @param {Edit} edit

		mvt_entity_encoding = self.view.settings().get('mvt_entity_encoding', 'e')
		mvt_entity_encoding = sublime.active_window().active_view().settings().get('mvt_entity_encoding', mvt_entity_encoding)

		# Save previous clipboard value / reset clipboard
		original_clipboard = sublime.get_clipboard()
		sublime.set_clipboard('')

		selections = self.view.sel()

		for selection in selections:
			
			# Get the selection's value and length
			string_value = self.view.substr(selection)

			v2e_output = variable_to_entity(string_value, mvt_entity_encoding)
			e2v_output = entity_to_variable(string_value)

			if (v2e_output is False) and (e2v_output is False):

				# Revert clipboard to value captured before command run
				sublime.set_clipboard(original_clipboard)
				
				# Output error message
				self.view.set_status(mvt_error_status_key, 'No valid variable or entity available for conversion')
				threading.Timer(3, self.view.erase_status, args=[mvt_error_status_key]).start()

				return False

			else:

				if v2e_output is not False:
					output = v2e_output
				elif e2v_output is not False:
					output = e2v_output

				# Copy output to clipboard
				previous_clipboard = sublime.get_clipboard()
				if previous_clipboard is '':
					sublime.set_clipboard(output)

				else:
					sublime.set_clipboard(previous_clipboard + '\n' + output)

		# Status message display
		self.view.set_status(mvt_copy_status_key, 'Converted and copied ' + str(len(sublime.get_clipboard())) + ' characters')
		threading.Timer(3, self.view.erase_status, args=[mvt_copy_status_key]).start()


class MvtVariableConvertToEntityCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		# Convert a MVT Variable to an Entity
		# ex: `l.settings:variable` => `&mvt:variable;`
		# 
		# @param {Regionset} self
		# @param {Edit} edit

		mvt_entity_encoding = self.view.settings().get('mvt_entity_encoding', 'e')
		mvt_entity_encoding = sublime.active_window().active_view().settings().get('mvt_entity_encoding', mvt_entity_encoding)

		selections = self.view.sel()

		for selection in selections:
			
			# Get the selection's value and length
			string_value = self.view.substr(selection)

			# Run conversion function
			output = variable_to_entity(string_value, mvt_entity_encoding)

			if output is False:
				
				# Output error message
				self.view.set_status(mvt_error_status_key, 'No valid variable available for conversion')
				threading.Timer(3, self.view.erase_status, args=[mvt_error_status_key]).start()

			else:

				## Replace the Variable selection with the generated Entity
				self.view.replace(edit, selection, output)


class MvtEntityConvertToVariableCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		
		# Convert a MVT Entity to an Variable
		# ex: `&mvt:variable;` => `l.settings:variable`
		# 
		# @param {Regionset} self
		# @param {Edit} edit

		selections = self.view.sel()

		for selection in selections:

			# Get the selection's value and length
			string_value = self.view.substr(selection)
			
			# Run conversion function
			output = entity_to_variable(string_value)

			if output is False:
				
				# Output error message
				self.view.set_status(mvt_error_status_key, 'No valid entity available for conversion')
				threading.Timer(3, self.view.erase_status, args=[mvt_error_status_key]).start()

			else:

				## Replace the Entity selection with the generated Variable
				self.view.replace(edit, selection, output)


class MvtToggleConversion(sublime_plugin.TextCommand):
	def run(self, edit):
		
		# Toggle conversion between Entity => Variable |OR| Variable => Entity
		#
		# @param {Regionset} self
		# @param {Edit} edit

		mvt_entity_encoding = self.view.settings().get('mvt_entity_encoding', 'e')
		mvt_entity_encoding = sublime.active_window().active_view().settings().get('mvt_entity_encoding', mvt_entity_encoding)

		selections = self.view.sel()

		for selection in selections:
			
			# Get the selection's value and length
			string_value = self.view.substr(selection)

			v2e_output = variable_to_entity(string_value, mvt_entity_encoding)
			e2v_output = entity_to_variable(string_value)

			if (v2e_output is False) and (e2v_output is False):
				
				# Output error message
				self.view.set_status(mvt_error_status_key, 'No valid variable or entity available for conversion')
				threading.Timer(3, self.view.erase_status, args=[mvt_error_status_key]).start()

			else:

				if v2e_output is not False:
					output = v2e_output
				elif e2v_output is not False:
					output = e2v_output

				## Replace the selection with the generated Conversion
				self.view.replace(edit, selection, output)


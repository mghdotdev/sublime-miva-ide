import sublime, sublime_plugin, re

def variable_to_entity(str):
	# Define the RegEx for "local" and "global" variables
	regex_local = '^l\.settings\:(.+?)$'
	regex_global = '^g\.(.+?)$'

	# Test the RegEx
	local_match = re.match(regex_local, str)
	global_match = re.match(regex_global, str)

	# If a "local" variable is found, convert it to an entity
	if local_match is not None:

		# Strip `l.settings:` from the match
		varname = local_match.group(1)
		varname_len = len(varname)

		# Generate Entity String
		output = '&mvt:%s;' % (varname)

	elif global_match is not None:

		# Strip `g.` from the match
		varname = global_match.group(1)
		varname_len = len(varname)

		# Generate Entity String
		output = '&mvt:global:%s;' % (varname)

	else:
		return False

	return output


def entity_to_variable(str):
	# Define the RegEx for "local" and "global" entities
	regex_local = '^&mvt[a-z]?:(?!global:)(.+?);$'
	regex_global = '^&mvt[a-z]?:global:(.+?);$'

	# Test the RegEx
	local_match = re.match(regex_local, str)
	global_match = re.match(regex_global, str)

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

		# Save previous clipboard value / reset clipboard
		original_clipboard = sublime.get_clipboard()
		sublime.set_clipboard('')

		selections = self.view.sel()

		for selection in selections:
			
			# Get the selection's value and length
			str	= self.view.substr(selection)

			v2e_output = variable_to_entity(str)
			e2v_output = entity_to_variable(str)

			if (v2e_output is False) and (e2v_output is False):

				# Revert clipboard to value captured before command run
				sublime.set_clipboard(original_clipboard)
				
				# Output error message
				sublime.error_message('No valid \'variable\' or \'entity\' available for conversion.')

			else:

				if v2e_output is not False:
					output = v2e_output
					conversion_type = 'Variable'
				elif e2v_output is not False:
					output = e2v_output
					conversion_type = 'Entity'

				# Copy output to clipboard
				previous_clipboard = sublime.get_clipboard()
				if previous_clipboard is '':
					sublime.set_clipboard(output)

				else:
					sublime.set_clipboard(previous_clipboard + '\n' + output)

				# Status message display
				# self.view.set_status('mvt_convert_and_copy', conversion_type + ' Converted and Copied')


class MvtVariableConvertToEntityCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		# Convert a MVT Variable to an Entity
		# ex: `l.settings:variable` => `&mvt:variable;`
		# 
		# @param {Regionset} self
		# @param {Edit} edit

		selections = self.view.sel()

		for selection in selections:
			
			# Get the selection's value and length
			str	= self.view.substr(selection)

			# Run conversion function
			output = variable_to_entity(str)

			if output is False:
				
				# Output error message
				sublime.error_message('No valid \'variable\' available for conversion.')

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
			str	= self.view.substr(selection)
			
			# Run conversion function
			output = entity_to_variable(str)

			if output is False:
				
				# Output error message
				sublime.error_message('No valid \'entity\' available for conversion.')

			else:

				## Replace the Entity selection with the generated Variable
				self.view.replace(edit, selection, output)


class MvtToggleConversion(sublime_plugin.TextCommand):
	def run(self, edit):
		
		# Toggle conversion between Entity => Variable |OR| Variable => Entity
		#
		# @param {Regionset} self
		# @param {Edit} edit

		selections = self.view.sel()

		for selection in selections:
			
			# Get the selection's value and length
			str	= self.view.substr(selection)

			v2e_output = variable_to_entity(str)
			e2v_output = entity_to_variable(str)

			if (v2e_output is False) and (e2v_output is False):

				print(v2e_output)
				print(e2v_output)
				
				# Output error message
				sublime.error_message('No valid \'variable\' or \'entity\' available for conversion.')

			else:

				if v2e_output is not False:
					output = v2e_output
				elif e2v_output is not False:
					output = e2v_output

				## Replace the selection with the generated Conversion
				self.view.replace(edit, selection, output)
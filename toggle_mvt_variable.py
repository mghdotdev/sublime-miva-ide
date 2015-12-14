import sublime, sublime_plugin, re

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
				sublime.error_message('No valid \'variable\' available for conversion.')
				return False

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

				print (varname)

				# Generate Entity String
				output = 'l.settings:%s' % (varname)

			elif global_match is not None:

				# Strip `&mvt:global:*;` from the match
				varname = global_match.group(1)
				varname_len = len(varname)

				# Generate Entity String
				output = 'g.%s' % (varname)

			else:
				sublime.error_message('No valid \'entity\' available for conversion.')
				return False

			## Replace the Variable selection with the generated Entity
			self.view.replace(edit, selection, output)
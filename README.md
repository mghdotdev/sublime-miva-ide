# Miva Template Language (MVT)
Miva Template Language (MVT) syntax plugin for Sublime Text 2/3.

##### Syntax Features
* Proper `<mvt:comment>` highlighting.
* Support for `<mvt:assign>` function names.
* Support for `<mvt:do>` function names.
* Support for __toolkit__ and __toolbelt__ function names.

##### Package Features
* Adds Toggle Comment support for `<mvt:comment>` tags and HTML style block comments.
* Adds Symbol List definition preferences for function subsets.

---

### Install via Package Control
* Open Sublime Text 2/3
* Access your Command Palette <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> for Windows/Linux or <kbd>⌘</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> for Mac.
* Type "Package Control: Install Package" ... Press ENTER.
* Search for "MVT", "Miva Template Language" or any similar search term ... Press ENTER.
* Done!

### Plugins that Work Well with Miva Template Language (MVT)
* [DefaultFileType](https://github.com/spadgos/sublime-DefaultFileType) - This package sets the default file type of new files to be either the same as the current file, or a predefined default.

Here is my `default_file_type.sublime-settings` file contents:
```json
{
	"default_new_file_syntax": "Packages/Miva Template Language (MVT)/MVT.tmLanguage",
	"use_current_file_syntax": false
}
```
* [BracketHighlighter](https://github.com/facelessuser/BracketHighlighter) - Bracket and tag highlighter for Sublime Text

Here is my `bh_core.sublime-settings` file contents:
```json
{
	"user_brackets": [
		{
			"name": "mvt_angle",
			"open": "(<)(?=[^?%]|$)",
			"close": "(?:(?<=[^?%])|(?<=^))(>)",
			"style": "angle",
			"scope_exclude": [
				"string",
				"comment"
			],
			"language_filter": "whitelist",
			"language_list": [
				"MVT"
			],
			"plugin_library": "bh_modules.tags",
			"enabled": true
		}
	]
}
```

Here is my `bh_tag.sublime-settings` file contents:
```json
{
	"tag_mode": {
		"xhtml": ["XML"],
		"html": [
			"HTML",
			"HTML 5",
			"PHP",
			"HTML (Jinja Templates)",
			"HTML (Rails)",
			"HTML (Twig)",
			"HTML (Django)",
			"laravel-blade",
			"Handlebars",
			"AngularJS",
			"Java Server Pages (JSP)",
			"MVT"
		],
		"cfml": ["HTML+CFML", "ColdFusion", "ColdFusionCFC"]
	},
	"single_tags": [
		"area", "base", "basefont", "br", "col", "embed", "frame", "hr",
		"img", "input", "isindex", "keygen", "link", "meta", "param",
		"source", "track", "wbr",
		"mvt:else", "mvt:elseif"
	]
}```

# Miva Template Language (MVT)
Miva Template Language (MVT) syntax plugin for Sublime Text 2/3.

## UPDATED FOR 9.0006!
## UPDATED FOR ENGINE 5.24!
### Functions Added in 5.24:
* miva_setprocessname
* miva_async_sleep
* miva_csv_encode
* miva_html_strip
* miva_cdata_encode
* file_touch
* miva_struct_merge
* miva_struct_merge_ref
* indexofl
* indexofli
* miva_array_filter
* miva_array_filter_ref
* miva_ieee754_normalize
* rsa_load_publickey_engine
* rsa_load_privatekey_engine
* crypto_rand_set_rand_engine

---

##### Syntax Features
* Proper `<mvt:comment>` highlighting.
* Support for `<mvt:assign>` function names.
* Support for `<mvt:do>` function names.
* Support for __toolkit__ and __toolbelt__ function names.
* Robust autocomplete for Mivascript and Miva Merchant functions.

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

----

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
	// Determine which style of tag-matching to use in which syntax
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

	// Tags that never have a closing.  You can use 'null' if it does not require a pattern.
	"single_tag_patterns": {
		"xhtml": null,
		"html": "area|base|basefont|br|col|embed|frame|hr|img|input|isindex|keygen|link|meta|param|source|track|wbr|mvt:else|mvt:elseif",
		"cfml": "area|base|basefont|br|col|embed|frame|hr|img|input|isindex|keygen|link|meta|param|source|track|wbr"
	},

	// Self closing HTML tags. You can use 'null' if it does not require a pattern.
	"self_closing_patterns": {
		"xhtml": null,
		"html": "colgroup|dd|dt|li|options|p|td|tfoot|th|thead|tr|mvt:assign|mvt:callcontinue|mvt:callstop|mvt:eval|mvt:exit|mvt:foreachcontinue|mvt:foreachstop|mvt:item|mvt:miva|mvt:whilecontinue|mvt:whilestop",
		"cfml": "cf.+|colgroup|dd|dt|li|options|p|td|tfoot|th|thead|tr"
	}
}
```

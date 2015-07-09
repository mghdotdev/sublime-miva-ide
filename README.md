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

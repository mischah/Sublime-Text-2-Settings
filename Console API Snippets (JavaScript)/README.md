#JavaScript Console API Snippets for Sublime Text

This is a [Sublime Text 2][sublime] package including a bunch of handy snippets for using the Console API of Firebug or other web Inspector tools in the browser of your choice.

[![Flattr Button](http://mischah.github.com/Console-API-Snippets/images/flattr.png)](https://flattr.com/thing/953497/JavaScript-Console-API-Snippets-for-Sublime-Text)

##Installation

### With Package Control ###

If you have the [Package Control][package_control] package installed, you can install Console API Snippets from inside Sublime Text itself. Open the Command Palette and select »Package Control: Install Package«, then search for »Console API Snippets«.

It just works ; ]

… check [this video][package_control_video] if you still need assistance.

###Without Package Control
If you haven't got Package Control installed (seriously, go install it!) you will need to make a clone of this repository into your packages folder, like so:

	git clone https://github.com/mischah/Console-API-Snippets.git Console-API-Snippets
	
The packages folder is located here:

- Windows: %APPDATA%\Sublime Text 2\Packages
- OS X: ~/Library/Application Support/Sublime Text 2/Packages
- Linux: ~/.Sublime Text 2/Packages
- Portable Installation: Sublime Text 2/Data/Packages

… check [this video][manual_install_video] if you still need assistance.

Or just download the package from [download page][download] here at github and copy the folder »Console-API-Snippets« to the packages folder on your machine.

[sublime]: http://www.sublimetext.com/
[download]: https://github.com/mischah/Console-API-Snippets/downloads
[package_control]: http://wbond.net/sublime_packages/package_control
[package_control_video]: https://tutsplus.com/lesson/package-control/
[manual_install_video]: https://tutsplus.com/lesson/installing-plugins-without-package-control/

##Usage
1. Just type »console« and hit the »Tab« key (⇥)
2. Select one of the offered console methods with your cursor
3. Hit the »Return« key (↵)
4. Use Tab to jump through the placeholders and replace them accruing to your needs

![Screenshot](http://mischah.github.com/Console-API-Snippets/images/console.group.png)

You could also wrap console.time() and console.timeEnd() around existing code by opening the command palette (cmd ⌘ + shift ⇧ + P) and begin to type »console.time« and choose »console.time() - Wrapper«.

##About the Console API

You should have a look at »[Firebug and Logging][firebug_info]« to get an idea of how useful it is to know the different console methods. Or check the screencast »[Become a Javascript Console Power-User][screencast]« from Paul Irish.

The snippets I’m offering are based on the console object from Firebug. See [Firebug Console API][firebug_api] for details.

You could also have a look at these tutorials:

- [Firebug Tutorial – Logging, Profiling And Commandline (Part I)][firebug_tut_1]
- [Firebug Tutorial – Logging, Profiling And Commandline (Part II)][firebug_tut_2]

###Different browsers, different capabilities
The implementation of the Console API are differing from browser to browser. 

You don't have to worry when it comes to modern browsers like Chrome, Firefox, Safari and Opera. I’m not sure about IE9 and IE10, but especially the old version of Internet Explorer have a lack of console methods.

So you need a type of »Console Fix« to prevent, that browsers are throwing errors because of unknown methods.

####A basic console fix:
The simplest way to accomplish that is to include a small snippet like the following in which you can define the missing methods you are using as »empty« methods to prevent errors.

	if (!window.console) {
		window.console = {
			log		: function (event) {},
			info	: function (event) {},
			warn	: function (event) {},
			error	: function (event) {}
		};
	}

####A more advanced console fix
Mike Wilcox has a more advanced approach. See »[JavaScript Console Fix V2][console_fix]«.

####One last thing
You should avoid to deploy console output to your production server. 

![](http://mischah.github.com/Console-API-Snippets/images/production.jpg)

If you are using [Grunt][grunt]: There is a [task for that][grunt_task]. 

[firebug_info]: http://getfirebug.com/logging
[screencast]: http://www.youtube.com/watch?v=4mf_yNLlgic
[firebug_api]: http://getfirebug.com/wiki/index.php/Console_API
[firebug_tut_1]: http://michaelsync.net/2007/09/09/firebug-tutorial-logging-profiling-and-commandline-part-i
[firebug_tut_2]: http://michaelsync.net/2007/09/10/firebug-tutorial-logging-profiling-and-commandline-part-ii
[console_fix]: http://clubajax.org/javascript-console-fix-v2-now-with-ios/
[grunt]: http://gruntjs.com/
[grunt_task]: https://github.com/ehynds/grunt-remove-logging

## Author
Michael Kühnel ⤳ [Interweb](http://michael-kuehnel.de)


## License
Use it, change it, fork it, sell it. Do what you will, but please leave the author attribution.

##Version history

**Version 1.0 (10-10-2012)**

- Initial release 

**Version 1.0.1 (10-22-2012)**

- Add CoffeeScript support. Thanks to [Allen Bargi](https://github.com/aziz)

**Version 1.0.2 (11-22-2012)**

- Fix typo in readme and github pages
- Add screencast »Become a Javascript Console Power-User« to readme and github pages

**Version 1.0.3 (09-08-2013)**

- Add console.time wrapper which lets you wrap console.time statements around your selected code. Thanks to [Joe Maller](https://github.com/joemaller)




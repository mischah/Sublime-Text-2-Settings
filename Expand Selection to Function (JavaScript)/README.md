Expand Selection to Function (JavaScript)
=========================================

A command to expand the current selection to the enclosing JavaScript function. This works with named and anonymous functions.

Each time this command runs it will expand farther out. For anonymous functions, the local variable or property name that refers to the function can also be selected. For example, expanding from the `alert` line below will first select the anonymous function (as represented with the «angle quotes»):

    var foobar = «function() {
        alert('Example!')
    }»;

Running it again will then select the variable and trailing semicolon:

    «var foobar = function() {
        alert('Example!')
    };»

After expanding, you can restore the last selection, which will contract the selection back to what it was before. You can expand several times then restore several times to return to your original selection, which is useful for quickly visualizing the scope of deeply nested functions.

Usage
-----

Both commands are available in the `Selection` menu and bound to the following keyboard shortcuts on Windows and Linux:

    Expand Selection to Function (JavaScript)   Alt+Up
    Restore Last Selection                      Alt+Up

Or similarly, on OS X:
    
    Expand Selection to Function (JavaScript)   ⌥↑ (Option+Up)
    Restore Last Selection                      ⌥↓ (Option+Up)

Compatibility
-------------

Compatible with both Sublime Text 2 and Sublime Text 3 (as of beta build 3019).
# To Do

* For 0.0.3:
    * [ ] Implement optional `with` support for `Hx` methods
    * [ ] Implement a `bullet/b` method for easier simple bullets
    * [ ] Implement `w` and `wp` for using `sys.stdout.write` instead of `print`
    * [ ] Clearer global methods and setup for indentation etc.
    * [ ] Clean up and document the indentation methods
    * [ ] Document the centering methods
    * [ ] Move simple under styledterm and document
    * [ ] Make a script that encapsulates building the packages in podman
        * have it take the version and confirm the python and debian and tag match that
        * no need to have it setup the container... possibly a future thing or another project
* Future:
    * [ ] Close review of the native `logging` module and how it relates
    * [x] Add example to show `tprint` functionality
    * [ ] Document the lower level methods
    * [ ] For annotated text, support `[red bold]` in addition to `[red][bold]`
    * [ ] For `p`, support `[red][bold]` in addition to `[red bold]`
* Ideas:
    * syntax like: `P.pp("[green]=>","[JP]=>",a_dictionary)` to reduce need for fstrings

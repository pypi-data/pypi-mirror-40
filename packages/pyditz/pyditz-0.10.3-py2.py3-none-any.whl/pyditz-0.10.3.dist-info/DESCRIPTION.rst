=======================================
 PyDitz -- a distributed issue tracker
=======================================

.. image:: https://drone.io/bitbucket.org/zondo/pyditz/status.png
   :target: https://drone.io/bitbucket.org/zondo/pyditz

.. contents:: :depth: 1

Introduction
============

This package is intended to be a drop-in replacement for the Ditz_
distributed issue tracker.  It provides a ``pyditz`` command-line program,
which acts (mostly) the same way as ``ditz``, and it adds several other
nice things too:

* Whereas ``ditz``, when typed on its own, runs the ``todo`` command,
  ``pyditz`` drops you into a command shell where you can run Ditz commands
  and get completion on command names, issue names and release names
  according to context.

* With PyDitz, you don't have to run it from the same directory where the
  issue database is; it will look in parent directories for it.

* It keeps an intelligent cache of issues, so parsing of all the YAML files
  isn't necessary for each command.  This greatly improves speed when you
  have lots of issues.

* You can extend PyDitz using plugins that you write---either simple
  standalone files (similar to the ``ditz`` 'hook' feature), or packages
  that use setuptools_ entrypoints.

* You can use the database engine of PyDitz in Python programs to migrate
  bug databases to and from Ditz format, or create summary reports in your
  own favourite format.  Me, I prefer reStructuredText_ and rst2pdf_.

Requirements
============

To install and run it:
    PyYAML_, Jinja2_, cerberus_ and six_

To have nice terminal highlighting output:
    Pygments_ (and colorama_ if you're on Windows)

To mark up description and comment text in HTML output:
    Markups_ (and the modules it needs to function)

To run the test suite:
    Nose_, Mock_ and Coverage_

To build the documentation:
    Sphinx_, and the alabaster_ theme.

Installation
============

The usual incantation will install things::

    pip install pyditz

This will install the ``ditz`` module and a console command called
``pyditz`` to invoke in a similar manner to the original ``ditz``.

If you want to shadow the original completely, and have the ``ditz``
command run this instead, you have two options:

1. Define the environment variable ``DITZCMD`` to be ``ditz``.  This only
   takes effect at installation time.  Of course, instead of ``ditz`` you
   can choose anything else more keyboard-friendly.

2. Create your own shell alias.

Documentation
=============

The current documentation can be found online here__.  You can also look at
an example of the `HTML output`_.

__ https://pythonhosted.org/pyditz

License
=======

PyDitz is distributed under the `GNU Lesser General Public License, v2`__
or later.

__ http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html

Links
=====

If you like this, here's a few more things you might want to check out:

* Pitz_ is another Ditz-alike issue tracker, also written in Python.  Its
  bug database is not compatible with Ditz, and I didn't have much luck
  getting it to work, but it might work for you.

* There's another Python project of the same name called akaihola-pyditz_.
  (I only found it after publishing mine, or I might have chosen another
  name.)  Not updated for 6 years, but it has some ideas for logging work
  that might be useful.

* There's also `ditz plus plus`_, another reimplemenation written in C++,
  although that hasn't been updated since mid-2013.

* If you're a fan of `GNU Emacs`_, there's a ditz-mode_ written for it that
  I maintain.  It works with the original Ditz, or PyDitz.

Changes
=======

Version 0.10.3 (2019-01-11)
---------------------------

* bugfix: Fix highlighting customization

Version 0.10.2 (2018-08-31)
---------------------------

* bugfix: Resolve problems with cerberus update
* bugfix: Resolve problems with markups update

Version 0.10.1 (2017-07-31)
---------------------------

* bugfix: Crash when trying to create db

Version 0.10 (2016-11-27)
-------------------------

* Improve startup operations
* Allow abbreviation of issue names
* Sort issues by last-modified time
* Implement issue-claiming commands
* Use cerberus for data validation

Version 0.9.1 (2016-03-24)
--------------------------

* bugfix: Line wrapping problem in terminal
* bugfix: Fix problems with version detection
* Minor package improvements

Version 0.9 (2015-09-27)
------------------------

* bugfix: Bytes output if pygments is not installed
* bugfix: Initialization command doesn't work
* Implement the 'edit' command
* Implement command plugins
* Add support for markup in HTML output
* Allow per-project config file
* New command to list all issues
* Add project file to version control
* Add validation schemas
* Search more fields with grep

Version 0.8.1 (2015-08-18)
--------------------------

* bugfix: Fix non-ASCII text in issue data
* bugfix: HTML plugin load failure

Version 0.8 (2014-12-05)
------------------------

* bugfix: Grep arguments not handled correctly
* Allow customization of HTML output
* Allow issues to be specified by ID
* Add progress time indicator to 'show' and HTML
* Implement exporting directly to archive
* Add section arg to config command
* Add exporter plugin system
* Add python 3 support
* Improve the default HTML style
* Move ~/.ditzrc to ~/.ditz/ditz.cfg
* Relicense under LGPL

Version 0.7 (2014-09-28)
------------------------

* bugfix: Handle YAML comment char in strings
* Add VCS support
* Add unicode support
* Add issue type column to HTML output
* Add command to display configuration
* Implement the 'validate' command
* Add output highlighting
* Add support for command aliases
* Add pager support
* Improve the documentation
* Wire up the remaining program options
* Improve configuration settings
* Improve logging command output

Version 0.6.2 (2014-08-10)
--------------------------

* bugfix: Name substitution not done in issue description

Version 0.6.1 (2014-08-09)
--------------------------

* bugfix: Print message on successful unassignment
* bugfix: Ignore unreleased releases when assigning issues

Version 0.6 (2014-03-28)
------------------------

* bugfix: Handle non-ASCII characters when writing output
* Install as 'ditz' if required by user
* Add HTML component column if multiple components in use
* Don't show HTML release column for unassigned issues
* Print message on successful issue assignment

Version 0.5.2 (2013-12-20)
--------------------------

* bugfix: Blank lines shouldn't end a comment

Version 0.5.1 (2013-12-18)
--------------------------

* bugfix: Prompt for component when creating issues
* bugfix: Show issue status even if not closed

Version 0.5 (2013-12-12)
------------------------

* bugfix: Issue names not replaced in comment text
* bugfix: Reconfigure clobbers existing file
* Add sortable tables to HTML output
* Write some user documentation
* Add a user config file

Version 0.4 (2013-12-09)
------------------------

* Implement the 'html' command

Version 0.3 (2013-11-23)
------------------------

* bugfix: Multiple 'issuedir' keywords in init

Version 0.2 (2013-11-23)
------------------------

* bugfix: Fix up problems with blank comments

Version 0.1 (2013-11-23)
------------------------

* bugfix: Fix round-tripping of issue files
* Implement all the ditz commands

.. _Coverage: https://pypi.python.org/pypi/coverage
.. _Ditz: http://rubygems.org/gems/ditz
.. _GNU Emacs: https://www.gnu.org/software/emacs
.. _HTML output: https://pythonhosted.org/pyditz/_static/index.html
.. _Jinja2: http://jinja.pocoo.org
.. _Markups: https://pypi.python.org/pypi/Markups
.. _Mock: https://pypi.python.org/pypi/mock
.. _Nose: https://pypi.python.org/pypi/nose
.. _Pitz: https://github.com/mw44118/pitz
.. _Pygments: https://pypi.python.org/pypi/Pygments
.. _PyYAML: https://pypi.python.org/pypi/PyYAML
.. _Sphinx: http://sphinx.pocoo.org
.. _akaihola-pyditz: https://github.com/akaihola/pyditz
.. _alabaster: https://pypi.python.org/pypi/alabaster
.. _cerberus: https://pypi.python.org/pypi/cerberus
.. _colorama: https://pypi.python.org/pypi/colorama
.. _ditz plus plus: http://sourceforge.net/projects/ditz
.. _ditz-mode: https://bitbucket.org/zondo/ditz-mode
.. _reStructuredText: http://docutils.sourceforge.net/docs/ref/rst/introduction.html
.. _rst2pdf: https://pypi.python.org/pypi/rst2pdf
.. _setuptools: http://pythonhosted.org/setuptools
.. _six: https://pypi.python.org/pypi/six



SrcWatcher
=======

A python script to run a command when a file changes. Think nodemon for node.js.

Install
-------
Simply download the .py file and add it to your path.

Usage
-------
These assume you are executing the script in the current working directory.
 
- Simple Example

.. code-block:: fish

    srcwatcher.py "python main.py" main.py

- Specific File Extensions

.. code-block:: fish

    srcwatcher.py "python main.py" *.py

- All files in the current working directory

.. code-block:: fish

    srcwatcher.py "python main.py" *.*
    

TODO
-------
- Add watching for nested files in subdirectories
- Allow for multiple file extension types
- **DONE** Monitor a specific file for changes
- **DONE** Monitor multiple files with a specific extension for changes
- **DONE** Monitor all files in the current working directory for changes

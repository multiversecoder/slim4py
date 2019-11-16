# Slim4Py - Slim Templates for Python


What is Slim?
-------------

Slim is a fast, lightweight templating engine whose goal is reduce html syntax to the essential parts without becoming cryptic.

Check on the official site: [http://slim-lang.com/](http://slim-lang.com/)


What is slim4py?
-------------

Slim4Py is a simple script that allows you to use all the functions of Slim (Ruby)
in any python framework with the addition that you can also use the
mako syntax (a popular and fast template engine for python).

Here is a small example of usage:

```python
from slim4py.slim import Slim

slim = Slim("slim")

def say_hello():
    return "Hello World"

slim.render("example.slim", say_hello=say_hello, year="2019", author="https://github.com/multiversecoder/slim4py")
```


About Magic Comments
--------------------

If you need to use python inside the templates, you can define at the beginning of the file a magic comment containing all the variables that will be rendered by mako using the logic written in python.

To define a magic comment use:

    / mako_vars = [name_var_1, name_var_2, ...]

This comment will be detected by the engine and rendered using mako and python.


Combining Python With Ruby
--------------------------

``` slim
/ mako_vars = [list_]
doctype 5
html
  head
    title Slim4Py Example - Basic
  body
    #contents
      |
      % for a in list_:
        % if a.startswith("t"):
            its two or three
        % elif a.startswith("f"):
            four/five
        % else:
            one
        % endif
      % endfor
  footer
    | Copyright - #{author} - #{year}
```


Requirements
------------

You need Python 3.7 or later to run slim4py, ruby and the slim gem

In Ubuntu, Mint and Debian you can install Requirements like this:

    $ apt-get install python3 python3-pip
    $ apt-get install ruby
    $ gem install slim

For RHEL, Fedora and CentOS:

    $ dnf install python3 python3-pip
    $ dnf install ruby
    $ gem install slim

For other systems

    - Install Python3
    - Install Ruby
    - gem install slim


Quick start
-----------

slim4py can be installed using pip:

    $ python3 -m pip install -U slim4py

or:

    $ pip install slim4py

for install slim4py from source:

    $ git clone https://github.com/multiversecoder/slim4py
    $ cd ./slim4py
    $ pip install .


Development status
------------------

slim4py is beta software, but it has already been used in production and it has an extensive test suite.



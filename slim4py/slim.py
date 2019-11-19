"""
Slim4Py is a simple script that allows you to use all the functions of Slim (Ruby)
in any python framework with the addition that you can also use the
mako syntax (a popular and fast template engine for python).
"""

__author__ = "Adriano Romanazzo"
__copyright__ = "Copyright 2019, Adriano Romanazzo (https://github.com/multiversecoder)"
__license__ = "MIT"
__maintainer__ = "https://github.com/multiversecoder"
__status__ = "Production"


import os
import json
import shutil
import tempfile
import subprocess
import mako.template

from copy import copy
from typing import Optional, Any, Callable, Dict, Tuple


class SlimException(Exception):
    pass


class SlimNotInstalled(Exception):
    pass


class RubyNotInstalled(Exception):
    pass


class TemplateNotFound(Exception):
    pass


class Slim:

    def __init__(self, template_dir: str) -> None:
        """
        Set the templates basedir
        Used by the Slim::Engine (ruby) to render includes and other things
        Used by this script to check if the template exists

        Parameters
        ----------
            template_dir: str
                the main directory of templates

        """
        self.template_dir = os.path.abspath(template_dir)

    def __check_if_tpl_exists(self, filename: str) -> None:
        """
        Check if the template exists

        Parameters
        ----------
            filename: str
                the path of the template to render

        Raises
        ------
            TemplateNotFound
                if the template does not exists
        """
        template = os.path.join(self.template_dir, filename)

        if not os.path.exists(template):
            err = f"Cannot find the template {template}\n\
            Check that you have set the right directory for the templates \
            or that you have not made a mistake by typing the name of the template."
            raise TemplateNotFound(err)

    def __check_for_ruby(self) -> None:
        """
        Check if the ruby intepreter is installed

        Raises
        ------
            RubyNotInstalled
                If ruby is not installed in this system
        """
        if not bool(shutil.which("ruby")):
            raise RubyNotInstalled(
                "To Run this Ruby Slim Bridge You need to install Ruby on this system")

    def __prepare_for_mako(self, filename: str, **kwargs) -> Tuple[Dict[str, Callable], Dict[str, Callable]]:
        """
        Check if there are python functions or magic comments

        Note
        ----
            The magic comment is: // mako_vars = [var1, var2, ...]
            This magic comment is sensitive to new lines and will be stripped from html after the transfer to ruby.

        After opening the file we look for the magic comment at the beginning of the file and if present
        we add the variables declared into mdict, a dictionary that contains the values to be rendered with mako.
        If there is no magic comment, we analyze the presence of functions within kwargs and if there is a function,
        it is also added to mdict.

        In both cases, any element added in mdict is removed from kwargs

        Returns
        -------
            Tuple[Dict[str, Callable],Dict[str, Callable]]
                The first [0] is a dictionary containing the vars for mako,
                the second [1] is a dictionary containing the vars for ruby,
        """
        mdict = {}
        kwargs2 = copy(kwargs)

        with open(f"{self.template_dir}/{filename}" if not filename.startswith("/tmp/tmp") else filename) as f:

            content = f.read()

            if content.split("\n", 1)[0].replace(" ", "").startswith("/mako_vars"):
                magic_comment = [f"{el.strip(' ')}" for el in content.split("\n", 1)[0].replace("/", "").split("=")[1].replace(" ", "").replace("[", "").replace("]", "").split(",")]

                for val in magic_comment:
                    for k, v in kwargs.items():
                        if k == val:
                            mdict[k] = v
                            del kwargs2[k]

            for k, v in kwargs.items():
                if hasattr(v, "__call__"):
                    mdict[k] = v
                    del kwargs2[k]

        return mdict, kwargs2

    def __check_for_slim_gem(self) -> None:
        """
        Check if the slim gem is installed in this system

        Raises
        ------
            SlimNotInstalled
                if the gem is not installed
        """
        try:
            subprocess.check_output(["gem",  "list", "-i", "slim"])
        except subprocess.CalledProcessError:
            raise SlimNotInstalled(
                "Install Slim using 'gem install slim' to use this compiler")

    def __create_tmp_tpl(self, content: str) -> str:
        """
        Creates a temporary file containing the template rendered by mako

        Parameters
        ----------
            content: str
                the content rendered by mako
        Returns
        -------
            str
                the name of the temporary file
        """
        _, temp_tpl = tempfile.mkstemp()
        with open(temp_tpl, "w") as tp:
            tp.write(content)
        return temp_tpl

    def __delete_tmp_file(self, filename: str) -> None:
        """
        Deletes the temporary file

        Parameters
        ----------
            filename: str
                the name of the file to delete
        """
        os.remove(filename)

    def __render_with_mako(self, filename: str, **kwargs) -> str:
        """
        Render the file using mako

        Parameters
        ----------
            filename: str
                the name of the file to render using mako
            kwargs

        Returns
        -------
            str
                the content of the rendered file
        """
        with open(f"{self.template_dir}/{filename}") as tpl:
            tpl = mako.template.Template(
                tpl.read(), strict_undefined=True).render(**kwargs)
        return tpl

    def __create_tmp_json(self, args: dict) -> str:
        """
        Creates a temporary file containing the variables to be passed to ruby using json

        Parameters
        ----------
            args: dict
                Topics to be passed to ruby via json [kwargs]
        Returns
        -------
            str
                the name of the temporary file
        """
        _, temp_json = tempfile.mkstemp()
        with open(temp_json, "w") as tj:
            tj.write(json.dumps(args))
        return temp_json


    def render(self, filename: str, **kwargs) -> Optional[str]:

        self.__check_if_tpl_exists(filename)

        self.__check_for_ruby()

        self.__check_for_slim_gem()

        mkwargs, kwargs = self.__prepare_for_mako(filename, **kwargs)

        # check if mkwargs is not empty
        if mkwargs != {}:
            mako_rendered = self.__render_with_mako(filename, **mkwargs)
            # creates a temp file with the rendered template to pass to ruby
            temp_tpl = self.__create_tmp_tpl(mako_rendered)

        # creates a file with kwargs (json)
        temp_json = self.__create_tmp_json(kwargs)

        # return the template rendered by slim
        ret = subprocess.check_output(["ruby",
                                       f"{os.path.abspath(os.path.dirname(__file__))}/slim_compile.rb",
                                       self.template_dir, filename if "temp_tpl" not in locals() else temp_tpl, temp_json], shell=False).decode("utf-8")

        # deletes the temporary json file
        self.__delete_tmp_file(temp_json)

        # deletes the temporary template file if exists
        if "temp_tpl" in locals():
            self.__delete_tmp_file(temp_tpl)

        # if ruby returned an error, raise an exception
        if ret.startswith("#<Slim_Error_for_python>"):
            raise SlimException(ret)

        return ret

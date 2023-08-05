# -*- coding: utf-8 -*-

"""Main module."""

from inspect import signature, Parameter
from itertools import zip_longest
from pyvimplugin import extended_vim as vim
import logging
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


"""
Stores the function sent to vim.
keys  :   name of the vim function
values:   code of the (wrapped) python function
"""
vim_functions = {}


def vim_function(fn):
    """
    Wraps the python function ``fn`` inside a vim functions
    that can be called from vim.

    Boiler-plate code to fetch arguments from vim and convert the
    return value to vim-string is automatically generated.

    :param fn:  any python function that you want to use in vim
    :return:    the function that was provided, untouched
    """
    # parse the values of the arguments directly from vim
    wrapped = wrap_for_vim(fn)
    # execute vim code to define a vim function
    vim_name = send_to_vim(wrapped, fn)
    logger.info(f'Defined "{vim_name}"')
    # return the function so that this can be used as @decorator
    return fn


def wrap_for_vim(fn):
    """
    Returns a wrapper around the function that fetches the arguments
    automatically from vim.

    Features:
        - args are fetched from ``a:<argname>``
        - kwargs are fetched from vim's optional arguments ``"a:000"``
        - default python values are used when nothing found in vim's
        - attempt to cast vim's value to correct python type using type
        annotations

    :param fn:  a function with type annotated parameters, and possibly
    defaults values
    :return:    a wrapper around the function that automatically parses the
    arguments from vim ``a:`` variables
    """
    all_params = signature(fn).parameters  # {param_name: param_obj}
    req_params = required(all_params)      # only params without default
    opt_params = optional(all_params)      # only params with default

    def vim_wrapper():
        req_values = add_vim_args(req_params)  # {name: (vim_value, param_obj)}
        opt_values = add_vim_opts(opt_params)
        all_values = {**req_values, **opt_values}

        # use param_obj.default if no vim_value, else type_cast(vim_value)
        args = compute_defaults_and_types(all_values)

        # call the function with the arguments that we fetched from vim
        result = fn(**args)
        vim_result = vimify(result)        # "smart" convert to string
        return vim_result

    return vim_wrapper


def required(params):
    """ Filters `params` to keep only (args) those without default value. """
    return {n: p for (n, p) in params.items() if p.default is Parameter.empty}


def optional(params):
    """ Filters `params` to keep only (kwargs) those with default value. """
    return {n: p for (n, p) in params.items() if p.default is not
            Parameter.empty}


def add_vim_args(args):
    """ Fetches the parameters from vim and adds them to the dict. """
    names, params = zip(*args.items())
    values = vim.get_args(names)
    logger.debug(f'Vim arguments: {values}')
    return dict(zip(names, zip(values, params)))


def add_vim_opts(args):
    """ Fethes parameters from vim's ``a:000`` list and adds them to the dict.
        When the list is exhausted, None is used instead. """
    if not args:
        return args
    values = vim.get_opts_args_list()
    logger.debug(f'Vim options: {values}')
    names, params = zip(*args.items())
    return dict(zip(names, zip_longest(values, params)))


def compute_defaults_and_types(values):
    """ Computes: ``type_cast(vim_value) or default`` for each args. """
    return dict(compute_value(v) for v in values.items())


def compute_value(v):
    """ Returns (arg_name, type_cast(vim_value) or default_value). """
    name, (value, param) = v
    if value is not None:
        type_cast = argtype(param)
        return (name, type_cast(value))
    else:
        return (name, param.default)


def argtype(arg):
    """ Attempts to discover the type of ``arg`` based on type annotations or
        default values. """
    no_default = arg.default is Parameter.empty
    no_annotation = arg.annotation is Parameter.empty
    if no_default and no_annotation:
        return lambda x: x
    if no_annotation:
        return type(arg.default)
    else:
        return arg.annotation


def vimify(arg):
    """
    Convert to string for vim, handles corner cases:
    - if arg is None, empty string is returned.
    """

    if arg is None:
        return ''
    else:
        return repr(arg)


def send_to_vim(wrapped, fn):
    """
    Creates a vim function with same signature as ``fn``
    and whose implementation is a call to ``wrapped``.

    The function ``wrapped`` may parse vim's ``a:<name>`` variables.
    The name of the vim function is the camel-cased name of ``fn``.

    :param wrapped:  a python function of arity 0 and return value a string.
    :param fn:       a python function whose signature will be used for the
                     vim function.
    """
    vim_name = camelize(fn.__name__)    # name of the vim function
    vim_functions[vim_name] = wrapped   # body of the vim function
    arg_str = vim_arguments_string(fn)  # arguments of the vim function

    # send code to create the vim function in vim
    vim.command(remove_indentation(f"""
    fun! {vim_name}({arg_str})
        python3<<ENDPYTHON
            from pyvimplugin import pyvimplugin
            import vim
            result = pyvimplugin.vim_functions['{vim_name}']()
            vim.command('return ' + repr(result))
            del result
        ENDPYTHON
    endf """))
    return vim_name


def vim_arguments_string(fn):
    """ Creates a comma-separated argument string in vim's format.
        Positional parameters are translated to vim's required parameters.
        When present, named parameters are translated to ``...``,
        i.e. vim's optional parameters.
    """
    all_params = signature(fn).parameters
    req_params = required(all_params)
    opt_params = optional(all_params)

    names = req_params.keys()
    arg_str = ', '.join(names)
    if opt_params:
        arg_str += ', ...'
    return arg_str


def camelize(string):
    """ Converts a string to CamelCaseIdentifier. """
    splits = re.split('([^a-zA-Z0-9])', string)
    return ''.join(a.capitalize() for a in splits
                   if a.isalnum())


def remove_indentation(multiline_str):
    """ ```lstrip``` each lines. """
    r = '\n'.join(l.lstrip() for l in multiline_str.splitlines())
    logger.debug('Unindented code:\n' + r)
    return r


def main():
    logger.setLevel(logging.WARNING)

    @vim_function
    def py_vim_plugin(a: int, b: int, c="Welcome"):
        message = f'{c} to pyvimplugin! {a + b}'
        print(message)
        return a + b

    vim_functions['PyVimPlugin']()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import importlib
import inspect
import typing as tx

# class Meta:
#     params = { 'sigmaX' : { 'type' : int,
#                              'max' : 255,
#                              'min' : 0    },
#                'sigmaY' : { 'type' : int,
#                              'max' : 255,
#                              'min' : 0    },
#                'sigmaZ' : { 'type' : int,
#                              'max' : 255,
#                              'min' : 0    } }
#     input =  { 'type' : 'image', 'mode' : '*' }
#     output = { 'type' : 'image', 'mode' : '*' }

class Parameter(object):
    
    __slots__: tx.ClassVar[tx.Tuple[str, ...]] = ('type', 'min',
                                                          'max',
                                                          'default')
    
    def __init__(self, parameter_type,
                       parameter_min,
                       parameter_max,
                       default_value=None, **kwargs):
        self.type = parameter_type
        self.min = parameter_min
        self.max = parameter_max
        self.default = default_value or parameter_type.__call__()
    
    def __get__(self,
                instance: tx.Any,
                cls: tx.Optional[type] = None) -> tx.Tuple[str, ...]:
        if cls is None:
            cls = type(instance)
        return dict(type=self.type,
                     min=self.min,
                     max=self.max,
                 default=self.default)
    
    def __set__(self,
                instance: tx.Any,
                newdict: tx.Mapping[str, tx.Any]):
        if 'type' in newdict:
            self.type = newdict['type']
        if 'min' in newdict:
            self.min = newdict['min']
        if 'max' in newdict:
            self.max = newdict['max']
        if 'default' in newdict:
            self.default = newdict['defualt']
    
    def __delete__(self,
                   instance: tx.Any):
        raise AttributeError("Can't delete a Parameter attribute")

""" MEET MISTER ACORONTIA STYX """

QUALIFIER = '.'

def qualified_import(qualified):
    """ Import a qualified thing-name.
        e.g. 'instakit.processors.halftone.FloydSteinberg'
    """
    if QUALIFIER not in qualified:
        raise ValueError("qualified_import() needs a qualified name (got %s)" % qualified)
    head = qualified.split(QUALIFIER)[-1]
    tail = qualified.replace("%s%s" % (QUALIFIER, head), '')
    module = importlib.import_module(tail)
    cls = getattr(module, head)
    return cls

def qualified_name(cls):
    """ Get a qualified thing-name for a class.
        e.g. 'instakit.processors.halftone.FloydSteinberg'
    """
    mod_name = getattr(cls, '__module__')
    cls_name = getattr(cls, '__qualname__',
               getattr(cls, '__name__'))
    return "%s%s%s" % (mod_name, QUALIFIER, cls_name)

def default_arguments(cls):
    """ Get a dictionary of the keyword arguments with provided defaults,
        as furnished by a given classes’ “__init__” function.
    """
    argspec = inspect.getargspec(cls)
    if len(argspec.args) == 1 or argspec.defaults is None:
        return dict()
    # The first thing in argspec.args is “self”:
    return dict(zip(argspec.args[1:], argspec.defaults))

def add_argparser(subparsers, cls):
    """ Add a subparser -- an instance of “argparse.ArgumentParser” --
        with arguments and defaults matching the keyword arguments and
        defaults provided by the given class (q.v. “default_arguments(…)”
        definition supra.)
    """
    qualname = qualified_name(cls)
    cls_help = getattr(cls, '__doc__', "help for %s" % qualname)
    parser = subparsers.add_parser(qualname, help=cls_help)
    for argument_name, argument_value in default_arguments(cls):
        argument_type = type(argument_value)
        add_argument_args = dict(type=argument_type,
                                 default=argument_value,
                                 help='help for argument %s' % argument_name)
        if argument_type is bool:
            add_argument_args.update({ 'action' : 'store_true' })
        parser.add_argument('--%s' % argument_name, **add_argument_args)
    return parser


def test():
    # Test “qualified_import()”:
    class_name = 'instakit.processors.halftone.SlowFloydSteinberg'
    ImportedFloydSteinberg = qualified_import(class_name)
    assert ImportedFloydSteinberg.__name__ == 'SlowFloydSteinberg'
    assert ImportedFloydSteinberg.__qualname__ == 'SlowFloydSteinberg'
    assert ImportedFloydSteinberg.__module__ == 'instakit.processors.halftone'
    
    class_name = 'instakit.processors.halftone.Atkinson'
    ImportedAtkinson = qualified_import(class_name)
    assert ImportedAtkinson.__name__ == 'Atkinson'
    assert ImportedAtkinson.__qualname__ == 'Atkinson'
    assert ImportedAtkinson.__module__ == 'instakit.processors.ext.halftone'
    
    # Test “qualified_name()”:
    class_name = qualified_name(Parameter)
    assert class_name == '__main__.Parameter'
    
    
    
    # Test “default_arguments()”:
    
    # Test “add_argparser()”:
    
    


if __name__ == '__main__':
    test()
#! /usr/bin/env python

import os
import sys
import json
import jinja2

DIR_SCRIPT = os.path.dirname(os.path.realpath(__file__))
DIR_BASE = os.path.abspath(os.path.join(DIR_SCRIPT, '..'))
DIR_TEMPLATE = os.path.join(DIR_BASE, 'templates')
DIR_DATA = os.path.join(DIR_BASE, 'data')
DIR_OUTPUT = os.path.abspath(os.path.join(DIR_BASE, '..'))

JINJA_ENV_OPTIONS = {
    'block_start_string'   : '[%',
    'block_end_string'     : '%]',
    'variable_start_string': '[[',
    'variable_end_string'  : ']]',
    'comment_start_string' : '[#',
    'comment_end_string'    : '#]',
}



class Context(dict):
    """This class serves as a render context dictionary that will
    automatically load all it's data from JSON files in the data
    directory.

    """
    def __init__(self):
        self.path = DIR_DATA
    
    def load(self, recursive=False):
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                if filename.endswith('.json'):
                    key = filename[:-5]
                    with open(os.path.join(dirpath, filename), 'r') as fd:
                        value = json.load(fd)
                    self[key] = value

    
class Compiler(object):
    """This class serves as an abstraction layer to the template compiler
    and it's configuration. Just instantiate the objects and call
    .build(<name>, <context>) with the name of the template to compile
    and the render context.

    """
    def __init__(self):
        options = JINJA_ENV_OPTIONS
        options.setdefault('loader', jinja2.FileSystemLoader(DIR_TEMPLATE))
        self.env = jinja2.Environment(**options)
        
        def maxlength(iterable, attribute=None):
            maxlength = 0
            for item in iterable:
                if attribute:
                    item = item.get(attribute, None)
                try:
                    length = len(item)
                except TypeError:
                    length = 0
                if length > maxlength:
                    maxlength = length
            return maxlength
        self.env.filters['maxlength'] = maxlength
        
        def currency(value):
            return u'${:20,.2f}'.format(value)
        self.env.filters['currency'] = currency
        
        self.env.filters['json'] = json.dumps
    
    def build(self, name, context):
        template = self.env.get_template(name)
        output = template.render(**context)
        with open(os.path.join(DIR_OUTPUT, name), 'w') as fd:
            fd.write(output)


def main():
    context = Context()
    context.load()
    compiler = Compiler()
    compiler.build('index.html', context)

if __name__ == '__main__':
    main()

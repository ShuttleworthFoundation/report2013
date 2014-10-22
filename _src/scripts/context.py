import os
import json

__all__ = ['context']

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
                        value = json.load(fd, object_pairs_hook=collections.OrderedDict)
                    self[key] = value

context = Context()
context.load()

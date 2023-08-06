# repobot/commands/base.py
'''The base command.'''

from docopt import docopt

class Base(object):
    '''A base command.'''

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError('The run() command was not implemented for this subclass')

    def checkHelp(self, doc):
        if '--help' in self.options:
            docopt(doc, argv=['--help'])


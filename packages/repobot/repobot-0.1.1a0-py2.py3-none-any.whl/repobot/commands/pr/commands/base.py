# repobot/commands/base.py
'''The base command.'''

from docopt import docopt

class Base(object):
    '''A base command.'''

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.options = {}

    def run(self):
        raise NotImplementedError('The run() command was not implemented for this subclass')

    def checkHelp(self, doc):
        if '--help' in self.options:
            docopt(doc, argv=['--help'])

class SubcommandBase(object):
    '''A base subcommand

    Subcommands get the argv list as input rather than parsed options.
    the subcommands docstring should then be used with docopt, to allow
    more parsing options than given from the subcommand file'''

    def __init__(self, argv, *args, **kwargs):
        self.argv = argv
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError('The run() command was not implemented for this subclass')

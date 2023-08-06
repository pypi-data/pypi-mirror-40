# repobot/commands/hello.py
'''
rbot pr - MANAGE PULL REQUESTS

Usage:
    rbot pr new
    rbot pr new <compare_branch>
    rbot pr new <base_branch> <compare_branch>
    rbot pr merge
    '''
from inspect import getmembers, isclass
from ..base import SubcommandBase
from json import dumps
from docopt import docopt
from ..utils import set_token
from . import commands
print(commands)
import requests

class Pr(SubcommandBase):

    def run(self):

        if '--help' in self.argv:
            self.argv.remove('--help')
            options = docopt(__doc__, help=False)
            options['--help'] = True
        else:
            options = docopt(__doc__, help=False)

        # Here we'll try to dynamically match the command the user is trying to run
        # with a pre-defined command class we've already created.
        for (k, v) in options.items():
            if hasattr(commands, k) and v:
                module = getattr(commands, k)
                rcommands = getmembers(module, isclass)
                command = [command[1] for command in rcommands if command[0] != 'Base'][0]
                command = command(options)
                command.run()

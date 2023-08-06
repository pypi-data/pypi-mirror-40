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

        return

        print(self.argv)
        self.options = docopt(__doc__, argv=self.argv[1:], help=True)

        if self.options['new']:
            return self.new()
        if self.options['merge']:
            return self.merge()


        #r = requests.get('https://api.github.com/user', auth=basicauth)
        print(self.argv)
        print(self.options)
        print('the re was')
        print('Hello, from pr!')
        print('You suplied the following optons:', dumps(self.options, indent=2, sort_keys=True))

    @set_token
    def new(self, basicauth):
        if self.options['<base_branch>'] and self.options['<compare_branch>']:
            print('base and compare')

    @set_token
    def merge(self, basicauth):
        print('merge')

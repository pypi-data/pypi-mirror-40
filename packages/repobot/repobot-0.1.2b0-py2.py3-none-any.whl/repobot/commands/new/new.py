# new.py
'''
rbot new - CREATE A NEW REPOSITORY

Usage:
    rbot new
    rbot new <repo_name> [-DC] [--private --clone --org=<org_name>]

Description:
    Create a new repository for the authenticated user or an organization the authenticated
    user belongs to. In its first form, repobot will prompt the user for nescessary
    information (name, description, private options, etc). In its second form, repobot will
    prompt for missing information, if nescessary. Prompts do not inclued creating in an
    organizaton and must be set with the --org flag instead.
    
    Upon successful creation, repobot provides the option of cloning the new repository in
    the directory where repobot was ran.

Options:
    -D                Use default repository optinos for any missing information. No prompts will
                      be given. The default options are: no description, public repo, no readme.

    -C, --clone       Automatically clone the repository after successfully creating.
    
    --private         Set the visibility option to private.
    
    --org=<org_name>  When set, repository will be created in the given organization. User must
                      have appropriate permissions set.
'''
import json
import sys
import requests
import os
from os import path

from ..base import Base
from ..utils import set_token, cinput, yn_input, allowescape, checkshellcommand

from docopt import docopt

class New(Base):

    @set_token
    def run(self, basicauth):
        self.checkHelp(__doc__)

        name = self.getname()

        description = self.getdescription()
        isprivate = self.getprivateoption()
        hasreadme = self.getreadmeoption()

        data = {'name': name,
                'description': description,
                'private': isprivate,
                'auto_init': hasreadme,}
        POST_URL = 'https://api.github.com/orgs/%s/repos' % (self.options['--org']) \
                    if self.options['--org'] \
                    else 'https://api.github.com/user/repos'
        
        res = requests.post(POST_URL, auth=basicauth, json=data)
        
        if res.status_code == 201:
            resdata = res.json()
            print('Successfully created at ' + resdata['clone_url'])
            self.cloneprompt(resdata['clone_url'])
        else:
            print('Couldn\'t create repo')
            print(json.dumps(res.json(), indent=2))

    @allowescape
    def getname(self):
        if self.options['<repo_name>'] is not None:
            return self.options['<repo_name>']
        return cinput('Repo name: ',
                      expression=r'^[a-z|A-Z|0-9|\-\_]*$',
                      error_message='Invalid name - use [a-z|A-Z|0-9|-_] characters only.')

    @allowescape
    def getdescription(self):
        if self.options['-D'] is not False:
            return ''
        return input('Description (optional): ')

    @allowescape
    def getprivateoption(self) -> bool:
        if self.options['-D']:
            return 'false'
        if self.options['--private']:
            return 'true'
        return yn_input('Private Repository? ', default=False)

    @allowescape
    def getreadmeoption(self) -> bool:
        if self.options['-D'] is not False:
            return 'false'
        return yn_input('Initialize with a README? ', default=False)

    @allowescape
    @checkshellcommand('git')
    def cloneprompt(self, cloneurl):
        if self.options['-C'] or yn_input('Clone into current working directory now?', default=False):
            return os.system(path.dirname(path.abspath(__file__)) + '/git-clone.sh ' + cloneurl)

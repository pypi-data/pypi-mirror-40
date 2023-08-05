'''

Copyright (C) 2019 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

import os
import re
import sys
from penrose.logger import bot
from glob import glob
from .utils import notvalid
import json


class LibraryValidator:

    def __init__(self,quiet=False):
        if quiet is True:
            bot.level = 0

    def __str__(self):
        return "expfactory.LibraryValidator"

    def validate(self, expfile):
        bot.test('EXPERIMENT: %s' % os.path.basename(expfile))
        if expfile.endswith('json'):
            if not self._validate_json(expfile):
                return False
        elif expfile.endswith('md'):
            if not self._validate_markdown(expfile):
                return False
        return True


    def _print_valid(self, result):
        options = {True:'yes', False: 'no'}
        return options[result]

    def _validate_markdown(self, expfile):
        '''ensure that fields are present in markdown file'''

        try:
            import yaml
        except:
            bot.error('Python yaml is required for testing yml/markdown files.')
            sys.exit(1)

        self.metadata = {}
        uid = os.path.basename(expfile).strip('.md')
     
        if os.path.exists(expfile):
            with open(expfile, "r") as stream:
                docs = yaml.load_all(stream)
                for doc in docs:
                    if isinstance(doc,dict):
                        for k,v in doc.items():
                            print('%s: %s' %(k,v))
                            self.metadata[k] = v
            self.metadata['uid'] = uid
       
            fields = ['github', 'preview', 'name', 'layout',
                      'tags', 'uid', 'maintainer']

            # Tests for all fields
            for field in fields:
                if field not in self.metadata:
                    return False
                if self.metadata[field] in ['',None]:
                    return False

            if 'github' not in self.metadata['github']:
                return notvalid('%s: not a valid github repository' % name)
            if not isinstance(self.metadata['tags'],list):
                return notvalid('%s: tags must be a list' % name)
            if not re.search("(\w+://)(.+@)*([\w\d\.]+)(:[\d]+){0,1}/*(.*)", self.metadata['github']):
                return notvalid('%s is not a valid URL.' %(self.metadata['github']))

        return True


    def _validate_json(self,jsonfile):
        valids = []
        valid = jsonfile.endswith('.json')
        valids.append(valid)
        bot.test("...extension json: %s" %(self._print_valid(valid))) 

        with open(jsonfile,'r') as filey:
            content = json.load(filey)
        valid = isinstance(content,dict)
        valids.append(valid)
        bot.test("...json loadable: %s" %(self._print_valid(valid)))

        if not all(valids):
            return False

        bot.test("Content:")
        name = os.path.basename(jsonfile)
        exp_id = name.replace('.json','')

        # Validate name
        if "name" not in content:
            return notvalid('"name" not found in %s' % name)

        # Library "name" corresponds to exp_id, name of repo
        if exp_id != content['name']:
            return notvalid('"name" not found in %s' % name)

        bot.test("        Name: %s" % content['name'])

        if not re.match("^[a-z0-9_-]*$", content['name']): 
            return notvalid('''invalid characters in %s, only 
                               lowercase and "-" or "_" allowed.''' %(content['name'])) 
         
        # Validate Github
        if "github" not in content:
            return notvalid('"github" not found in %s' %(name)) 
        if not re.search("(\w+://)(.+@)*([\w\d\.]+)(:[\d]+){0,1}/*(.*)",content['github']):
            return notvalid('%s is not a valid URL.' %(content['github'])) 
        if not isinstance(content["github"],str):
            return notvalid("%s must be a string" %(content['github']))
        bot.test("        Github: %s" % content['github'])

        # Maintainers
        if "maintainer" not in content:
            return notvalid('"maintainer" missing in %s' %(name)) 
        bot.test("        Maintainer: %s" % content['maintainer'])

        return True

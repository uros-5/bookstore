""" from django.test import TestCase """

# Create your tests here.

import re
sablon = re.compile(r'userInfo\[(.*)\]')
pretraga = sablon.findall('userInfo[grad]') 
if pretraga:
    exec(f'user.{pretraga[0]} = {nesto}')

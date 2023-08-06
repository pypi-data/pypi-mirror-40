# -*- coding: utf-8 -*-

import time
from gude import GudePowerStrip
from mdslogger import MdsLogger

log1 = MdsLogger('gudelog', conlogger=True, filelogger=False, loglev='debug')

# get states

ob1 = GudePowerStrip('gude1', log1.getLogObj(), 
    './epccontrol2.pl', '<ip-address>', 'password')
ob1.getStatePwrOutlet(3)

ob1.switchPwrOutlet(3, True)
time.sleep(2.0)
ob1.getStatePwrOutlet(3)

ob1.switchPwrOutlet(3, False)
time.sleep(2.0)
ob1.getStatePwrOutlet(3)


del ob1
del log1

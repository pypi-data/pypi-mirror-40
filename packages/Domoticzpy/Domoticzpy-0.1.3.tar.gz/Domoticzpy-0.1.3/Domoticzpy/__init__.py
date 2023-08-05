#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""



"""

import os

if os.environ.get('CI_COMMIT_TAG'):
    __version__ = os.environ['CI_COMMIT_TAG']
else:
    __version__ = os.environ['CI_JOB_ID']


from Domoticzpy.Domoticzpy import Domoticzpy

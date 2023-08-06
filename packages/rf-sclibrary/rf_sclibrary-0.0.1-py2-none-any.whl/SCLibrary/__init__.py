# -*- coding:utf-8 -*-

import os
from base import DynamicCore
from validator import ValidatorKeywords
from requester import RequesterKeywords
from util import UtilKeywords
from db import DBKeywords
from loglistener import LogListener
from robot.libraries.BuiltIn import BuiltIn

__version__ = '0.0.1'


class SCLibrary(DynamicCore):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        libraries = [ValidatorKeywords(), RequesterKeywords(), DBKeywords(), UtilKeywords()]
        DynamicCore.__init__(self, libraries)
        if BuiltIn().get_variable_value("${RF_DEBUG}") == True:
            self.ROBOT_LIBRARY_LISTENER = LogListener()

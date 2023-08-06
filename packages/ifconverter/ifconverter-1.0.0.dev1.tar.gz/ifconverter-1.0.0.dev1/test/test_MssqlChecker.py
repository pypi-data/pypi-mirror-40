import unittest
import unittest.mock
from unittest.mock import Mock
from Converter import mssql_checker

from model import ifconfig

class Test_MssqlChecker(unittest.TestCase):
    def setUp(self):
        ifcheck2 = ifconfig.IFCheck()
        ifcheck2.check_field = "col2"
        ifcheck2.msg = "col2 can not be null"
        ifcheck2.msg_field = "col100"
        ifchecks = []
        ifchecks.append(ifcheck2)
        self.ifchecks = ifchecks
        self.testInstance = mssql_checker.MssqlChecker(ifchecks,"#temp123")
    def test_BuildSQLStatement(self):
        
        result =  self.testInstance.BuildSQLStatement()
        print(result)
import unittest
from unittest.mock import Mock
from Converter.convert_runner import ConvertRunner


class Test_ConvertRunner(unittest.TestCase):
    
    
    def setUp(self):
        self.testInstance = ConvertRunner("test",Mock())
        self.testInstance.vcode.jobid = 'E445BDC2-969C-454D-9F17-AB10C5A09F24'
    def test_getAllConfig(self):

        self.testInstance.getAllCofig()
    def test_getIfhead(self):
        self.testInstance.getIf()
    def test_updateIfjobStatus(self):
        self.testInstance.getIf()
        self.testInstance.updateIfJobStatus(10)
    
    def test_converterrun(self):

        self.testInstance.Run()
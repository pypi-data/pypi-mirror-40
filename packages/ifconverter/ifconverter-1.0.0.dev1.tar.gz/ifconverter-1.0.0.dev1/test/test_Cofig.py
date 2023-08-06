import unittest

from Converter import config


class Testconfig(unittest.TestCase):
    
    
    def test_GetIFdef(self):
        testInstance = config.Config()
        result =  testInstance.GetIFdef('string')
        self.assertEqual(result.status_code, 200)


    def test_GetIFActHead(self):
        testInstance = config.Config()
        result =  testInstance.GetIFActHead('7')
        self.assertEqual(result.status_code, 200)

    def test_GetIFCheck(self):
        testInstance = config.Config()
        result =  testInstance.GetIFCheck('1')
        self.assertEqual(result.status_code, 200)


    def test_GetIFConvert(self):
        testInstance = config.Config()
        result =  testInstance.GetIFConvert('1')
        self.assertEqual(result.status_code, 200)

    def test_GetIFLineAlias(self):
        testInstance = config.Config()
        result =  testInstance.GetIFLineAlias('1')
        
        self.assertEqual(result.status_code, 200)

    def test_GetIFLineAliases(self):
        testInstance = config.Config()
        result =  testInstance.GetIFLineAliases('0')
        self.assertEqual(result.status_code, 200)
import unittest
import unittest.mock
from unittest.mock import Mock

from model import ifconfig
from model import ifheadmod

from Converter.mssql_converter import MsSqlConverter


class  TestMsSqlConverter(unittest.TestCase):
    
    def setUp(self):
        workConnStr = "mssql+pyodbc://sa:Netsdl123.@47.99.188.93/fitdb?driver=SQL+Server+Native+Client+11.0"
        ifConnStr = "mssql+pyodbc://sa:Netsdl123.@47.99.188.93/fitdb?driver=SQL+Server+Native+Client+11.0"
       
        ifhead = ifheadmod.IfHeadMod()
        ifhead.IfLineIndex = "If_line3"
         
        ifhead.IfHeadId = '813F5315-AFC1-43FD-A541-EA72E8BDBDE3'
        ifconvert = ifconfig.IFConvert()

        ifconvert.convert_from_fields = "itemcd,itemkey,itemName"
        ifconvert.convert_to_fields = "col001,col002,col003"
        ifconvert.join_if_fields = "itemcd,itemkey,itemName"
        ifconvert.join_to_fields = "col001,col002,col003"
        ifconvert.join_type = "left join"
        ifconvert.join_table_sql = "item_master"
        self.ifconvert =ifconvert
        self.testInstance  = MsSqlConverter(ifhead,ifconvert)
    def test_Pulldatafromifdb(self):
        ifdef = ifconfig.IFdef()
        ifdef.startLine = 0 
        ifdef.ifActId = 0
        ifdef.ifCd = 'uniqlo 商品上传'
        
        self.testInstance.pullDataIntotempIfline()

    def test_GenerateConvertFields(self):
        
        fromF = "itemcd,itemkey,itemName"
        toF = "col001,col002,col003"
        result =  self.testInstance.pairStr_WithKey(fromF,toF,"as")
        self.assertIn("itemcd as col001 , itemkey as col002 , itemName as col003", result)

    def test_joindataIntoSource(self):

        ifconvert = ifconfig.IFConvert()

        ifconvert.convert_from_fields = "itemcd,itemkey,itemName"
        ifconvert.convert_to_fields = "col001,col002,col003"
        ifconvert.join_if_fields = "itemcd,itemkey,itemName"
        ifconvert.join_to_fields = "col001,col002,col003"
        ifconvert.join_type = "left join"
        ifconvert.join_table_sql = "item_master"

        self.testInstance.joindataIntoSource(ifconvert)
    def test_prebuildJoinTableSql(self):

        ifconvert = ifconfig.IFConvert()
        ifconvert.convert_from_fields = "itemcd,itemkey,itemName"
        ifconvert.convert_to_fields = "col001,col002,col003"
        ifconvert.join_if_fields = "itemcd,itemkey,itemName"
        ifconvert.join_to_fields = "col001,col002,col003"
        ifconvert.join_type = "left join"
        ifconvert.join_table_sql = "item_master"
        # test table without rule
        result = self.testInstance.prebuildJoinTableSql(ifconvert)
        self.assertEqual(result, "item_master")
        #test table with rule
        result = self.testInstance.prebuildJoinTableSql(ifconvert,"where Status >= '0'")
        self.assertIn("where Status >= '0'", result)
        #test select sql 
        ifconvert.join_table_sql  = "select itemcd from item_master"
        result = self.testInstance.prebuildJoinTableSql(ifconvert)
        self.assertIn("(", result)
        #test sql with $Pj_id
        ifconvert.join_table_sql = "select itemcd from item_master where Pj_id = $Pj_id"
        self.testInstance.Pj_id = '82022'
        result = self.testInstance.prebuildJoinTableSql(ifconvert)
        self.assertIn('82022', result)
    def test_mergeTable(self):
        result = self.testInstance.mergeTable()
        print(result)
    
    def test_BuildExecueSqlStatement(self):
        result = self.testInstance.BuildExecueSqlStatement()
        for sql in result:
            print(sql)
import unittest
import os
import json
from jsonpath_ng import jsonpath, parse

class JSONPath(unittest.TestCase):

    def getJSONFromFile(self, jsonPath):
        
        with open(jsonPath, 'r') as myfile:
            jsonStr = myfile.read()
        
        jsonObj = json.loads(jsonStr)
        return jsonObj
        

    def test_hardcodedJSONPATH(self):
        jsonpath_expr = parse('foo[*].baz')
        match = jsonpath_expr.find({'foo': [{'baz': 1}, {'baz': 2}]})

        self.assertEqual( len(match), 2) 
        self.assertEqual(match[0].value, 1) 
        self.assertEqual(match[1].value, 2) 
    
    def test_fileJSONPATH(self):
        jsonObj = self.getJSONFromFile( "{}/tests/json/_lds-api_v3_log-sources_cpcode-products.json".format(os.getcwd()) )
        self.assertEqual( len(jsonObj), 2) 

        #global search example
        jsonpath_expr = parse('[*].id')
        match = jsonpath_expr.find(jsonObj)

        self.assertEqual( len(match), 2) 
        self.assertEqual(match[0].value, "163842") 
        self.assertEqual(match[1].value, "143296") 

        jsonpath_expr = parse('id')

        #json path on only array elements example
        for obj in jsonObj:
            match = jsonpath_expr.find(obj)
            self.assertEqual( len(match), 1) 
        
        self.assertEqual(jsonpath_expr.find(jsonObj[0])[0].value, "163842") 
        self.assertEqual(jsonpath_expr.find(jsonObj[1])[0].value, "143296")  

if __name__ == '__main__':
    unittest.main()
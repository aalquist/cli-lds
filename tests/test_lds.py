import unittest
import os
import json
from bin.lds import Lds
from bin.lds_fetch import LdsFetch
from unittest.mock import patch
from akamai.edgegrid import EdgeGridAuth, EdgeRc

class MockResponse:

    def __init__(self):
        self.status_code = None
        self.jsonObj = None

    def json(self):
        return self.jsonObj

class Lds_Test(unittest.TestCase):

    
    @patch('requests.Session')
    def testFetchCPCodeProducts(self, mockSessionObj):

        response = MockResponse()
        response.status_code = 200
        response.jsonObj = self.getJSONFromFile( "{}/tests/json/_lds-api_v3_log-sources_cpcode-products.json".format(os.getcwd()) )

        session = mockSessionObj()
        session.get.return_value = response

        #updade tests
        fetch = LdsFetch()
        edgeRc = "{}/tests/other/.dummy_edgerc".format(os.getcwd())

        (code, json) = fetch.fetchCPCodeProducts(edgeRc, None, None)        
        self.assertEqual(response.status_code, code)
        self.runGetCPCodeProducts(json)

    def testNewJsonPath(self):

        lds = Lds()
        jsonObj = self.getJSONFromFile( "{}/tests/json/_lds-api_v3_log-sources_cpcode-products.json".format(os.getcwd()) )

        result = lds.buildandParseExpression(jsonObj, "$[*].id")
        self.assertEqual(len(result ), 2)
        self.assertEqual("163842", result[0] )
        self.assertEqual("143296", result[1] )
        
        result = lds.buildandParseExpression(jsonObj[0], "$.id")
        self.assertEqual(len(result ), 1)
        self.assertEqual("163842", result[0] )
        
        result = lds.buildandParseExpression(jsonObj, "$[*][?(@.status=\"active\")].status")
        self.assertEqual(len(result ), 1)
        self.assertEqual("active", result[0] )

        result = lds.buildandParseExpression(jsonObj[0], "$[?(@.status=\"active\")].status")
        self.assertEqual(len(result ), 1)
        self.assertEqual("active", result[0] )

        result = lds.buildandParseExpression(jsonObj, "$[*].logSource.id")
        self.assertEqual(len(result ), 2)
        self.assertEqual("200957-1", result[0] )
        self.assertEqual("104523-1", result[1] )

        result = lds.buildandParseExpression(jsonObj[0], "$.logSource.id")
        self.assertEqual(len(result ), 1)
        self.assertEqual("200957-1", result[0] )
        
        result = lds.buildandParseExpression(jsonObj[1], "$.logSource.id")
        self.assertEqual(len(result ), 1)
        self.assertEqual("104523-1", result[0] )

        error = None

        

        try:
            result = lds.buildandParseExpression(jsonObj[1], ".logSource.id")
            error = True

        except ValueError as identifier:
            message = identifier.args[0]
            self.assertEqual("JSON path: .logSource.id error: line 1:0 missing '$' at '.'", message )
            
        finally:

            if(error == True):
                self.fail("buildandParseExpression() did not raise exception!")

        
        
        


    def runGetCPCodeProducts(self, jsonObj):

        lds = Lds()
        result = lds.parseCPCodeProducts(jsonObj, ["$.id"])
        self.assertEqual(len(result ), 2)
        self.assertEqual("163842", result[0][0] )
        self.assertEqual("143296", result[1][0])

        result = lds.parseCPCodeProducts(jsonObj, "$.id")
        self.assertEqual(len(result ), 2)
        self.assertEqual(result[0][0], "163842")
        self.assertEqual(result[1][0], "143296")
        
        result = lds.parseCPCodeProducts(jsonObj, ["$.id", "$._dummy1"] )
        self.assertEqual(len(result ), 0)

        result = lds.parseCPCodeProducts(jsonObj, ["$._dummy2"] )
        self.assertEqual(len(result ), 0)

        result = lds.parseCPCodeProducts(jsonObj, ["$._dummy3"] )
        self.assertEqual(len(result ), 0)


        result = lds.parseCPCodeProducts(jsonObj, "$._dummy3b" )
        self.assertEqual(len(result ), 0)

        result = lds.parseCPCodeProducts(jsonObj, ["$.id", "$._dummy4"], False )
        self.assertEqual(len(result ), 2)
        self.assertEqual(result[0][0], "163842")
        self.assertEqual(result[1][0], "143296")
        
        result = lds.parseCPCodeProducts(jsonObj, ["$.deliveryDetails"], False )
        self.assertEqual(len(result ), 2)


        result = lds.parseCPCodeProducts(jsonObj, ["$..machine"], False )
        self.assertEqual(len(result ), 1)
        self.assertEqual(result[0][0], "akainsight.upload.akamai.com")

        result = lds.parseCPCodeProducts(jsonObj, ["$.logSource.id", "$.aggregationDetails.deliveryFrequency.value", "$.status", "$.encodingDetails.encoding.value"], True )
        self.assertEqual(len(result ), 2)
        
        self.assertEqual(len(result[0] ), 4)
        self.assertEqual(result[0][0], "200957-1")
        self.assertEqual(result[0][1], "Every 24 hours")
        self.assertEqual(result[0][2], "active")
        self.assertEqual(result[0][3], "GZIP")

        self.assertEqual(len(result[1] ), 4)
        self.assertEqual(result[1][0], "104523-1")
        self.assertEqual(result[1][1], "Every 1 hour")
        self.assertEqual(result[1][2], "suspended")
        self.assertEqual(result[1][3], "GZIP & UUENCODED")
        
        result = lds.parseCPCodeProducts(jsonObj, ["$[?(@.status=\"active\")].status"], True )
        self.assertEqual(len(result ), 1)
        self.assertEqual(result[0][0], "active")

        result = lds.parseCPCodeProducts(jsonObj, ["$[?(@.status=\"active\")].status"] )
        self.assertEqual(len(result ), 1)
        self.assertEqual(result[0][0], "active")

        result = lds.parseCPCodeProducts(jsonObj, ["$[?(@.status=\"active\")].status", "$.logSource.id" ], True )
        self.assertEqual(len(result ), 1)
        self.assertEqual(result[0][0], "active")
        self.assertEqual(result[0][1], "200957-1")

        result = lds.parseCPCodeProducts(jsonObj, ["$[?(@.status=\"active\")].status", "$.logSource.id" ], False )
        self.assertEqual(len(result ), 2)
        
        self.assertEqual(len(result[0] ), 2)
        self.assertEqual(result[0][0], "active")
        self.assertEqual(result[0][1], "200957-1")

        self.assertEqual(len(result[1] ), 1)
        self.assertEqual(result[1][0], "104523-1")

    def test_runGetCPCodeProducts(self):
       
        jsonObj = self.getJSONFromFile( "{}/tests/json/_lds-api_v3_log-sources_cpcode-products.json".format(os.getcwd()) )
        self.runGetCPCodeProducts(jsonObj)
        
        

    def getJSONFromFile(self, jsonPath):
        
        with open(jsonPath, 'r') as myfile:
            jsonStr = myfile.read()
        
        jsonObj = json.loads(jsonStr)
        return jsonObj

       

if __name__ == '__main__':
    unittest.main()




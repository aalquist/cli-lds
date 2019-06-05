# Copyright 2017 Akamai Technologies, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import os
import json
import sys
from io import StringIO


from bin.query_result import QueryResult
from bin.lds_fetch import LdsFetch
from bin.lds_parse_commands import main 

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
    def testMainBootStrap(self, mockSessionObj):

        response = MockResponse()
        response.status_code = 200
        response.jsonObj = self.getJSONFromFile( "{}/bin/tests/json/_lds-api_v3_log-sources_cpcode-products.json".format(os.getcwd()) )

        session = mockSessionObj()
        session.get.return_value = response

        edgeRc = "{}/bin/tests/other/.dummy_edgerc".format(os.getcwd())

        args = [ "cpcodelist",
                "--section",
                "default",
                 "--edgerc",
                edgeRc,
                "--debug",
                "--template",
                "default.json"
                ]

        self._testParseLDSCommandCombo(args)

        file = "{}/bin/queries/lds/default.json".format(os.getcwd()) 

        args = [ "cpcodelist",
                "--section",
                "default",
                 "--edgerc",
                edgeRc,
                "--debug",
                "--file",
                file
                ]

        self._testParseLDSCommandCombo(args)

        args = [ "cpcodelist",
                "--section",
                "default",
                 "--edgerc",
                edgeRc,
                "--debug"
                
                ]

        self._testParseLDSCommandCombo(args)

    @patch('requests.Session')
    def testJsonResponse(self, mockSessionObj):

        response = MockResponse()
        response.status_code = 200
        response.jsonObj = self.getJSONFromFile( "{}/bin/tests/json/_lds-api_v3_log-sources_cpcode-products.json".format(os.getcwd()) )

        session = mockSessionObj()
        session.get.return_value = response

        edgeRc = "{}/bin/tests/other/.dummy_edgerc".format(os.getcwd())

        args = [ "cpcodelist",
                "--section",
                "default",
                 "--edgerc",
                edgeRc,
                "--show-json"
                ]

        saved_stdout = sys.stdout
        finaloutput = None

        try:
            out = StringIO()
            sys.stdout = out
            
            self.assertEqual(main(args), 0, "command args {} should return successcode".format(args) )

            output = list(out.getvalue().split("\n"))
            finaloutput = list(filter(lambda line: line != '', output))

           
            self.assertGreater(len(finaloutput), 0, "command args {} and its output should be greater than zero".format(args) )
            

            self.assertEqual(302, len(finaloutput))
            

        finally:
            pass
            sys.stdout = saved_stdout

    
   

    def _testParseLDSCommandCombo(self, args):

        saved_stdout = sys.stdout
        finaloutput = None

        try:
            out = StringIO()
            sys.stdout = out
            
            self.assertEqual(main(args), 0, "command args {} should return successcode".format(args) )

            output = list(out.getvalue().split("\n"))
            finaloutput = list(filter(lambda line: line != '', output))

           
            self.assertGreater(len(finaloutput), 0, "command args {} and its output should be greater than zero".format(args) )
            line = finaloutput[0]
            
            sys.stdout = saved_stdout
            
            self.assertIn("200957-1", line)
            self.assertIn("Every 24 hours", line)
            self.assertIn("active", line)
            self.assertIn("GZIP", line)
            
            line = finaloutput[1]
            self.assertIn("104523-1", line)
            self.assertIn("Every 1 hour", line)
            self.assertIn("suspended", line)
            self.assertIn("GZIP & UUENCODED", line)

            self.assertEqual(2, len(finaloutput))
            

        finally:
            pass
            sys.stdout = saved_stdout

        return finaloutput

    
    @patch('requests.Session')
    def testFetchCPCodeProducts(self, mockSessionObj):

        response = MockResponse()
        response.status_code = 200
        response.jsonObj = self.getJSONFromFile( "{}/bin/tests/json/_lds-api_v3_log-sources_cpcode-products.json".format(os.getcwd()) )

        session = mockSessionObj()
        session.get.return_value = response

        #updade tests
        fetch = LdsFetch()
        edgeRc = "{}/bin/tests/other/.dummy_edgerc".format(os.getcwd())

        
        (code, json) = fetch.fetchCPCodeProducts(edgerc=edgeRc, section=None, account_key=None)        
        self.assertEqual(response.status_code, code)
        self.runParseElement(json)

    def testNewJsonPath(self):

        lds = QueryResult("lds")
        jsonObj = self.getJSONFromFile( "{}/bin/tests/json/_lds-api_v3_log-sources_cpcode-products.json".format(os.getcwd()) )

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
            #enable - suppress expected error messages during tests
            saved_stdout = sys.stderr

            out = StringIO()
            sys.stderr = out

            result = lds.buildandParseExpression(jsonObj[1], ".logSource.id")
            error = True

        except ValueError as identifier:
            message = identifier.args[0]
            self.assertEqual("JSON path: .logSource.id error: line 1:0 missing '$' at '.'", message )
            
        finally:
            #rollback - suppress expected error messages during tests
            sys.stderr = saved_stdout
            if(error == True):
                self.fail("buildandParseExpression() did not raise exception!")

    def runParseElement(self, jsonObj):

        lds = QueryResult("lds")
        result = lds.parseElement(jsonObj, ["$.id"])
        self.assertEqual(len(result ), 2)
        self.assertEqual("163842", result[0][0] )
        self.assertEqual("143296", result[1][0])

        result = lds.parseElement(jsonObj, "$.id")
        self.assertEqual(len(result ), 2)
        self.assertEqual(result[0][0], "163842")
        self.assertEqual(result[1][0], "143296")
        
        result = lds.parseElement(jsonObj, ["$.id", "$._dummy1"] )
        self.assertEqual(len(result ), 0)

        result = lds.parseElement(jsonObj, ["$._dummy2"] )
        self.assertEqual(len(result ), 0)

        result = lds.parseElement(jsonObj, ["$._dummy3"] )
        self.assertEqual(len(result ), 0)


        result = lds.parseElement(jsonObj, "$._dummy3b" )
        self.assertEqual(len(result ), 0)

        result = lds.parseElement(jsonObj, ["$.id", "$._dummy4"], False )
        self.assertEqual(len(result ), 2)
        self.assertEqual(result[0][0], "163842")
        self.assertEqual(result[1][0], "143296")
        
        result = lds.parseElement(jsonObj, ["$.deliveryDetails"], False )
        self.assertEqual(len(result ), 2)


        result = lds.parseElement(jsonObj, ["$..machine"], False )
        self.assertEqual(len(result ), 1)
        self.assertEqual(result[0][0], "akainsight.upload.akamai.com")

        result = lds.parseElement(jsonObj, ["$.logSource.id", "$.aggregationDetails.deliveryFrequency.value", "$.status", "$.encodingDetails.encoding.value"], True )
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
        
        result = lds.parseElement(jsonObj, ["$[?(@.status=\"active\")].status"], True )
        self.assertEqual(len(result ), 1)
        self.assertEqual(result[0][0], "active")

        result = lds.parseElement(jsonObj, ["$[?(@.status=\"active\")].status"] )
        self.assertEqual(len(result ), 1)
        self.assertEqual(result[0][0], "active")

        result = lds.parseElement(jsonObj, ["$[?(@.status=\"active\")].status", "$.logSource.id" ], True )
        self.assertEqual(len(result ), 1)
        self.assertEqual(result[0][0], "active")
        self.assertEqual(result[0][1], "200957-1")

        result = lds.parseElement(jsonObj, ["$[?(@.status=\"active\")].status", "$.logSource.id" ], False )
        self.assertEqual(len(result ), 2)
        
        self.assertEqual(len(result[0] ), 2)
        self.assertEqual(result[0][0], "active")
        self.assertEqual(result[0][1], "200957-1")

        self.assertEqual(len(result[1] ), 1)
        self.assertEqual(result[1][0], "104523-1")

    def testParseCommandDefault(self):
        lds = QueryResult("lds")

        jsonObj = self.getJSONFromFile( "{}/bin/tests/json/_lds-api_v3_log-sources_cpcode-products.json".format(os.getcwd()) )
        result = lds.parseCommandDefault(jsonObj)
        
        self.assertEqual(len(result ), 2)
        self.assertEqual(len(result[0] ), 4)

        r1 = result[0]
        r1.sort()

        self.assertEqual(r1[0], "200957-1")
        self.assertEqual(r1[1], "Every 24 hours")
        self.assertEqual(r1[2], "GZIP") 
        self.assertEqual(r1[3], "active")

        self.assertEqual(len(result[1] ), 4)

        r2 = result[1]
        r2.sort()

        self.assertEqual(r2[0], "104523-1")
        self.assertEqual(r2[1], "Every 1 hour")
        self.assertEqual(r2[2], "GZIP & UUENCODED")
        self.assertEqual(r2[3], "suspended")

    def testNetStorageParseCommandDefault(self):
        lds = QueryResult("netstorage")

        jsonObj = self.getJSONFromFile( "{}/bin/tests/json/_storage_v1_storage-groups.json".format(os.getcwd()) )

        jsonObj = jsonObj["items"]

        result = lds.parseCommandDefault(jsonObj, True)
        r1 = result[0]

        self.assertEqual(r1[0], "5-555V556")
        self.assertEqual(r1[1], "aka_storage")
        self.assertEqual(r1[2], "akastorage")
        self.assertEqual(r1[3], 0)
        self.assertEqual(r1[4], "carndt")
        self.assertEqual(r1[5], "456789,456790") 


    def test_runGetCPCodeProducts(self):
       
        jsonObj = self.getJSONFromFile( "{}/bin/tests/json/_lds-api_v3_log-sources_cpcode-products.json".format(os.getcwd()) )
        self.runParseElement(jsonObj)
        
        

    def getJSONFromFile(self, jsonPath):
        
        with open(jsonPath, 'r') as myfile:
            jsonStr = myfile.read()
        
        jsonObj = json.loads(jsonStr)
        return jsonObj

       

if __name__ == '__main__':
    unittest.main()




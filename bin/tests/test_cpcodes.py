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

from bin.fetch_cpcodes import CPCODEFetch


from unittest.mock import patch
from akamai.edgegrid import EdgeGridAuth, EdgeRc

class MockResponse:

    def __init__(self):
        self.status_code = None
        self.jsonObj = []
        

    def appendResponse(self, obj):
        self.jsonObj.insert(0,obj)

    def json(self):

        if self.json is not None and len(self.jsonObj) > 0:
            return self.jsonObj.pop()
        else :
            raise Exception("no more mock responses")

        return self.jsonObj


class CPCODE_Test(unittest.TestCase):

    @patch('requests.Session')
    def testFetchGroupCPCODES(self, mockSessionObj):

        response = MockResponse()
        response.status_code = 200
        response.appendResponse( self.getJSONFromFile( "{}/bin/tests/json/_papi_v1_groups.json".format(os.getcwd()) ) )
        response.appendResponse( self.getJSONFromFile( "{}/bin/tests/json/_papi_v1_cpcodes__ctr_1-1TJZFW_grp_41445.json".format(os.getcwd()) ) )
        response.appendResponse( self.getJSONFromFile( "{}/bin/tests/json/_papi_v1_cpcodes__ctr_1-1TJZFW_grp_41444.json".format(os.getcwd()) ) )
        response.appendResponse( self.getJSONFromFile( "{}/bin/tests/json/_papi_v1_cpcodes__ctr_1-1TJZFW_grp_41443.json".format(os.getcwd()) ) )
        
        session = mockSessionObj()
        session.get.return_value = response

        edgeRc = "{}/bin/tests/other/.dummy_edgerc".format(os.getcwd())

        fetch = CPCODEFetch()
        (code, json) = fetch.fetchGroupCPCODES(edgerc = edgeRc, section="default", account_key=None, debug=False)

        self.assertEqual(code, 200)
        self.assertEqual(len(json), 3)

        self.assertEqual(json[0]["cpcodes"][0]["cpcodeId"], "cpc_33192")
        self.assertEqual(json[0]["cpcodes"][0]["cpcodeName"], "SME WAA")

        self.assertEqual(json[1]["cpcodes"][0]["cpcodeId"], "cpc_33191")
        self.assertEqual(json[1]["cpcodes"][0]["cpcodeName"], "SME WAA")

        self.assertEqual(json[2]["cpcodes"][0]["cpcodeId"], "cpc_33190")
        self.assertEqual(json[2]["cpcodes"][0]["cpcodeName"], "SME WAA")

        
    
    
    def getJSONFromFile(self, jsonPath):
            
            with open(jsonPath, 'r') as myfile:
                jsonStr = myfile.read()
            
            jsonObj = json.loads(jsonStr)
            return jsonObj

       

if __name__ == '__main__':
    unittest.main()




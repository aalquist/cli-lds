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

import sys
import yaml
import os

#seems to be the most reliable jsonpath parser https://github.com/pacifica/python-jsonpath2 
from jsonpath2.path import Path


class Lds():

    def buildParseExp(self, paths):
        
        try:
            expr = Path.parse_str(paths)
            return expr

        except Exception as identifier:
            raise ValueError("JSON path: {} error: {}".format(paths, identifier))

    
    def parseExp(self, json, expression):
        data = list(map(lambda match_data : match_data.current_value, expression.match( json ) ) )
        return data

    def buildandParseExpression(self, json, paths):
        expr = self.buildParseExp(paths)
        data = self.parseExp(json, expr)
        return data
    
    def parseFileQuery(self, queryfile):
        with open(queryfile) as f:
            read_data = f.read()
            ydata = yaml.load(read_data, Loader = yaml.FullLoader)
            return ydata

    def parseDefaultFileQuery(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        query_yaml = os.path.join(dir_path, "queries", "default.yaml")
        return self.parseFileQuery(query_yaml)
        
    def parseDefault(self, json):
        defaultquery = self.parseDefaultFileQuery()
        queries = list(defaultquery.values() )
        result = self.parseCPCodeProducts(json, queries, True )
        return result

    def parseCPCodeProducts(self, json, paths, RequireAll = True):
        
        returnList = []

        jsonExpressions = []
        
        if(isinstance(paths,str) and paths is not None):
            path = self.buildParseExp(paths)
            jsonExpressions.append(path)

        else: 

            for p in paths:

                path = self.buildParseExp(p)
                jsonExpressions.append(path)
                
        #json path on only array elements example
        for obj in json:

            #for each lds config search path
            allMatched = True
            
            matchedArray = []

            for jsonpath_expr in jsonExpressions:
                
                #match = jsonpath_expr.find(obj)
                match = self.parseExp(obj, jsonpath_expr)

                if(len(match) == 0):
                    allMatched = False

                #for each result add to return list
                
                for m in match:
                    matchedArray.append(m)

            if RequireAll == False or allMatched == True:

                if(len(matchedArray) > 0):
                    returnList.append(matchedArray)

        return returnList

    
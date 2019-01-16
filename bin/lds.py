import sys

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
    
    def parseStandard(self, json):
        result = self.parseCPCodeProducts(json, ["$.logSource.id", "$.aggregationDetails.deliveryFrequency.value", "$.status", "$.encodingDetails.encoding.value"], True )
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

    
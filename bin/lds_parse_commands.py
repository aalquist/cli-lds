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

import argparse
import sys
import os
import json

from bin.fetch_lds import LdsFetch
from bin.fetch_netstorage import NetStorageFetch
from bin.query_result import QueryResult

import json

PACKAGE_VERSION = "0.0.1"

class MyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(0, '%s: error: %s\n' % (self.prog, message))

def get_prog_name():
    prog = os.path.basename(sys.argv[0])
    if os.getenv("AKAMAI_CLI"):
        prog = "akamai query"
    return prog

def create_sub_command( subparsers, name, help, *, optional_arguments=None, required_arguments=None, actions=None):

    action = subparsers.add_parser(name=name, help=help, add_help=False)

    if required_arguments:
        required = action.add_argument_group("required arguments")
        for arg in required_arguments:
            name = arg["name"]
            del arg["name"]
            required.add_argument("--" + name,
                                  required=True,
                                  **arg)

    optional = action.add_argument_group("optional arguments")

    if optional_arguments:

        for arg in optional_arguments:
            name = arg["name"]
            del arg["name"]

            if name.startswith("use-") or name.startswith("show-") or name.startswith("for-"):
                optional.add_argument(
                    "--" + name,
                    required=False,
                    **arg,
                    action="store_true")
            else:
                optional.add_argument("--" + name,
                                      required=False,
                                      **arg)

    optional.add_argument(
        "--edgerc",
        help="Location of the credentials file [$AKAMAI_EDGERC]",
        default=os.path.join(os.path.expanduser("~"), '.edgerc'))

    optional.add_argument(
        "--section",
        help="Section of the credentials file [$AKAMAI_EDGERC_SECTION]",
        default="lds")

    optional.add_argument(
        "--debug",
        help="DEBUG mode to generate additional logs for troubleshooting",
        action="store_true")

    optional.add_argument(
        "--account-key",
        help="Account Switch Key",
        default="")

    actions[name] = action

    #return action

def main(mainArgs=None):

    prog = get_prog_name()
    if len(sys.argv) == 1:
        prog += " [command]"

    parser = MyArgumentParser(
            description='Akamai LDS CLI',
            add_help=False,
            prog=prog
    )

    parser.add_argument('--version', action='version', version='%(prog)s ' + PACKAGE_VERSION)

    subparsers = parser.add_subparsers(help='commands', dest="command")

    actions = {}

    subparsers.add_parser(
        name="help",
        help="Show available help",
        add_help=False).add_argument( 'args', metavar="", nargs=argparse.REMAINDER)

    create_sub_command(
        subparsers, "cpcodelist", "List all cpcode based log delivery configurations",
        optional_arguments=[ 
                            {"name": "show-json", "help": "output json"},
                            {"name": "use-stdin", "help": "use stdin for query"},
                            {"name": "file", "help": "the json file for query"},
                            {"name": "template", "help": "use template name for query"} ],
        required_arguments=None,
        actions=actions)

    create_sub_command(
        subparsers, "template", "prints the default yaml query template",
        optional_arguments=[  {"name": "get", "help": "get template by name"}],
        required_arguments=None,
        actions=actions)
    
    create_sub_command(
        subparsers, "netstoragelist", "List netstroage information",
        optional_arguments=[ 
                            {"name": "show-json", "help": "output json"},
                            {"name": "use-stdin", "help": "use stdin for query"},
                            {"name": "file", "help": "the json file for query"},
                            {"name": "template", "help": "use template name for query"} ],
        required_arguments=None,
        actions=actions)
    

    args = None
    


    if mainArgs is None: 
        print("no arguments were provided", file=sys.stderr)
        parser.print_help(sys.stderr)
        return 1

    elif isinstance(mainArgs, list) and len(mainArgs) <= 0: 
        print("no arguments were provided and empty", file=sys.stderr)
        parser.print_help(sys.stderr)
        return 1

    else:
        args = parser.parse_args(mainArgs)

    if args.command == "help":

        if len(args.args) > 0:
            helparg = args.args[0]
            
            if helparg in actions and actions[helparg]:
                actions[helparg].print_help()
            else:
                parser.print_help(sys.stderr)
                return 1
        else:
            parser.prog = get_prog_name() + " help [command]"
            parser.print_help()
            
        return 0

    try:
        return getattr(sys.modules[__name__], args.command.replace("-", "_"))(args)

    except Exception as e:
        print(e, file=sys.stderr)
        return 1


def template(args):
    lds = QueryResult("lds")

    if args.get is None:
        obj = lds.listQuery()
    else:

        obj = lds.getQuerybyName(args.get)
        

    print( json.dumps(obj,indent=1) )
    return 0



def cpcodelist(args):

    fetch = LdsFetch()
    lds = QueryResult("lds")

    (_ , jsonObj) = fetch.fetchCPCodeProducts(edgerc = args.edgerc, section=args.section, account_key=args.account_key, debug=args.debug)  

    if not args.show_json:

        if args.use_stdin :
            
            inputString = getArgFromSTDIN()
            parsed = loadInput(lds, inputString, jsonObj)

        elif args.file is not None :
            
            inputString = getArgFromFile(args.file)
            parsed = loadInput(lds, inputString, jsonObj)

        elif args.template is not None :

            templateJson = lds.getQuerybyName(args.template)
            parsed = lds.parseCommandGeneric(jsonObj, templateJson)

        else:
            
            parsed = lds.parseCommandDefault(jsonObj)

    
        for line in parsed:
            print( json.dumps(line) )

    else: 
        print( json.dumps( jsonObj, indent=1 ) )


    return 0

def netstoragelist(args):

    fetch = NetStorageFetch()
    lds = QueryResult("netstorage")
    
    (_ , jsonObj) = fetch.fetchNetStorageGroups(edgerc = args.edgerc, section=args.section, account_key=args.account_key, debug=args.debug)  

    if not args.show_json:

        if args.use_stdin :
            
            inputString = getArgFromSTDIN() 
            parsed = loadInput(lds, inputString, jsonObj) 

        elif args.file is not None :
            
            yaml = getArgFromFile(args.file)
            yamlObj = lds.loadJson(yaml)
            parsed = lds.parseCommandGeneric(jsonObj , yamlObj)

        elif args.template is not None :

            templateJson = lds.getQuerybyName(args.template)
            parsed = lds.parseCommandGeneric(jsonObj, templateJson)

        else:

            parsed = lds.parseCommandDefault(jsonObj) 

        for line in parsed: 
            print( json.dumps(line) ) 



    else: 
        print( json.dumps( jsonObj, indent=1 ) )


    return 0


def loadInput(lds, inputString, jsonObj):
    templateJson = lds.loadJson(inputString)
    parsed = lds.parseCommandGeneric(jsonObj , templateJson)
    return parsed

def argFromInput(arg):

    with open(arg, 'r') as myfile:
            jsonStr = myfile.read()
        
    return jsonStr

def getArgFromSTDIN():
    return argFromInput(0)

def getArgFromFile(jsonPath):
    return argFromInput(jsonPath)

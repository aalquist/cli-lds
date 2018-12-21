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

class MyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(0, '%s: error: %s\n' % (self.prog, message))

def main():

    parser = MyArgumentParser(
            description='Akamai LDS CLI',
    )

    subparsers = parser.add_subparsers(help='commands', dest="command")

    create_parser = subparsers.add_parser("help", help="Show available help")
    create_parser = subparsers.add_parser("list", help="Subcommands")
    create_parser = subparsers.add_parser("hello", help="A cheerful greeting")
    create_parser.add_argument("name", nargs='?', default='World')
    
    opts = parser.parse_args()

    if opts.command == "help":
        parser.print_help()

    elif opts.command == "list":
        print("doing list")
        
    elif opts.command == "hello":
        print("doing hello")
        print ("Hello %s" % opts.name)

    else:
        # argparse will error on unexpected commands, but
        # in case we mistype one of the elif statements...
        parser.print_help(sys.stderr)



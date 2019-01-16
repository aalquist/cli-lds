import os
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import requests
import configparser
import sys
import collections 

class CredentialFactory():

    def buildContext(self, base_url, account_switch_key, session):
        
        key = ''
        if account_switch_key != '' and account_switch_key is not None:
            key = 'accountSwitchKey=' + account_switch_key
    
        credentials = collections.namedtuple('Credentials',['base_url', 'account_key', 'session']) 
        return credentials(base_url, key, session) 

    def load(self, edgerc_file, section, account_key):

        if not edgerc_file:
            if not os.getenv("AKAMAI_EDGERC"):
                edgerc_file = os.path.join(os.path.expanduser("~"), '.edgerc')
            else:
                edgerc_file = os.getenv("AKAMAI_EDGERC")

        if not os.access(edgerc_file, os.R_OK):
            raise ValueError("Unable to read edgerc file {}".format(edgerc_file ))

        if not section:
            if not os.getenv("AKAMAI_EDGERC_SECTION"):
                section = "default"
            else:
                section = os.getenv("AKAMAI_EDGERC_SECTION")

        try:
            edgerc = EdgeRc(edgerc_file)
            base_url = edgerc.get(section, 'host')

            session = requests.Session()
            session.auth = EdgeGridAuth.from_edgerc(edgerc, section)
            context = self.buildContext(base_url, account_key, session)
            return context

        except configparser.NoSectionError:
            raise ValueError("Edgerc section {} not found".format(section) )

        except Exception:
            raise ValueError("Unknown error occurred trying to read edgerc file {}".format(edgerc_file) )


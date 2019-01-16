import os
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import requests
import configparser
import sys

try:
    from credentialfactory import CredentialFactory
    
except ModuleNotFoundError:
    #supports unit tests
    from bin.credentialfactory import CredentialFactory

class LdsFetch():

    def makeSwitchUrl(self, url, account_switch_key):
        
        if '?' in url:
            url = "{}&{}".format(url,account_switch_key)
        

    def fetchCPCodeProducts(self, edgerc_file, section, account_key):

        factory = CredentialFactory()
        context = factory.load(edgerc_file, section, account_key)
        
        url = "https://{}/lds-api/v3/log-sources/cpcode-products/log-configurations".format(context.base_url)

        result = context.session.get(url)
        status_code = result.status_code

        if status_code in [200]:
            lds_json = result.json()
            return (status_code, lds_json)
        else: 
            raise Exception("Unexpected Reponse Code:{} for /lds-api/v3/log-sources/cpcode-products/log-configurations".format(status_code)  )
        
        

if __name__ == '__main__':
    
    fetch = LdsFetch()
    fetch.fetchCPCodeProducts(None, "p-lds", None)        
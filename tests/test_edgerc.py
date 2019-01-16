import unittest
import os
from bin.credentialfactory import CredentialFactory

class EdgeRCTest(unittest.TestCase):


    def test_load(self):
        factory = CredentialFactory()
        edgeRc = "{}/tests/other/.dummy_edgerc".format(os.getcwd())

        context = factory.load(edgeRc, "other", None)
        self.assertEqual("akab-MjIzMTE5ODM5NTQ1MGRkNTczNmIyZjk0.luna.akamaiapis.net", context.base_url )
        self.assertEqual("", context.account_key )
        self.assertIsNotNone(context.session)

        context = factory.load(edgeRc, None, None)
        self.assertEqual("akab-DjIzMTE5ODM5NTQ1MGRkNTczNmIyZjk0.luna.akamaiapis.net", context.base_url )
        self.assertEqual("", context.account_key )
        self.assertIsNotNone(context.session)

        context = factory.load(edgeRc, "default", None)
        self.assertEqual("akab-DjIzMTE5ODM5NTQ1MGRkNTczNmIyZjk0.luna.akamaiapis.net", context.base_url )
        self.assertEqual("", context.account_key )
        self.assertIsNotNone(context.session)

        context = factory.load(edgeRc, "other", "someKey")
        self.assertEqual("akab-MjIzMTE5ODM5NTQ1MGRkNTczNmIyZjk0.luna.akamaiapis.net", context.base_url )
        self.assertEqual("accountSwitchKey=someKey", context.account_key )
        self.assertIsNotNone(context.session)

        error = False
        try:
            context = factory.load(edgeRc, "missingSection", None)
            
        except ValueError:
            error = True
        
        self.assertTrue(error)

if __name__ == '__main__':
    unittest.main()
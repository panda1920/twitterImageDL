from pathlib import Path
import shutil
import sys
import os

import pytest
    
PROJECT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_DIR / 'src'

sys.path.append(str( SRC_DIR ))

from twitterAPIAuthentication import createOAuth1HeaderString, createSignature, createSignatureBaseString, createAuthInfo

@pytest.fixture(scope='function')
def setupTestEnviron():
    os.environ['CONSUMER_KEY'] = 'xvz1evFS4wEEPTGEFPHBog'
    os.environ['CONSUMER_SECRET'] = 'kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw'
    os.environ['ACCESS_TOKEN'] = '370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb'
    os.environ['ACCESS_SECRET'] = 'LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE'

class TestOauth1:
    testURLEndpoint = 'https://api.twitter.com/1.1/statuses/update.json'
    testHTTPMethod = 'POST'
    testQueryString = { 'include_entities': 'true' }
    testRequestBody = { 'status': 'Hello Ladies + Gentlemen, a signed OAuth request!' }

    def createDummyAuthInfo(self):
        authInfo = createAuthInfo()
        authInfo['oauth_nonce'] = 'kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg'
        authInfo['oauth_timestamp'] = '1318622958'

        return authInfo

    def test_createSignatureBaseString(self, setupTestEnviron):
        signatureBaseString = createSignatureBaseString(
            self.testURLEndpoint,
            self.testHTTPMethod,
            self.testQueryString,
            self.testRequestBody,
            self.createDummyAuthInfo()
        )
        referenceSignatureBaseString = r'POST&https%3A%2F%2Fapi.twitter.com%2F1.1%2Fstatuses%2Fupdate.json&include_entities%3Dtrue%26oauth_consumer_key%3Dxvz1evFS4wEEPTGEFPHBog%26oauth_nonce%3DkYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1318622958%26oauth_token%3D370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb%26oauth_version%3D1.0%26status%3DHello%2520Ladies%2520%252B%2520Gentlemen%252C%2520a%2520signed%2520OAuth%2520request%2521'
        assert signatureBaseString == referenceSignatureBaseString

    def test_createSignature(self, setupTestEnviron):
        signature = createSignature(
            self.testURLEndpoint,
            self.testHTTPMethod,
            self.testQueryString,
            self.testRequestBody,
            self.createDummyAuthInfo(),
        )
        referenceSignature = 'hCtSmYh+iHYCEqBWrE7C7hYmtUk='
        assert signature == referenceSignature

    def test_createOauth1HeaderString(self, setupTestEnviron):
        headerString = createOAuth1HeaderString(
            self.testURLEndpoint,
            self.testHTTPMethod,
            self.testQueryString,
            self.testRequestBody,
            self.createDummyAuthInfo(),
        )
        referenceHeaderString = r'OAuth oauth_consumer_key="xvz1evFS4wEEPTGEFPHBog", oauth_nonce="kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg", oauth_signature="hCtSmYh%2BiHYCEqBWrE7C7hYmtUk%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1318622958", oauth_token="370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb", oauth_version="1.0"'
        assert headerString == referenceHeaderString
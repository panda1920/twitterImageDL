import os
import uuid
import time
import math
import urllib.parse

def createAuthInfo():
    consumerKey = os.environ.get('CONSUMER_KEY', None)
    accessToken = os.environ.get('ACCESS_TOKEN', None)
    nonce = uuid.uuid4().hex
    requestTime = str( math.floor(time.time()) )
    
    return {
        'oauth_consumer_key': consumerKey,
        'oauth_nonce': nonce,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': requestTime,
        'oauth_token': accessToken,
        'oauth_version': '1.0',
    }

def createOAuth1HeadereString(endpointUrl, method, queryString, body, authInfo):
    authInfo['oauth_signature'] = createSignature(endpointUrl, method, queryString, body, authInfo)

    headerString = 'OAuth '
    for key, value in sorted(authInfo.items()):
        headerString += f'{quote(key)}="{quote(value)}", '

    return headerString[:-2]

def createSignature(endpointUrl, method, queryString, body, authInfo):
    from hashlib import sha1
    import hmac
    import base64

    signatureString = createSignatureBaseString(endpointUrl, method, queryString, body, authInfo)
    key = createSigningKey()
    hashed = hmac.new(key.encode('utf-8'), signatureString.encode('utf-8'), sha1)

    return base64.encodebytes(hashed.digest()).decode('utf-8').rstrip('\n')

def createSignatureBaseString(endpointUrl, method, queryString, body, authInfo):
    params = {}
    params.update(queryString)
    params.update(body)
    params.update(authInfo)

    parameterString = createParameterString(params)

    return f'{method}&{quote(endpointUrl)}&{quote(parameterString)}'

def quote(string):
    return urllib.parse.quote(string, safe='')

def createParameterString(params):
    quotedParams = {
        quote(key): quote(value)
        for key, value in params.items()
    }
    paramString = ''
    for key, value in sorted(quotedParams.items()):
        paramString += f'{key}={value}&'

    return paramString[:-1]

def createSigningKey():
    consumerSecret = os.environ.get('CONSUMER_SECRET', None)
    accessSecret = os.environ.get('ACCESS_SECRET', None)
    return f'{quote(consumerSecret)}&{accessSecret}'
import os
import uuid
import time
import math
import urllib.parse

import twitter_image_dl.global_constants as constants

def createAuthInfo(settings):
    consumerKey = settings.get()[constants.API_SECTION][constants.CONSUMER_KEY]
    accessToken = settings.get()[constants.API_SECTION][constants.ACCESS_TOKEN]
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

def createOAuth1HeaderString(endpointUrl, method, queryString, body, authInfo, settings):
    authInfo['oauth_signature'] = createSignature(
        createSignatureBaseString(endpointUrl, method, queryString, body, authInfo),
        settings
    )

    headerString = 'OAuth '
    for key, value in sorted(authInfo.items()):
        headerString += f'{quote(key)}="{quote(value)}", '

    return headerString[:-2]

def createSignature(signatureBaseString, settings):
    from hashlib import sha1
    import hmac
    import base64

    key = createSigningKey(settings)
    hashed = hmac.new(key.encode('utf-8'), signatureBaseString.encode('utf-8'), sha1)

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

    return paramString[:-1] # remove last '&'

def createSigningKey(settings):
    consumerSecret = settings.get()[constants.API_SECTION][constants.CONSUMER_SECRET]
    accessSecret = settings.get()[constants.API_SECTION][constants.ACCESS_SECRET]
    return f'{quote(consumerSecret)}&{accessSecret}'

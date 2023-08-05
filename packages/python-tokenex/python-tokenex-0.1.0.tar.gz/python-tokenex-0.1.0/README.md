## TokenEx Python Module

[![Build Status](https://travis-ci.org/tablethotels/python-tokenex.svg?branch=master)](https://travis-ci.org/tablethotels/python-tokenex)
[![Coverage Status](https://coveralls.io/repos/github/tablethotels/python-tokenex/badge.svg?branch=master)](https://coveralls.io/github/tablethotels/python-tokenex?branch=master)

A Python Module for interacting with TokenEx tokenization services

TokenEx Website:  https://tokenex.com  
TokenEx documentation: https://docs.tokenex.com

### Installation

    pip install python-tokenex

### CLI

This module provides a CLI for interacting with TokenEx at the command 
line.  TokenEx ID, API Key, and Token Scheme can be passed in thru command arguments
or Environment Variables TOKENEX_USER_ID, TOKENEX_API_KEY, and TOKENEX_SCHEME
respectively.  Enabling the -t option will point your command to the 
TokenEx test api.

    usage: tokenex [-h]
               [-s {nTOKEN,sixNTOKENfour,sixASCIITOKENfour,sixANTOKENfour,GUID,nGUID,sixTOKENfour,nTOKENfour,fourTOKENfour,fourASCIITOKENfour,TOKENfourNonLuhn,sixTOKENfourNonLuhn,ASCIITOKEN,SSN,ANTOKENAUTO,fourTOKENfourNonLuhn,fourANTOKENfour,TOKEN,ANTOKEN,TOKENfour,ASCIITOKENAUTO,NTOKENAUTO,ASCIITOKENfour,fourNTOKENfour,ANTOKENfour}]
               [-k API_KEY] [-u USER_ID] [-t]
               {detokenize,transparent_detokenize,tokenize,tokenize_encrypted,validate,delete}
               value

    positional arguments:
      {detokenize,transparent_detokenize,tokenize,tokenize_encrypted,validate,delete}
                            Command to run
      value                 Command Input Value
    
    optional arguments:
      -h, --help            show this help message and exit
      -s {nTOKEN,sixNTOKENfour,sixASCIITOKENfour,sixANTOKENfour,GUID,nGUID,sixTOKENfour,nTOKENfour,fourTOKENfour,fourASCIITOKENfour,TOKENfourNonLuhn,sixTOKENfourNonLuhn,ASCIITOKEN,SSN,ANTOKENAUTO,fourTOKENfourNonLuhn,fourANTOKENfour,TOKEN,ANTOKEN,TOKENfour,ASCIITOKENAUTO,NTOKENAUTO,ASCIITOKENfour,fourNTOKENfour,ANTOKENfour}, --token-scheme {nTOKEN,sixNTOKENfour,sixASCIITOKENfour,sixANTOKENfour,GUID,nGUID,sixTOKENfour,nTOKENfour,fourTOKENfour,fourASCIITOKENfour,TOKENfourNonLuhn,sixTOKENfourNonLuhn,ASCIITOKEN,SSN,ANTOKENAUTO,fourTOKENfourNonLuhn,fourANTOKENfour,TOKEN,ANTOKEN,TOKENfour,ASCIITOKENAUTO,NTOKENAUTO,ASCIITOKENfour,fourNTOKENfour,ANTOKENfour}
                            Tokenization Scheme
      -k API_KEY, --api-key API_KEY
                            TokenEx API Key
      -u USER_ID, --user-id USER_ID
                            TokenEx User ID
      -t, --test-mode       Enable Testing Mode

### TokenEx Module

The CLI uses an underlying TokenEx Python module to perform its operations, and this module
is designed to be directly imported into your application.

#### _tokenex.TokenExRequest(tokenex_id, api_key, token_scheme_name="nTOKENfour", requests_options=None, tokenex_test_mode=False)_

This Object represents a TokenEx Request, or more specifically a connection to perform multiple 
requests with.  It heavily relies on the Python Requests module.

* _**tokenex_id**_  
Your TokenEx Customer ID

* _**api_key**_  
Your TokenEx API Key

* _**token_scheme_name**_  
TokenEx Tokenization Scheme Name (https://docs.tokenex.com/?page=appendix#token-schemes)

* _**requests_options**_  
Any standard Requests options that you would like to add to the API call

* _**tokenex_test_mode**_  
If True, points your API call to the TokenEx testing environment

##### _Methods_

All methods return a tokenex.TokenExResponse object

* tokenize(value)  
Tokenizes a string value

* detokenize(token)
Detokenizes an existing token

* tokenize_encrypted(enc_value)
Tokenizes a browser-encrypted string

* validate(token)
Validates an existing token

* delete(token)
Deletes existing token

* transparent_detokenize(data, destination, method='POST', bypass=False)
Sends a request thru the TokenEx Transparent Gateway API (https://docs.tokenex.com/?page=tgapi#)

    * _data_ - The POST data to be sent thru the gateway.  This can be form or json data, with the 
    appropriate Content-type set in the requests_options of the TokenExRequest object
    
    * _destination_ - The full URI you wish to send your request to
    
    * _method_ - Request method.  Currently the only supported method is POST
    
    * _bypass_ - If True, bypass the Transparent API and send directly to destination.  This option
    can be useful for conditional requests where you do not want to send a token, since the API
    will error if no token is present in the request.
    
#### _tokenex.TokenExResponse(requests_response):_

A Requests-inspired response object, returned by TokenExRequest methods

* TokenExResponse.status_code - Status code of the response
* TokenExResponse.text - The text output of the response body
* TokenExResponse.content - The binary content of the response body
* TokenExResponse.json - Dictionary representation of JSON response body
* TokenExResponse.encoding - The encoding of the response
* TokenExResponse.headers - The response headers
* TokenExResponse.raise_for_status() - Raises exception for unsuccessful status_code

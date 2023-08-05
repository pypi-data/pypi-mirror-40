from __future__ import absolute_import, print_function, unicode_literals

import copy
try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

import requests


class TokenExException(Exception):
    """
    Exception for TokenEx Errors
    """

    def __init__(self, error):
        super(TokenExException, self).__init__()
        self.error = error
        self.error_code = error.get('Code')
        self.message = error.get('Message')
        self.reference_number = error.get('RefNumber')

    def __str__(self):
        return str(self.error)


class TokenExRequest(object):
    """Object with methods for interacting with TokenEx APIs"""

    # Base TokenEx URL
    BASE_URL = "api.tokenex.com/TokenServices.svc/REST"

    # Base TokenEx Transparent Gateway URL
    BASE_TRANSPARENT_URL = "api.tokenex.com/TransparentGatewayAPI"

    # Command map to set method parameters by configuration
    COMMAND_MAP = {
        "tokenize": {
            "url": BASE_URL,
            "url_suffix": "Tokenize"
        },
        "detokenize": {
            "url": BASE_URL,
            "url_suffix": "Detokenize"
        },
        "tokenize_encrypted": {
            "url": BASE_URL,
            "url_suffix": "TokenizeFromEncryptedValue"
        },
        "validate": {
            "url": BASE_URL,
            "url_suffix": "ValidateToken"
        },
        "delete": {
            "url": BASE_URL,
            "url_suffix": "DeleteToken"
        },
        "transparent_detokenize": {
            "url": BASE_TRANSPARENT_URL,
            "url_suffix": "Detokenize"
        }
    }

    # Possible Token Schemes https://docs.tokenex.com/?page=appendix#token-schemes
    TOKEN_SCHEMES = {
        "sixTOKENfour": 1,
        "fourTOKENfour": 2,
        "TOKENfour": 3,
        "GUID": 4,
        "SSN": 5,
        "nGUID": 6,
        "nTOKENfour": 7,
        "nTOKEN": 8,
        "sixANTOKENfour": 9,
        "fourANTOKENfour": 10,
        "ANTOKENfour": 11,
        "ANTOKEN": 12,
        "ANTOKENAUTO": 13,
        "sixASCIITOKENfour": 16,
        "fourASCIITOKENfour": 17,
        "ASCIITOKENfour": 14,
        "ASCIITOKEN": 15,
        "ASCIITOKENAUTO": 18,
        "sixNTOKENfour": 19,
        "fourNTOKENfour": 20,
        "NTOKENAUTO": 21,
        "TOKEN": 22,
        "sixTOKENfourNonLuhn": 23,
        "fourTOKENfourNonLuhn": 24,
        "TOKENfourNonLuhn": 25,
    }

    # Default headers for all transactions, unless overwritten by requests_options param
    DEFAULT_HEADERS = {
        "Accept": "application/json"
    }

    def __init__(self, tokenex_id, api_key, token_scheme_name="nTOKENfour",
                 requests_options=None, tokenex_test_mode=False):
        """Instantiate class"""

        self.api_key = api_key
        self.tokenex_id = tokenex_id
        self.token_scheme_name = token_scheme_name
        self.requests_options = requests_options if requests_options else {}
        self.tokenex_test_mode = tokenex_test_mode

        self.action = None
        self.response = None

    @property
    def tokenex_url(self):
        """Generate tokenex url for the request related to each method"""
        prefix = 'test-' if self.tokenex_test_mode else ''
        suffix = self.COMMAND_MAP[self.action]['url_suffix']
        url = self.COMMAND_MAP[self.action]['url']
        return "https://{0}{1}/{2}".format(prefix, url, suffix)

    @property
    def default_post_data(self):
        """Generate default post data with TokenEx authentication info"""

        if self.api_key is None:
            raise AttributeError('Attribute api_key must be set')

        if self.tokenex_id is None:
            raise AttributeError('Attribute tokenex_id must be set')

        default_post_data = {
            "APIKey": self.api_key,
            "TokenExID": self.tokenex_id
        }
        return default_post_data

    @property
    def token_scheme(self):
        """Translate token scheme name to number"""

        if self.token_scheme_name not in self.TOKEN_SCHEMES:
            raise AttributeError('{} is not a valid Token scheme, see TokenEx Docs'.format(
                self.token_scheme_name))
        return self.TOKEN_SCHEMES[self.token_scheme_name]

    @property
    def headers(self):
        """Dynamically generate the headers and overlay headers from requests_options param"""

        headers_dict = copy.deepcopy(self.DEFAULT_HEADERS)

        if self.requests_options and "headers" in self.requests_options.keys():
            for key in self.requests_options['headers']:
                headers_dict[key] = self.requests_options['headers'][key]

        return headers_dict

    def tokenize(self, data):
        """Tokenize a credit card and return result"""

        self.action = "tokenize"
        self.response = None

        post_data = copy.deepcopy(self.default_post_data)
        post_data["Data"] = data
        post_data["TokenScheme"] = self.token_scheme

        options = copy.deepcopy(self.requests_options)
        options['json'] = post_data
        options['headers'] = self.headers

        requests_response = requests.post(self.tokenex_url, **options)
        return TokenExResponse(requests_response)

    def detokenize(self, token):
        """Tokenize a credit card and return result"""

        self.action = "detokenize"
        self.response = None

        post_data = copy.deepcopy(self.default_post_data)
        post_data["Token"] = token

        options = copy.deepcopy(self.requests_options)
        options['json'] = post_data
        options['headers'] = self.headers

        requests_response = requests.post(self.tokenex_url, **options)
        return TokenExResponse(requests_response)

    def tokenize_encrypted(self, data):
        """Tokenize a credit card that has already been browser encrypted"""

        self.action = "tokenize_encrypted"
        self.response = None

        post_data = copy.deepcopy(self.default_post_data)
        post_data["EcryptedData"] = data
        post_data["TokenScheme"] = self.token_scheme

        options = copy.deepcopy(self.requests_options)
        options['json'] = post_data
        options['headers'] = self.headers

        requests_response = requests.post(self.tokenex_url, **options)
        return TokenExResponse(requests_response)

    def validate(self, token):
        """Validate an existing token"""

        self.action = "validate"
        self.response = None

        post_data = copy.deepcopy(self.default_post_data)
        post_data['Token'] = token

        options = copy.deepcopy(self.requests_options)
        options['json'] = post_data
        options['headers'] = self.headers

        requests_response = requests.post(self.tokenex_url, **options)
        return TokenExResponse(requests_response)

    def delete(self, token):
        """Delete an existing token"""

        self.action = "delete"
        self.response = None

        post_data = copy.deepcopy(self.default_post_data)
        post_data['Token'] = token

        options = copy.deepcopy(self.requests_options)
        options['json'] = post_data
        options['headers'] = self.headers

        requests_response = requests.post(self.tokenex_url, **options)
        return TokenExResponse(requests_response)

    def transparent_detokenize(self, data, destination, method='POST', bypass=False):
        """
        Send a request thru the transparent gateway api and detokenize. Use
        bypass argument to bypass TokenEx and post directly to the
        destination.
        """

        self.action = "transparent_detokenize"
        self.response = None

        options = copy.deepcopy(self.requests_options)
        options['headers'] = self.headers

        # not thrilled about this line because it means we can't pass in an Accept header
        # into this command properly but need to remove it for now so that we get back
        # whatever the destination server returns
        options['headers'].pop('Accept')

        if bypass:
            target = destination
        else:
            options['headers']['tx_tokenexid'] = self.tokenex_id
            options['headers']['tx_apikey'] = self.api_key
            options['headers']['tx_url'] = destination
            target = self.tokenex_url

        if options['headers'].get('Content-Type') == "application/json":
            options['json'] = data
        else:
            options['data'] = data

        if bypass and method.lower() == 'get':
            requests_response = requests.get(target, **options)
        else:
            requests_response = requests.post(target, **options)

        return TokenExResponse(requests_response)


class TokenExResponse(object):

    def __init__(self, requests_response):
        self.requests_response = requests_response
        self.codes = requests.codes

    @property
    def status_code(self):
        return self.requests_response.status_code

    @property
    def text(self):
        return self.requests_response.text

    @property
    def content(self):
        return self.requests_response.content

    @property
    def json(self):
        return self.requests_response.json()

    @property
    def encoding(self):
        return self.requests_response.encoding

    @property
    def headers(self):
        return self.requests_response.headers

    def raise_for_status(self):
        self.requests_response.raise_for_status()
        return None

    def raise_for_tokenex_status(self):
        """
        Raises exception if we encounter a TokenEx and only a TokenEx error
        """
        if not self.requests_response.status_code == requests.codes.ok:
            try:
                response_json = self.requests_response.json()
            except JSONDecodeError:
                return None

            if 'Code' and 'RefNumber' in response_json.keys():
                raise TokenExException(response_json)


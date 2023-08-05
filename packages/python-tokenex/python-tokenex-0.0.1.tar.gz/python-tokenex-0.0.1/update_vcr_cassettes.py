#!/usr/bin/env python

import os
import sys

import argparse
import vcr

from tokenex import TokenexRequest


CASSETTE_DIR = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)
    ),
    'tokenex', 'tests', 'fixtures', 'cassettes'
)

MY_VCR = vcr.VCR(
    cassette_library_dir=CASSETTE_DIR,
    record_mode='all',
    filter_post_data_parameters=['APIKey', 'TokenExID']
)


@MY_VCR.use_cassette('tokenize.yml')
def tokenize(tr, data):
    result = tr.tokenize(data)
    result.raise_for_status()
    assert result.json['Success']
    return result.json['Token']


@MY_VCR.use_cassette('tokenize_encrypted.yml')
def tokenize_encrypted(tr, data):
    result = tr.tokenize_encrypted(data)
    assert result.json['Success']
    return result.json['Token']


@MY_VCR.use_cassette('validate.yml')
def validate(tr, token):
    result = tr.validate(token)
    result.raise_for_status()
    assert result.json['Success']
    assert result.json['Valid']


@MY_VCR.use_cassette('detokenize.yml')
def detokenize(tr, token):
    result = tr.detokenize(token)
    result.raise_for_status()
    assert result.json['Success']
    assert result.json['Value'] == ARGS.data


@MY_VCR.use_cassette('delete.yml')
def delete(tr, token):
    result = tr.delete(token)
    result.raise_for_status()
    assert result.json['Success']


def main():

    tr = TokenexRequest(
        ARGS.user_id,
        ARGS.api_key,
        tokenex_test_mode=True,
        token_scheme_name="nTOKENfour"
    )

    token = tokenize(tr, ARGS.data)
    validate(tr, token)
    detokenize(tr, token)
    delete(tr, token)

    if ARGS.encrypted_data:
        token = tokenize_encrypted(tr, ARGS.encrypted_data)
        validate(tr, token)
        detokenize(tr, token)
        delete(tr, token)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('data', help="Plaintext sample string for tokenization")
    parser.add_argument('-u', '--user-id', default=None, help="Tokenex User ID")
    parser.add_argument('-k', '--api-key', default=None, help="Tokenex API Key")
    parser.add_argument('-e', '--encrypted-data', default=None, help="Tokenex Encryption Key")

    ARGS = parser.parse_args()

    if ARGS.user_id is None:
        ARGS.user_id = os.environ.get('TOKENEX_USER_ID', None)
    if ARGS.user_id is None:
        print('You must specify a Tokenex User ID via -u or envar TOKENEX_USER_ID')
        sys.exit(1)

    if ARGS.api_key is None:
        ARGS.api_key = os.environ.get('TOKENEX_API_KEY', None)
    if ARGS.api_key is None:
        print('You must specify a Tokenex API Key via -k or envar TOKENEX_API_KEY')
        sys.exit(1)

    if ARGS.encrypted_data is None:
        print('No encryption data provided, tokenize_encrypted step will be skipped')

    main()

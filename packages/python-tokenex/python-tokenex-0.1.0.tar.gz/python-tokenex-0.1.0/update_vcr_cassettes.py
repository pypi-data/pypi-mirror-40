#!/usr/bin/env python

import os
import sys

import argparse
import vcr

from tokenex import TokenexRequest


# This utility script updates the VCRpy cassettes for all unit tests.  Use -h for options.
# When providing an encrypted string, you can use this pre-encrypted string on the
# TokenEx test api
ENCRYPTED_SAMPLE_DATA = "KDEpseiHuwDDeVl/3L969fSYurfJgoAhhD3JYExtfv13umH9lJRQk7BGx7ZCLMepmSwD+KmIXyww6PHMs6IB7ai1VdCVX1jN6mJxNX/NkygkFlMCcPLsxnP7ZZmrSwWD46Tkzunfh46cVIIZtXEOR9vYh0QzUtlD3SYx5Ocw0JWYONW3aOvLXetQAk7jpt/3+vfAAERyXI5P2Nac8mF2Gm/jkuUKKoPUTd4S4WchCsLU1L084Q8xRaM60Qcwng68mKdEwdOdtByl2ZzPqzvAiyfFhzO9mG0yi8qp5Kg9m3QjQhGVF7OC8+N9zwKQk5y0h2R7DCrPoCt4aoIAlamkyA=="

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
    parser.add_argument('-e', '--encrypted-data',
                        default=ENCRYPTED_SAMPLE_DATA,
                        help="Encrypted data sample")

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

    main()

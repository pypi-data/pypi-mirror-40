import os

import argparse

from .tokenex import TokenExRequest


CLI_COMMAND_MAP = {
    "positionals": {
        "action": {
            "options": {
                "choices": TokenExRequest.COMMAND_MAP.keys(),
                "help": "Command to run"
            }
        },
        "value": {
            "options": {
                "help": "Command Input Value"
            }
        }
    },
    "optionals": {
        "user_id": {
            "short_flag": "-u",
            "long_flag": "--user-id",
            "envar": "TOKENEX_USER_ID",
            "required": True,
            "options": {
                "default": None,
                "help": "TokenEx User ID"
            }
        },
        "api_key": {
            "short_flag": "-k",
            "long_flag": "--api-key",
            "envar": "TOKENEX_API_KEY",
            "required": True,
            "options": {
                "default": None,
                "help": "TokenEx API Key"
            }
        },
        "token_scheme": {
            "short_flag": "-s",
            "long_flag": "--token-scheme",
            "envar": "TOKENEX_SCHEME",
            "options": {
                "default": "TOKENfour",
                "choices": TokenExRequest.TOKEN_SCHEMES.keys(),
                "help": "Tokenization Scheme"
            }
        },
        "test_mode": {
            "short_flag": "-t",
            "long_flag": "--test-mode",
            "envar": "TOKENEX_TEST_MODE",
            "options": {
                "default": None,
                "action": "store_true",
                "help": "Enable Testing Mode"
            }
        }
    }
}


def parse_args():  #pragma: no cover
    parser = argparse.ArgumentParser()

    positionals = CLI_COMMAND_MAP['positionals']
    for key, arg in positionals.items():
        parser.add_argument(key, **arg['options'])

    optionals = CLI_COMMAND_MAP['optionals']
    for key, arg in optionals.items():
        parser.add_argument(str(arg['short_flag']), str(arg['long_flag']), **arg['options'])

    args = parser.parse_args()

    return args


def validate_args(args):

    validation_errors = []
    optional_args = CLI_COMMAND_MAP['optionals']

    for key, arg in optional_args.items():

        # skip test_mode
        if key == 'test_mode':
            continue

        if getattr(args, key) is None:
            setattr(args, key, os.environ.get(arg['envar'], None))
            if not getattr(args, key) and arg.get('required', None):
                error_msg = "You must provide {0} via {1} {2}".format(
                    key,
                    arg['short_flag'],
                    "or envar " + arg.get('envar', "")
                )
                validation_errors.append(error_msg)

    # special validation for test_mode
    test_mode_envar = os.environ.get(optional_args['test_mode']['envar'], None)
    if test_mode_envar and test_mode_envar.lower() == "true":
        test_mode_envar = True
    else:
        test_mode_envar = False
    # if arg not set
    if args.test_mode is None:
        if test_mode_envar:
            args.test_mode = True

    if args.test_mode is None:
        args.test_mode = False

    return validation_errors


def main(args):

    if args.test_mode:
        print("*** TEST MODE ENABLED ***")

    tr = TokenExRequest(
        args.user_id,
        args.api_key,
        tokenex_test_mode=args.test_mode,
        token_scheme_name=args.token_scheme
    )

    result = None

    if args.action == "tokenize":
        result = tr.tokenize(args.value)
    elif args.action == "tokenize_encrypted":
        result = tr.tokenize_encrypted(args.value)
    elif args.action == "validate":
        result = tr.validate(args.value)
    elif args.action == "detokenize":
        result = tr.detokenize(args.value)
    elif args.action == "delete":
        result = tr.delete(args.value)

    if result:
        print("Result:")
        for key, value in result.json.items():
            print("\t{}: {}".format(key, value))
        print("")
    else:
        print("\n** An unexpected error has occurred **\n")  # pragma: no cover


def handle():  # pragma: no cover
    args = parse_args()
    errors = validate_args(args)

    if len(errors) == 0:
        main(args)
    else:
        print("The following validation errors occurred:")
        for validation_error in errors:
            print(" - " + validation_error)


if __name__ == "__main__":

    handle()

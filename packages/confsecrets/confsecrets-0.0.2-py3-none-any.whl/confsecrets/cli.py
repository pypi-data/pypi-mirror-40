#!/usr/bin/env python3
import argparse
import sys
import os
from base64 import b64encode, b64decode

from confsecrets.config import Config
from confsecrets.vault import Vault


try:
    from Cryptodome import Random
except ImportError:
    from Crypto import Random


def newsalt_command(raw=False):
    newsalt = Random.new().read(8)
    if raw:
        print(newsalt)
    else:
        print(b64encode(newsalt).decode('ascii'))
    return 0


def list_secrets_command(vault):
    if len(vault):
        print('Secrets:')
        for key in sorted(vault.keys()):
            print('\t{} = {}'.format(key, vault[key]))
    else:
        print('No secrets')
    return 0


def get_secret_command(vault, secret):
    try:
        print(vault[secret])
    except KeyError:
        sys.stderr.write('There is no secret "{}" in the vault\n'.format(secret))
        return 1
    return 0


def put_secret_command(vault, secret, value):
    vault[secret] = value
    print('Updated "{}" in vault'.format(secret))
    return 0


def rm_secret_command(vault, secret):
    try:
        del vault[secret]
        print('Removed "{}" from vault'.format(secret))
    except KeyError:
        sys.stderr.write('There is no secret "{}" in the vault\n'.format(secret))
        return 1
    return 0


def parse_args(prog, args):
    main_parser = argparse.ArgumentParser(
        prog=prog,
        description='Manage a vault of symmetrically encrypted secrets',
    )
    main_parser.add_argument('--verbose', action='store_true', default=False)
    main_parser.add_argument('--key', metavar='TEXT',
                             default=os.environ.get(Config.KEY.value, None),
                             help='A password or passphrase')
    main_parser.add_argument('--path', metavar='PATH',
                             default=os.environ.get(Config.PATH.value, None),
                             help='A path to the secret vault')
    main_parser.add_argument('--salt', metavar='BASE64',
                             default=os.environ.get(Config.SALT.value, None),
                             help='8-byte base64 encoded salt, see newsalt command')
    sub = main_parser.add_subparsers(dest='cmd')

    newsalt = sub.add_parser('newsalt', help='Create a new vault at the path')
    newsalt.add_argument('--raw', action='store_true', default=False)

    get_secret = sub.add_parser('get', help='Get a secret from the vault')
    get_secret.add_argument('name')

    sub.add_parser('list', help='List secrets in the vault')

    put_secret = sub.add_parser('put', help='Update the vault with a new secret')
    put_secret.add_argument('name')
    put_secret.add_argument('value')

    rm_secret = sub.add_parser('rm', help='Remove a secret from the vault')
    rm_secret.add_argument('name')
    return main_parser.parse_args(args)


def main_guts(prog, args):
    opts = parse_args(prog, args)

    if opts.cmd == 'newsalt':
        return newsalt_command(raw=opts.raw)

    salt = opts.salt
    if not salt:
        sys.stderr.write('salt required: provide --salt or CONFSECRETS_SALT via environment\n')
        return 1
    salt = b64decode(opts.salt)

    if not opts.key:
        sys.stderr.write('key required: provide --key or CONFSECRETS_KEY via environment\n')
        return 1

    if not opts.path:
        sys.stderr.write('path required: provide --path or CONFSECRETS_PATH via environment\n')
        return 1

    vault = Vault(salt, opts.key, opts.path)
    if opts.cmd == 'list':
        return list_secrets_command(vault)
    elif opts.cmd == 'get':
        return get_secret_command(vault, opts.name)
    elif opts.cmd == 'put':
        return put_secret_command(vault, opts.name, opts.value)
    elif opts.cmd == 'rm':
        return rm_secret_command(vault, opts.name)
    else:
        sys.stderr.write('A command is required\n')
        return 1


def main():
    rv = main_guts(sys.argv[0], sys.argv[1:])
    sys.exit(rv)


if __name__ == '__main__':
    main()

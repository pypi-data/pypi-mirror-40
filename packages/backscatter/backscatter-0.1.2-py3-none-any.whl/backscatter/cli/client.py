#!/usr/bin/env python
"""."""
import json
import logging
import os
import sys

from argparse import ArgumentParser
from backscatter import Backscatter


CONFIG_PATH = os.path.expanduser('~/.config/backscatter')
CONFIG_FILE = os.path.join(CONFIG_PATH, 'config.json')
CONFIG_DEFAULTS = {'version': 'v0', 'api_key': ''}


def main():
    """Run the core."""
    parser = ArgumentParser()
    subs = parser.add_subparsers(dest='cmd')
    setup_parser = subs.add_parser('setup')
    setup_parser.add_argument('-k', '--api-key', dest='api_key', required=True,
                              help='API key for Backscatter.', type=str)

    setup_parser = subs.add_parser('observations')
    setup_parser.add_argument('-q', '--query', dest='query', required=True,
                              help='Query to search with.', type=str)
    setup_parser.add_argument('-t', '--type', dest='query_type', required=True,
                              help='Query type to search.', type=str)
    setup_parser.add_argument('--scope', dest='scope', required=False,
                              help='Days to search back through.', type=int)
    setup_parser.add_argument('--summary', dest='summary', required=False,
                              help='Print the summary information.', default=False,
                              action='store_true')

    setup_parser = subs.add_parser('trends')
    setup_parser.add_argument('-t', '--type', dest='trend_type', required=True,
                              help='Trend type to search.', type=str)
    setup_parser.add_argument('--scope', dest='scope', required=False,
                              help='Days to search back through.', type=int)
    args = parser.parse_args()

    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    if not os.path.exists(CONFIG_FILE):
        json.dump(CONFIG_DEFAULTS, open(CONFIG_FILE, 'w'), indent=4,
                  separators=(',', ': '))

    if args.cmd == 'setup':
        config = CONFIG_DEFAULTS
        config['api_key'] = args.api_key
        json.dump(config, open(CONFIG_FILE, 'w'), indent=4,
                  separators=(',', ': '))

    config = json.load(open(CONFIG_FILE))
    if config['api_key'] == '':
        raise Exception("Run setup before any other actions!")

    if args.cmd == 'observations':
        bs = Backscatter(api_key=config['api_key'], version=config['version'])
        kwargs = {'query': args.query, 'query_type': args.query_type}
        if args.scope:
            kwargs.update({'scope': args.scope})
        response = bs.get_observations(**kwargs)
        if args.summary:
            results = response.get('results', dict())
            print(json.dumps(results.get('summary', dict()), indent=4))
        else:
            print(json.dumps(response, indent=4))

    if args.cmd == 'trends':
        bs = Backscatter(api_key=config['api_key'], version=config['version'])
        kwargs = {'trend_type': args.trend_type}
        if args.scope:
            kwargs.update({'scope': args.scope})
        response = bs.get_trends(**kwargs)
        print(json.dumps(response, indent=4))

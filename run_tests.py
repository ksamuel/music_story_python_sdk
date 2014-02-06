#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Run the music_story unit tests.

Usage:
  run_tests.py <consumer_key> <consumer_secret> [<access_token>] [<token_secret>]
  run_tests.py --file=INI_FILE

You can pass the Oauth credentials using a ini files containing:

 consumer_key=your key
 consumer_secret=your secret
 access_token=your access token (this line is optional)
 token_secret=you token secret (this line is optional)

"""

from __future__ import absolute_import

import sys
import os

try:
    import pytest
    from docopt import docopt
except:
    sys.exit('You must install lib dependancies before running tests. '
             'Use setup.py.')

from tests import CREDENTIALS_FILE


arguments = docopt(__doc__)

f = arguments['--file']
if f is not None:
    arguments = {}
    if not os.path.isfile(f):
        sys.exit('Cannot open file "%s"' % f)

    # extract credentials from a ini file
    for line in open(f):
        line = line.strip()
        if line:
            key, val = line.split('=')
            arguments[key.strip()] = val.strip()

    if not 'consumer_key' in arguments:
        sys.exit('Missing consumer_key value')

    if not 'consumer_secret' in arguments:
        sys.exit('Missing consumer_secret value')


# hack to pass the credential to tests using a temp file
with open(CREDENTIALS_FILE, 'w') as f:
    for key, val in arguments.items():
        if not '--' in key and val is not None:
            f.write("%s=%s\n" % (key.strip('<>'), val))

try:
    result = pytest.main(['-x', '--capture=no', 'tests'])
finally:
    os.remove(CREDENTIALS_FILE)

sys.exit(result)


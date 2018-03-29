#!/usr/bin/env python

import os
import json
import sys

output_dir = sys.argv[1]
os.system('cp /tmp/addresses.csv {}/addresses.csv'.format(output_dir))

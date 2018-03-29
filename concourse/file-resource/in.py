#!/usr/bin/env python

import os
import json
import sys

destination_dir = sys.argv[1]
source_payload = json.loads(sys.stdin)
print(source_payload)


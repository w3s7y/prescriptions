#!/usr/bin/env python

import requests
import sys
import json
import hashlib

# Output directory, input payload etc.
output_dir = sys.argv[1]
input = json.loads(sys.stdin.readline())
source = input['source']
params = input['params']

# Get the file from online source
file_req = requests.get(source['url'])
filename = source['url'].split('/')[-1]

# Create SHA512 hash for version.
hash_ver = hashlib.sha512(file_req.text.encode('utf-8')).hexdigest()

# Write the downloaded file to output dir.
out = open('{}/{}.csv'.format(output_dir, filename), 'w')
out.writelines(file_req.text)
out.flush()
out.close()

response = {"version": hash_ver}

print(response)
sys.exit(0)

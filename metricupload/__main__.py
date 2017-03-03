"""
Copyright (C) 2017 by Strong Leaf Consultant Ltd.

GNU AGPL v3+

Upload custom metrics
"""

from benchupload import cidetect
from metricupload import schema

import argparse
import json
import os
import sys
import jsonschema
import requests

def parsed_args():
    parser = argparse.ArgumentParser(description="Upload handling")
    parser.add_argument('--url', dest='url', default='https://api.bob-bench.org/v1/metric_upload.pl', help="Uplpad URL")
    parser.add_argument('files', metavar='file', nargs='+', help="List of files to upload")
    return parser.parse_args()

def post(url, ci, fnames):
    files = list(map(lambda x: (os.path.basename(x), open(x, 'rb')), fnames))
    data = {
        'x-is-github':  ci.is_github,
        'x-commit':     ci.commit,
        'x-tag':        ci.tag,
        'x-branch':     ci.branch,
        'x-buildnr':    ci.build_nr,
        'x-os-name':    ci.os_name,
        'x-repo-url':   ci.repo_url,
        'x-ci':         ci.system_name(),
        'x-job-id':     ci.job_id,
        'x-prev-buildnr': ci.prev_build_nr
    }
    res = requests.post(url, data=data, files=files)
    if res.status_code != 200:
        sys.stderr.write("Failed to POST resources\n")
        sys.exit(43)

def validate(fname, json_data):
    try:
        jsonschema.validate(json_data, schema)
    except jsonschema.exceptions.ValidationError as e:
        sys.stderr.write("ERROR: file: %s. %s\n" % (fname, e))
        sys.exit(45)

def main():
    args = parsed_args()

    for fname in args.files:
        try:
            with open(fname, "r") as f:
                try:
                    data = json.load(f)
                    validate(fname, data)
                except ValueError as e:
                    sys.stderr.write("ERROR: file: %s. %s\n" % (fname, e))
                    sys.exit(44)
        except IOError as e:
            sys.stderr.write("ERROR: %s.\n" % e)
            sys.exit(43)

    ci = cidetect.detect()
    if not ci:
        sys.stderr.write("No CI system reported. Please report it to cidetect@bob-bench.org\n")
        sys.exit(42)

    if ci.is_pull_request:
        sys.stdout.write("Skipping on pull-request\n")
        sys.exit(0)

    post(args.url, ci, args.files)
    sys.stdout.write("Uploaded {} files\n".format(len(files)))

if __name__ == "__main__":
    main()

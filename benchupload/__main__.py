"""
Copyright (C) 2016 by Strong Leaf Consultant Ltd.

GNU AGPL v3+

Bob-Bench xUnit file detection
"""

from benchupload import xunit
from benchupload import cidetect
import argparse
import os
import sys
import requests


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
        'x-job-id':     ci.job_id
    }
    res = requests.post(url, data=data, files=files)
    if res.status_code != 200:
        sys.stderr.write("Failed to POST resources\n")
        sys.exit(43)

def parsed_args():
    parser = argparse.ArgumentParser(description="Upload handling")
    parser.add_argument('--dir', dest='start_dir', default=os.curdir, help="Start directory")
    parser.add_argument('--url', dest='url', default='https://api.bob-bench.org/v1/xunit_upload.pl', help="Uplpad URL")
    return parser.parse_args()

def main():
    args = parsed_args()
    ci = cidetect.detect()
    if not ci:
        sys.stderr.write("No CI system reported. Please report it to cidetect@bob-bench.org\n")
        sys.exit(42)

    files = xunit.detect_xunit_files(args.start_dir)
    if len(files) == 0:
        sys.stdout.write("No XML test results detected\n")
        sys.exit(0)

    post(args.url, ci, files)
    sys.stdout.write("Uploaded {} files\n".format(len(files)))

if __name__ == "__main__":
    main()


"""
Copyright (C) 2016 by Strong Leaf Consultant Ltd.

GNU AGPL v3+

Bob-Bench xUnit file detection
"""

from benchupload import xunit
from benchupload import cidetect
import os
import sys
import requests


xunit_dest_url = "https://api.bob-bench.org/v1/xunit_upload.pl"

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
        'x-ci':         ci.system_name()
    }
    res = requests.post(xunit_dest_url, data=data, files=files)
    if res.status_code != 200:
        sys.stderr.write("Failed to POST resources\n")
        sys.exit(43)

def main():
    ci = cidetect.detect()
    if not ci:
        sys.stderr.write("No CI system reported. Please report it to cidetect@bob-bench.org\n")
        sys.exit(42)

    files = xunit.detect_xunit_files(os.curdir)
    if len(files) == 0:
        sys.stdout.write("No XML test results detected\n")
        sys.exit(0)

    post(xunit_dest_url, ci, files)

if __name__ == "__main__":
    main()


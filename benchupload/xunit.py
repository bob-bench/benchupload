"""
Copyright (C) 2016 by Strong Leaf Consultant Ltd.

GNU AGPL v3+

Bob-Bench xUnit file detection
"""

import os
import os.path

def is_xunit_file(fname):
    if not fname.endswith(".xml"):
        return False
    with open(fname, "rb") as f:
        # Somehow str/bytes in f (file, textwrapper) does not work
        # assume the xml file is reasonable small
        content = f.read()
        return b"<testsuite" in content

def detect_xunit_files(base):
    res = []
    for root, dirs, files in os.walk(base):
        abs_files = map(lambda x: os.path.join(root, x), files)
        res.extend(filter(is_xunit_file, abs_files))
    return res

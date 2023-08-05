# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os
import sys

from .validate import validate_py3


def main():
    """Run validate on a single python file"""
    if len(sys.argv) != 2:
        sys.stderr.write("No python file specified")
        sys.exit(1)

    file_path = os.path.abspath(os.path.realpath(sys.argv[1]))
    if not os.path.exists(file_path):
        sys.stderr.write("{} does not exist.".format(file_path))
        sys.exit(1)

    results = validate_py3(file_path)
    if results:
        print(results[file_path])

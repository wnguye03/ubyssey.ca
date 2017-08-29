#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # os.environ.setdefault("DISPATCH_PROJECT_DIR", os.path.dirname(os.path.realpath(__file__)))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ubyssey.settings2")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

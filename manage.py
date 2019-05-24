#!/usr/bin/env python
import os
import sys

app = __name__

if app == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ubyssey.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

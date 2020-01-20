#!/usr/bin/env python
import os
import sys
from app import app

if __name__ == "__main__":
    app.run(debug=True)
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")
    #
    # from django.core.management import execute_from_command_line
    #
    # execute_from_command_line(sys.argv)

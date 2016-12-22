#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qipr_approver.settings")

    from django.core.management import execute_from_command_line

    import django
    django.setup()

    if sys.argv[1] == 'loadmesh':
        from approver.custom_commands import loadmesh
        loadmesh(sys.argv)
    else:
        execute_from_command_line(sys.argv)

#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qipr_approver.settings")

    from django.core.management import execute_from_command_line

    import django
    django.setup()

    from approver.signals.bridge.all_signals import disconnect_signals

    if sys.argv[1] == 'loadmesh':
        disconnect_signals()
        from approver.custom_commands import loadmesh
        loadmesh(sys.argv)
    elif sys.argv[1] == 'loadcontacts':
        disconnect_signals()
        from approver.custom_commands import loadcontacts
        loadcontacts(sys.argv)
    elif sys.argv[1] == 'loadprojects':
        disconnect_signals()
        from approver.custom_commands import loadprojects
        loadprojects(sys.argv)
    elif sys.argv[1] == 'dedupemesh':
        disconnect_signals()
        from approver.custom_commands import dedupemesh
        dedupemesh(sys.argv)
    else:
        execute_from_command_line(sys.argv)

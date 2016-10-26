from django.apps import AppConfig

import approver.constants as constants

class ApproverConfig(AppConfig):
    name = constants.app_label

    def ready(self):
        from approver.signals import all_signals


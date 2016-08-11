from django.apps import AppConfig


class ApproverConfig(AppConfig):
    name = 'approver'

    def ready(self):
        from approver.signals import all_signals


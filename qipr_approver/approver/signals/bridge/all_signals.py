from approver.signals.bridge.model_signals import connect_model_signals, disconnect_for_loading

def connect_signals():
    connect_model_signals()

def disconnect_signals():
    disconnect_for_loading()

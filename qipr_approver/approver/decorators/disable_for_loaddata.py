def disable_for_loaddata(signal_function):
    """
    This is a decorator that will disable signals
    that should not be run on loaddata
    """
    def wrapped_signal(**kwargs):
        if kwargs.get('raw'):
            return
        else:
            return signal_function(**kwargs)
    return wrapped_signal

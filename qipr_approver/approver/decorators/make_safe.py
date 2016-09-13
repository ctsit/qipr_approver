def make_safe(func):
    """
    When things could blow up,
    and you know that it happens
    the decorator
    """
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return None
    return wrapped

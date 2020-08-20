class AbortFlag:
    def __init__(self):
        self._abort = False

    def set_abort(self):
        self._abort = True

    def is_set(self):
        return self._abort

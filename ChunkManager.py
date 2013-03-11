class ChunkManager:
    """Dynamically loads and unloads data from files
    to accomodate data sets larger than memory

    """
    def __init__(self, files):
        """

        """
        self._files = files
        self._chunks = {}
        self._data = {}

    def get(self, name):
        value = None
        try:
            value = self._data[name]
        except KeyError:
            self.load(name)
        return value

    def load_range(self, lower, upper):
        pass

    def unload_range(self, lower, upper):
        pass

    def load(self, name):
        pass

    def unload(self, name):
        pass

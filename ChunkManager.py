"""
Contains classes that support data sets which can exist both on disk and in
memory


"""

import cPickle


class Chunk:
    """Holds header information for a chunk and handles bringing the chunk
    data in and out of memory

    """
    def __init__(self, chunkPath):
        self._path = chunkPath
        self._data = None

    def load(self):
        """Bring the chunk data into memory"""
        self._data = cPickle.load(self._path)

    def unload(self):
        """Write back the chunk data to file and removes it from memory"""
        cPickle.dump(self._data, self._path)
        self._data = None


class ChunkManager:
    """Dynamically loads and unloads data from files
    to accomodate data sets larger than memory

    """
    def __init__(self, chunkHeaderPath, maxChunks):
        """

        """
        self._chunkHeaders = cPickle.load(chunkHeaderPath)
        self._chunksLoaded = 0
        self._maxChunks = maxChunks

    def get(self, name):
        """Retrieve data value specified by name"""
        value = None
        try:
            value = self._chunkHeaders[name]
        except KeyError:
            self.load(name)
        return value

    def load_range(self, lower, upper):
        pass

    def unload_range(self, lower, upper):
        pass

    def load(self, name):
        self._chunksLoaded += 1

    def unload(self, name):
        self._chunksLoaded -= 1

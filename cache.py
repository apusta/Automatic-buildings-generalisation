import pickle
import os.path


class Cache:
    DIR = 'dump'

    def save(self, filename, data):
        if os.path.exists(self.__getDumpPath()) is False:
            os.mkdir(self.__getDumpPath())

        with open(self.__getPath(filename), 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, filename):
        with open(self.__getPath(filename), 'rb') as handle:
            return pickle.load(handle)

    def exists(self, filename):
        return os.path.exists(self.__getPath(filename))

    def __getPath(self, filename):
        current_dir = os.path.dirname(__file__)
        return os.path.join(current_dir, self.DIR, filename + '.pickle')

    def __getDumpPath(self):
        current_dir = os.path.dirname(__file__)
        return os.path.join(current_dir, self.DIR)

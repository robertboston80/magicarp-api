class Engine(object):
    def __init__(self, **kwargs):
        self.data = {}

    def set_key(self, key, data, **extra):
        self.data[key] = data

    def get_key(self, key):
        return self.data[key]

    def delete_key(self, key):
        del self.data[key]

    def key_exists(self, key):
        return key in self.data

    def flush_all(self):
        self.data = {}

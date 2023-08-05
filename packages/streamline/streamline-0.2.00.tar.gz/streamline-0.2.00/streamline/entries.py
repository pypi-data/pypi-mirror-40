
class Entry():
    def __init__(self, value, index=None):
        self.index = index
        self.values = [value]
        self.errors = []

    @property
    def original_value(self):
        return self.values[0]

    def get_value(self):
        return self.values[-1]

    def set_value(self, new_value):
        self.values.append(new_value)

    def error(self, e):
        self.errors.append(e)
        self.value = None

    value = property(get_value, set_value)

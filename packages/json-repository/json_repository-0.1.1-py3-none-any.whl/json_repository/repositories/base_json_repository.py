from ..context.json_context import JsonContext


class BaseJsonRepository(object):
    def __init__(self, entity_name, filepath="./"):
        self.context = JsonContext(entity_name, filepath=filepath)

    def __enter__(self):
        self.context.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.close()

    def insert(self, entity):
        return self.context.add(entity)

    def update(self, entity):
        return self.context.add(entity)

    def delete(self, entity):
        self.context.delete(entity)

    def get_all(self):
        return self.context.get_all()

    def get(self, identifier):
        return self.context.get(identifier)

    def find(self, function):
        return self.context.find(function)

    def first(self, function=None):
        return self.context.first(function)

    def single(self, function=None):
        return self.context.single(function)



class Element(object):
    def __init__(self, params):
        self.__dict__.update(params)
        self.__initial = list(params.keys())

    def __str__(self):
        _d = {}
        for p in self.__initial:
            _d[p] = getattr(self, p)
        return str(_d)

    def __repr__(self):
        return self.__str__()


class Entity:
    def __init__(self, config, model=None):
        self.wrapper, self.fields = list(config.items())[0]
        self.data = []
        self.model = model

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def append_data(self, data):
        '''Appends parsed data to entity storage
        Args:
            data (dict): dictionary whith keys same as self.fields
                and parsed data from xml as a value
        '''
        _d = {k: data.get(k) for k in self.fields}
        self.data.append(self.gen_element(_d))

    def clear(self):
        self.data = list()

    def gen_element(self, element):
        if self.model is not None:
            return self.model(**element)
        return Element(element)




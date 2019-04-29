"""
Classes to define all location types. Uses the Composite Pattern.
"""

from abc import ABC, abstractmethod


class Location(ABC):
    """
    Abstract component
    """
    def __init__(self, name):
        self.name = name

    def add(self, component):
        pass

    def remove(self, idx):
        pass

    def __getitem__(self, item):
        pass

    def __iter__(self):
        return NullIterator()

    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.name)

    def __str__(self):
        return self.name

    def __eq__(self, value):
        return self.name == value


class Site(Location):

    def __init__(self, name, identifier, latitude, longitude, elevation):

        super().__init__(self, name)
        self.identifier = identifier
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

        self.forecast_3hourly = None
        self.forecast_daily = None
        self.observations_hourly = None

    def __repr__(self):
        return "{}('{}:{}')".format(
            type(self).__name__,
            self.name,
            self.identifier)


class Area(Location):

    def __init__(self, name):
        super().__init__(self, name)
        self.children = []
        self.regions = []
        self.areas = []

    def add(self, component):
        if isinstance(component, Region):
            self.regions.append(component)
        if isinstance(component, Area):
            self.areas.append(component)
        self.children.append(component)

    def remove(self, idx):
        self.children[idx] = []

    def __len__(self):
        return len(self.children)

    def __getitem__(self, idx):
        return self.children[idx]

    def __iter__(self):
        return AreaIterator(self.children)


class Region(Area):

    def __init__(self, name, region_id):

        super().__init__(self, name)
        self.region_id = region_id

    def __repr__(self):
        return "{}('{}:{}')".format(
            type(self).__name__,
            self.name,
            self.region_id)


class AreaIterator(object):
    """
    Object to iterate through the children in an area or region
    """

    def __init__(self, children):
        self.position = 0
        self.children = children
        self.stack = [children.__iter__()]

    def __next__(self):

        if self.stack == []:
            raise StopIteration
        else:
            try:
                component = next(self.stack[-1])
                self.stack.append(component.__iter__())
                return component
            except StopIteration:
                self.stack.pop()
                return self.__next__()


class NullIterator(object):
    def __next__(self):
        raise StopIteration()

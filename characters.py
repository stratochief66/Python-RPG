__author__ = 'Kyle_Lasowski'

class IterRegistry(type): # borrowed from internet, allows iteration over classes that use this as a metaclass
    def __iter__(cls):
        return iter(cls._registry)

class Character(object):
    __metaclass__ = IterRegistry
    _registry = []

    entityCount = 0

    def __init__(self, name, rep_char, health = 100, strength = 2, view_range = 2):
        self._registry.append(self)
        self.name = name
        self.health = health
        self.strength = strength
        self.view_range = view_range
        self.rep_char = rep_char
        self.xp = 0
        self.position = (4,1)
        self.number = Character.entityCount

        Character.entityCount += 1

    def display_stats(self):
        return "This person/object is %s with %s health and represented by %s" % (self.name, self.health, self.rep_char)

class Monster(Character): # subclass of Character. inherits from Character.
    def __init__(self, name, health = 20, strength = 1, view_range = 2, rep_char = 'b', position = (4,4)): # defaults will create a bat
        self._registry.append(self)
        self.name = name
        self.health = health
        self.strength = strength
        self.view_range = view_range
        self.rep_char = rep_char
        self.xp = False
        self.position = position
        self.number = Character.entityCount

        Character.entityCount += 1
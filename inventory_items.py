__author__ = 'Kyle_Laskowski'

from characters import IterRegistry

class InvItem(object):
    __metaclass__ = IterRegistry
    _registry = []

    entityCount = 0

    def __init__(self, name, description, weight, rep_char, position, cost=10):  # future, add rep_char & rep_colour
        self._registry.append(self)
        self.name = name
        self.description = description
        self.weight = weight
        self.rep_char = rep_char
        self.position = position
        self.cost = cost

class InvWeapon(InvItem):

    def __init__(self, name, description, weight, rep_char, position, attack, cost=20):
        InvItem.__init__(self, name, description, weight, rep_char, position, cost)  # can I save on repetition here?
        self.attack = attack
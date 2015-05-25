__author__ = 'Kyle Laskowski'
"""
setattr(hero, 'health', hero.health + 5) # a syntax for stepping a known function up or down

hasattr(emp1, 'age')    # Returns true if 'age' attribute exists
getattr(emp1, 'age')    # Returns value of 'age' attribute
setattr(emp1, 'age', 8) # Set attribute 'age' at 8
delattr(empl, 'age')    # Delete attribute 'age'
"""

class IterRegistry(type): # borrowed from internet, allows iteration over classes that use this as a metaclass
    def __iter__(cls):
        return iter(cls._registry)

class Character(object):
    __metaclass__ = IterRegistry
    _registry = []

    empCount = 0

    def __init__(self, name, rep_char, health = 100, strength = 2, view_range = 2):
        self._registry.append(self)
        self.name = name
        self.health = health
        self.strength = strength
        self.view_range = view_range
        self.rep_char = rep_char
        self.xp = 0
        self.position = (4,1)
        self.number = Character.empCount

        Character.empCount += 1

    def display_stats(self):
        return "This person/object is %s with %s health and represented by %s" % (self.name, self.health, self.rep_char)

class Monster(Character): # subclass of Character. inherits from Character.
    def __init__(self, name, health = 20, strength = 1, view_range = 2, rep_char = 'm'):
        self._registry.append(self)
        self.name = name
        self.health = health
        self.strength = strength
        self.view_range = view_range
        self.rep_char = rep_char
        self.xp = False
        self.position = (4,4)
        self.number = Character.empCount

        Character.empCount += 1

map = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (1,0), (1,7), (2,0), (2,7), (3,0), (3,1), (3,3), (3,4), (3,5), (3,7),
    (4,0), (4,3), (4,7), (5,0), (5,1), (5,3), (5,4), (5,5), (5,7), (6,0), (6, 7), (7,0), (7,7), (8,0), (8,1), (8,2), (8,3),
    (8,4), (8,5), (8,6), (8,7)] # a basic test map. maps suck in python, and/or I need a better way to create maps

# row 0 through 7
# column 0 through 8

hero = Character("Kyle", 'K', 100, 2, 4) # overrides the default view range, confirms the other properties.
bat = Monster("bat")

def print_map():
    special = {}
    for item in Character:
        special[item.position] = item.rep_char # need to review the syntax of how this works
    print
    for row in range(9):
        for column in range(8):
            if (row, column) in map:
                print "W", # where wall exists, the character W will print
            elif (row, column) in special:
                print special[(row,column)],
            else:
                print " ",
        print("")
    print("")

def User_Interface(): # requests a move command from the user, then prints all objects current positions
    import os
    os.system('cls') # will clear the screen between turns.

    print_map()

    global prompt # will be determined by user choice, handed to Control Loop for feedback in screen printout

    print(prompt)
    print

    x = raw_input("Which direction would you like to move in? <N E S W>  (" + str(turn_count) + " turns remaining) :")
    x = x.upper() # input will accept upper or lower case valid directions
    print
    if x == 'N':
        if not (hero.position[0] - 1, hero.position[1]) in map:
            hero.position = (hero.position[0] - 1, hero.position[1])
            prompt = "You moved."
        else:
            prompt = "There must be a wall there. Lose a turn."
            print
    elif x == 'S':
        if not (hero.position[0] + 1, hero.position[1]) in map:
            hero.position = (hero.position[0] + 1, hero.position[1])
            prompt = "You moved."
        else:
            prompt = "There must be a wall there. Lose a turn."
            print
    elif x == 'E':
        if not (hero.position[0], hero.position[1] + 1) in map:
            hero.position = (hero.position[0], hero.position[1] + 1)
            prompt = "You moved."
        else:
            prompt = "There must be a wall there. Lose a turn."
            print
    elif x == 'W':
        if not (hero.position[0], hero.position[1] - 1) in map:
            hero.position = (hero.position[0], hero.position[1] - 1)
            prompt = "You moved."
        else:
            prompt = "There must be a wall there. Lose a turn."
            print
    else:
        prompt = "Can't follow instructions? Lose a turn."
        print

    print_map()

turn_count = 4 # Behind the scenes turn count control

prompt = "first turn, good luck!"

def Control_Loop(): #relies on and counts down the turn_count
    global turn_count
    while turn_count > 0:
        User_Interface()
        turn_count -= 1
    else:
        print("You are out of turns.")
        raw_input("Press Enter to close game.")

Control_Loop() # will begin the program


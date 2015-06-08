__author__ = 'Kyle Laskowski'
"""
setattr(hero, 'health', hero.health + 5) # a syntax for stepping a known function up or down

hasattr(emp1, 'age')    # Returns true if 'age' attribute exists
getattr(emp1, 'age')    # Returns value of 'age' attribute
setattr(emp1, 'age', 8) # Set attribute 'age' at 8
delattr(empl, 'age')    # Delete attribute 'age'
"""

from characters import *
from inventory_items import *
from prompt_class import PromptText

wall_map = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (1,0), (1,7), (2,0), (2,7), (3,0), (3,1), (3,3), (3,4), (3,5), (3,7),
    (4,0), (4,3), (4,7), (5,0), (5,1), (5,3), (5,4), (5,5), (5,7), (6,0), (6, 7), (7,0), (7,7), (8,0), (8,1), (8,2), (8,3),
    (8,4), (8,5), (8,6), (8,7)]  # a basic test map. maps suck in python, and/or I need a better way to create maps

# map structure:
# row 0 through 7
# column 0 through 8

turn_count = 25  # Behind the scenes turn count control

objects_of_interest = {}

hero = Character("Kyle", 'K', 50, 2, 4)  # overrides the default view range, confirms the other properties.

knife = InvWeapon("knife", "Used against enemies", 1, 'w', position=(7, 2), attack=1)

bat = Monster("bat")
dragon = Monster("dragon", 200, 5, 3, rep_char='d', position=(1, 5))

def combat(enemy):
    hero.health -= enemy.strength
    enemy.health -= hero.strength  # v2 both parties take damage proportional to the combatant's strength.

    if knife in hero.inventory:
        enemy.health -= knife.attack

    if hero.health <= 0:
        PromptText.add_to("You have died in glorious combat with a %s." % enemy.name)
        PromptText.print_out()
        import sys
        sys.exit()

    if enemy.health <= 0:
        hero.xp += 10 * enemy.strength  # v2, step XP proportional to enemy strength
        PromptText.add_to("You have killed the fierce %s and now have %s experience!" % (enemy.name, str(hero.xp)))
        """ above, the idea is to append this bit of prompt text to the existing string,
        so that it is displayed on the next screen refresh loop """


def prompt_decision(location):
    if location in wall_map:
        PromptText.add_to("There must be a wall there. Lose a turn.")
        return hero.position
    elif location in objects_of_interest:
        if type(objects_of_interest[location]) == Monster:  # if you have bumped into a monster
            combat(objects_of_interest[location])
            if objects_of_interest[location].health > 0:
                PromptText.add_to("Prepare to fight a %s!" % objects_of_interest[location].name)
                PromptText.add_to("You have %s health remaining and the enemy has %s." % (hero.health, objects_of_interest[location].health))
            return hero.position
        else:
            PromptText.add_to("You have found a %s and picked it up." % objects_of_interest[location].name)
            hero.inventory.append(objects_of_interest[location])
            objects_of_interest[location].position = ()
            return hero.position
    else:
        PromptText.add_to("You moved.")
        return location


def print_map():
    global objects_of_interest  # make special global so that it can be used for combat decisions
    objects_of_interest = {}

    for item in Character:
        if item.health > 0:
            objects_of_interest[item.position] = item  # dictionary, location : creature

    for thing in InvItem:
        if not thing.position == ():  # objects in inventories will have null positions
            objects_of_interest[thing.position] = thing

    print

    for row in range(9):
        for column in range(8):
            if (row, column) in wall_map:
                print "W",  # where wall exists, the character W will print
            elif (row, column) in objects_of_interest:
                print objects_of_interest[(row,column)].rep_char,  # by my design, this should return the creature.rep_char ie. bat.rep_char which is b
            else:
                print " ",
        print("")
    print("")

def user_interface():  # requests a move command from the user, then prints all objects current positions
    import os
    import platform
    if platform.system() == 'Windows':
        os.system('cls')  # will clear the screen between turns on Windows
    else:
        os.system('clear')  # will clear the screen between turns on Linux or OSX

    print_map()
    
    PromptText.print_out()
    
    print

    if platform.system() == 'Vindows':
        import msvcrt
        print "Which direction would you like to move in? <N E S W>  (" + str(turn_count) + " turns remaining. Q to quit.) : "
        input_char = msvcrt.getwche()
    else:
        input_char = raw_input("Which direction would you like to move in? <N E S W>  (" + str(turn_count) + " turns remaining. Q to quit.) : ")

    input_char = input_char.upper()  # input will accept upper or lower case valid directions

    print

    if input_char == 'N':
        hero.position = prompt_decision((hero.position[0] - 1, hero.position[1]))
    elif input_char == 'S':
        hero.position = prompt_decision((hero.position[0] + 1, hero.position[1]))
    elif input_char == 'E':
        hero.position = prompt_decision((hero.position[0], hero.position[1] + 1))
    elif input_char == 'W':
        hero.position = prompt_decision((hero.position[0], hero.position[1] - 1))
    elif input_char == 'Q':
        print("You have chosen to end the game. Goodbye.")
        raw_input("Press Enter to close game.")  # intended to give the user a chance to review the screen before exiting
        import sys
        sys.exit()
        

def control_loop():  # relies on and counts down the turn_count
    global turn_count
    while turn_count > 0:
        user_interface()
        turn_count -= 1
    else:
        print("You are out of turns.")
        raw_input("Press Enter to close game.")  # intended to give the user a chance to review the screen before exiting


control_loop() # will begin the program


__author__ = 'Kyle Laskowski'
"""
setattr(hero, 'health', hero.health + 5) # a syntax for stepping a known function up or down

hasattr(emp1, 'age')    # Returns true if 'age' attribute exists
getattr(emp1, 'age')    # Returns value of 'age' attribute
setattr(emp1, 'age', 8) # Set attribute 'age' at 8
delattr(empl, 'age')    # Delete attribute 'age'
"""

from characters import Character
from characters import Monster # seriously, I have to import both classes separately?
from characters import IterRegistry

wall_map = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (1,0), (1,7), (2,0), (2,7), (3,0), (3,1), (3,3), (3,4), (3,5), (3,7),
    (4,0), (4,3), (4,7), (5,0), (5,1), (5,3), (5,4), (5,5), (5,7), (6,0), (6, 7), (7,0), (7,7), (8,0), (8,1), (8,2), (8,3),
    (8,4), (8,5), (8,6), (8,7)]  # a basic test map. maps suck in python, and/or I need a better way to create maps

# map structure:
# row 0 through 7
# column 0 through 8

turn_count = 25 # Behind the scenes turn count control

prompt_text = "first turn, good luck!"  # initializes prompt

special = {}

hero = Character("Kyle", 'K', 50, 2, 4)  # overrides the default view range, confirms the other properties.
bat = Monster("bat")
dragon = Monster("dragon", 200, 5, 3, rep_char='d', position=(1,5))

def combat(enemy):
    hero.health -= enemy.strength
    enemy.health -= hero.strength  # v2 both parties take damage proportional to the combatant's strength.

    if hero.health <= 0:
        print "\nYou have died in glorious combat with a %s." % enemy.name
        import sys
        sys.exit()
    if enemy.health <= 0:
        hero.xp += 10 * enemy.strength  # v2, step XP proportional to enemy strength

        global prompt_text
        prompt_text += "\nYou have killed the fierce %s and now have %s experience!" % (enemy.name, str(hero.xp))
        """ above, the idea is to append this bit of prompt text to the existing string,
        so that it is displayed on the next screen refresh loop """

def prompt_decision(location):
    global prompt_text
    if location in wall_map:
        prompt_text += "There must be a wall there. Lose a turn."
        return hero.position
    elif location in special:
        prompt_text += "Prepare to fight a %s! \nYou have %s health remaining and the enemy has %s." % (special[location].name, hero.health, special[location].health)
        combat(special[location])
        return hero.position
    else:
        prompt_text += "You moved."
        return  location

def print_map():
    global special  # make special global so that it can be used for combat decisions
    special = {}
    for item in Character:
        if item.health > 0:
            special[item.position] = item # dictionary, location : creature
    print
    for row in range(9):
        for column in range(8):
            if (row, column) in wall_map:
                print "W", # where wall exists, the character W will print
            elif (row, column) in special:
                print special[(row,column)].rep_char, # by my design, this should return the creature.rep_char ie. bat.rep_char which is b
            else:
                print " ",
        print("")
    print("")

def user_interface(): # requests a move command from the user, then prints all objects current positions
    import os
    import platform
    if platform.system() == 'Windows':
        os.system('cls') # will clear the screen between turns on Windows
    else:
        os.system('clear') # will clear the screen between turns on Linux or OSX

    print_map()

    global prompt_text  # will be determined by user choice, handed to Control Loop for feedback in screen printout.

    print(prompt_text)
    print
    prompt_text = ""  # resets prompt_text for next round after it has been displayed

    if platform.system() == 'Vindows':
        import msvcrt
        print "Which direction would you like to move in? <N E S W>  (" + str(turn_count) + " turns remaining. Q to quit.) : "
        input_char = msvcrt.getwche()
    else:
        input_char = raw_input("Which direction would you like to move in? <N E S W>  (" + str(turn_count) + " turns remaining. Q to quit.) : ")

    input_char = input_char.upper() # input will accept upper or lower case valid directions

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
        raw_input("Press Enter to close game.") # intended to give the user a chance to review the screen before exiting
        import sys
        sys.exit()

    print_map()

def control_loop():  # relies on and counts down the turn_count
    global turn_count
    while turn_count > 0:
        user_interface()
        turn_count -= 1
    else:
        print("You are out of turns.")
        raw_input("Press Enter to close game.") # intended to give the user a chance to review the screen before exiting


control_loop() # will begin the program


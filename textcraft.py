#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Half an hour of hacking to produce the INTJf text adventure!
Programmed on python 2.7. Warning: Untested code ahead.
'''

# Used to call system commands to clear the screen.
import os


# To prevent the user from having to type a lot of choices out, we can use
# these dictionaries to translate back and fourth between shortcuts.
CHOICES = {
    'left': 'left(a)',
    'right': 'right(d)',
    'up': 'forward(w)',
    'down': 'back(s)',
    'pick up': 'pick up(e)',
    'drop': 'drop(q)',
    'exit': 'exit(x)',
}

# The reverse mapping.
SHORTCUTS = {
    'a': 'left',
    'd': 'right',
    'w': 'up',
    's': 'down',
    'e': 'pick up',
    'q': 'drop',
    'x': 'exit',
}


def clear():
    '''
    A very hacky way of clearing the screen.
    '''
    # Get the right command.
    command = 'clear'
    if os.name == 'nt':
        command = 'cls'

    # Run the command.
    os.system(command)


def get_initial_state():
    '''
    A little helper function to return the initial state of the game.
    '''
    # The player's coordinates.
    x = 10
    y = 10

    # A dictionary of rooms. Locations of the room are specified in left, right,
    # top, bottom respectively.
    rooms = {
        'library': {
            'name': 'library',
            'location': (5, 15, 25, 15),
            'treasure': {'key': (10, 20)},
            'doors': [('bottom', 10)]
        },
    }

    return (x, y, rooms)


def get_current_room(x, y, rooms):
    '''
    Gets the current room that the player is in. Returs None if the player
    isn't in a room.
    '''
    for room in rooms.values():
        # Get the location of the room.
        left, right, top, bottom = room['location']

        # Check to see if the player is in the room.
        if x >= left and x <= right and y >= bottom and y <= top:
            return room

    return None


def check_for_treasure(x, y, room):
    '''
    Checks to see if the player is standing on treasure.
    '''
    for name, location in room['treasure'].items():
        # Get the location of the treasure. Location is a tuple, which is a
        # list of fixed length. Since we know it will only ever have an x
        # and a y, we can decode it using the following syntax.
        treasure_x, treasure_y = location

        # Check to see if the player is standing on the treasure.
        if x == treasure_x and y == treasure_y:
            return name


def get_room_movement(x, y, room):
    '''
    Gets movement options if you are in a room.
    '''
    options = []

    # Check the walls of the room.
    left, right, top, bottom = room['location']

    if x > left:
        options.append('left')
    else:
        print 'Hit a wall.'

    if x < right:
        options.append('right')
    else:
        print 'Hit a wall.'

    if y < top:
        options.append('up')
    else:
        print 'Hit a wall.'

    if y > bottom:
        options.append('down')
    else:
        print 'Hit a wall.'

    # See if you can exit a room.
    for wall, position in room['doors']:
        # Check for doors on all sides of the room.
        if wall == 'left' and x == left and y == position:
            options.append('left')
            print 'Found a door.'

        if wall == 'right' and x == right and y == position:
            options.append('right')
            print 'Found a door.'

        if wall == 'bottom' and y == bottom and x == position:
            options.append('down')
            print 'Found a door.'

        if wall == 'top' and y == top and x == position:
            options.append('up')
            print 'Found a door.'

    return options


def get_outdoor_movement(x, y, rooms):
    '''
    Gets movement options if the player is not in a room.
    '''
    # Asssume the player can move everywhere.
    options = ['left', 'right', 'up', 'down']

    for name, room in rooms.items():
        left, right, top, bottom = room['location']

        # Hit the left wall.
        if y >= bottom and y <= top and x == left - 1:
            del options[options.index('right')]
            print 'Hit the %s room.' % name

        # Hit the right wall.
        if y >= bottom and y <= top and x == right + 1:
            del options[options.index('left')]
            print 'Hit the %s room.' % name

        # Hit the top wall.
        if x >= left and x <= right and y == top + 1:
            del options[options.index('down')]
            print 'Hit the %s room.' % name

        # Hit the bottom wall.
        if x >= left and x <= right and y == bottom - 1:
            del options[options.index('up')]
            print 'Hit the %s room.' % name

        # See if you can enter a room.
        for wall, position in room['doors']:
            # Check for doors on all sides of the room.
            if wall == 'left' and x == left - 1 and y == position:
                options.append('right')
                print 'Found a door.'

            if wall == 'right' and x == right + 1 and y == position:
                options.append('left')
                print 'Found a door.'

            if wall == 'bottom' and y == bottom - 1 and x == position:
                options.append('up')
                print 'Found a door.'

            if wall == 'top' and y == top + 1 and x == position:
                options.append('down')
                print 'Found a door.'

    return options


def get_movement_options(x, y, room, rooms):
    '''
    Gets a list of movement options (left, right, up, down).
    '''
    if room:
        return get_room_movement(x, y, room)

    return get_outdoor_movement(x, y, rooms)


def check_state(x, y, rooms):
    '''
    Checks the current state of the game and extracts the current room that
    the player is standing in, and any treasure they may be on. This function
    also returns a list of options that they player can use as a result of
    their current game state.
    '''
    # A list of options that the user can perform this turn.
    options = []

    # If the player is standing on treasure, this variable will be filled.
    treasure = None

    # Check to see if the player is in a room.
    room = get_current_room(x, y, rooms)
    if room:
        print 'You are currently in %s.' % room['name']

        # Check for treasure.
        treasure = check_for_treasure(x, y, room)
        if treasure:
            print 'You are currently standing on %s.' % treasure

            # The user can pick up the treasure.
            options.append('pick up')

    return room, treasure, options


def get_user_input(options):
    '''
    Keep asking the user until they enter a valid option.
    '''
    # Comma separate the options.
    choices = ', '.join([CHOICES[option] for option in options])

    # Prompt the user.
    print 'You can do the following: %s' % choices

    # Keep asking until the user picks a correct option.
    keep_trying = True
    while keep_trying:
        # Get the option.
        option = raw_input('Please type your option: ')

        # Check to make sure the option is valid.
        if option in SHORTCUTS and SHORTCUTS[option] in options:
            keep_trying = False

    return SHORTCUTS[option]


def update_state(x, y, rooms, item, room, treasure, option):
    '''
    Returns new copies of the state objects.
    '''
    if option == 'left':
        x -= 1

    elif option == 'right':
        x += 1

    elif option == 'up':
        y += 1

    elif option == 'down':
        y -= 1

    elif option == 'drop':
        item = None

    elif option == 'pick up':
        # Take the new item.
        item = treasure

        # Remove it from the room.
        name = room['name']
        del rooms[name]['treasure'][treasure]

    return x, y, rooms, item


def main():
    '''
    The main entry point of the program.
    '''
    # Get the initial state of the game.
    x, y, rooms = get_initial_state()

    # Track the item that the user is carrying.
    item = None

    # Loop endlessly until the user decides to stop.
    while True:
        # Clear the screen.
        clear()

        # Print the player's current location.
        print 'You are at: %d, %d' % (x, y)

        # Print the player's item.
        if item:
            print 'You have: %s' % item

        # Check the current state of the game.
        room, treasure, options = check_state(x, y, rooms)

        # If the player is holding an item, they can drop it.
        if item:
            options.append('drop')

        # Get the movement options.
        options += get_movement_options(x, y, room, rooms)

        # The user can always exit.
        options.append('exit')

        # Get the user's input.
        option = get_user_input(options)

        # If the user wants to exit, then exit.
        if option == 'exit':
            return

        # Update the state of the game.
        x, y, rooms, item = update_state(x, y, rooms, item, room,
                                         treasure, option)

        # Print a spacer to make turns clear.
        print


# If the file is called directly, run the main function.
if __name__ == '__main__':
    main()

#################################################################
# FILE : board.py
# WRITER : Naveh Mevorach , navehmevorach , 318284569
# EXERCISE : intro2cs2 ex9 2021
# DESCRIPTION: Board object of 7*7 board
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: none
#################################################################


import numpy as np


class Board:
    """
    The Class is a 7*7 matrix which has cars object init.
    The Class initiated with default size of 7 and empty car objects list
    The class methods are:
    __str__: return a string with the board in a shape of 7*7 matrix using numpy
    cell_list: return a list of all the coordinates on the board
    possible_moves: return a list of tuples with all the possible moves at the moment
    target_location: return a tuple with the target the player should move the Car object too
    cell_content: base on a coordinate the method return either its empty or not
    add_car: Add a new car object to the Board object
    move_car: move a car object into a different coordinate base on the payer command

    """

    def __init__(self):
        self.size = 7
        self.cars = []

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # Reset the board
        display_board = [['#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', '_', '_', '_', '_', '_', '_', '_', '#'],
                         ['#', '_', '_', '_', '_', '_', '_', '_', '#'],
                         ['#', '_', '_', '_', '_', '_', '_', '_', '#'], ['#', '_', '_', '_', '_', '_', '_', '_', '_'],
                         ['#', '_', '_', '_', '_', '_', '_', '_', '#'], ['#', '_', '_', '_', '_', '_', '_', '_', '#'],
                         ['#', '_', '_', '_', '_', '_', '_', '_', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#']]
        for car in self.cars:
            coordinates = car.car_coordinates()
            name = car.get_name()
            for i, j in coordinates:
                display_board[i + 1][j + 1] = name
        return f'{np.array(display_board)}'

    def cell_list(self):
        """ This function returns the coordinates of cells in this board and the winning coordinate as
        The last item
        :return: list of coordinates
        """
        lst = []
        for i in range(self.size):
            for j in range(self.size):
                lst.append((i, j))
        lst.append(self.target_location())
        return lst

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        legal_moves = []

        for car in self.cars:
            car_name = car.get_name()
            move_one, move_two = car.possible_moves().keys()
            move_one_target = car.movement_requirements(move_one)[0]
            move_two_target = car.movement_requirements(move_two)[0]
            if move_one == 'u':
                if move_one_target[0] >= 0 and not self.cell_content(move_one_target):
                    legal_moves.append((car_name, move_one, 'That is a legal move'))
            if move_one == 'l':
                if move_one_target[1] >= 0 and not self.cell_content(move_one_target):
                    legal_moves.append((car_name, move_one, 'That is a legal move'))
            if move_two == 'd':
                if move_two_target[0] <= 6 and not self.cell_content(move_two_target):
                    legal_moves.append((car_name, move_two, 'That is a legal move'))
            if move_two == 'r':
                if move_two_target[1] <= 6 and not self.cell_content(move_two_target):
                    legal_moves.append((car_name, move_two, 'That is a legal move'))
        return legal_moves

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return 3, 7

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        # Iterate through all the cars on the board
        for car in self.cars:
            # iterate thorough all the coordinates of the current car
            for car_coordinate in car.car_coordinates():
                # If on of the coordinate is equal to the given coordinate it means
                # The cell isn't empty and the method will return the car name which the cell is taken by
                if car_coordinate[0] == coordinate[0] and car_coordinate[1] == coordinate[1]:
                    return car.get_name()
        # In case the cell is empty return None
        return

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Get the car coordinates
        coordinates = car.car_coordinates()
        # Get all the car names the currently on the board
        all_existing_car_names = [car.get_name() for car in self.cars]
        for coordinate in coordinates:
            # Check if the coordinate is in the board range
            if coordinate[0] > self.size - 1 or coordinate[1] > self.size - 1 or coordinate[0] < 0 or \
                    coordinate[1] < 0:
                return False
            # Check if the name already exists on the board
            if car.get_name() in all_existing_car_names:
                return False
            # Check if there a car in one of the cells already and if there is - the car wont be added
            if self.cell_content(coordinate):
                return False
        self.cars.append(car)
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        # TODO - Check if there aren't any cars on the board what should the method should return
        # Check if there any cars on the board
        if not self.cars:
            return False
        # Get the car by it's name
        car_to_move_lst = [car for car in self.cars if car.get_name() == name]
        car_to_move = car_to_move_lst[0]
        # Check if the move suit the orientation
        direction_one, direction_two = car_to_move.possible_moves().keys()
        if direction_one in 'lr' and direction_two in 'lr' and movekey in 'ud':
            return False
        if direction_one in 'ud' and direction_two in 'ud' and movekey in 'lr':
            return False
        # Get the destination
        moving_dest = car_to_move.movement_requirements(movekey)[0]
        # Check if the destination is a valid coordinate according to the board
        if moving_dest not in self.cell_list():
            return False
        # Check if the destination is empty
        if self.cell_content(moving_dest):
            return False
        # Move the car
        if not car_to_move.move(movekey):
            return False
        return True

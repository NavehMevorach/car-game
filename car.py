#################################################################
# FILE : car.py
# WRITER : Naveh Mevorach , navehmevorach , 318284569
# EXERCISE : intro2cs2 ex9 2021
# DESCRIPTION: Car object with length of 2-4, ordination of 0,1, name and location
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: none
#################################################################


class Car:
    """
    The class is initiated with name: A string representing the car's name,
    length: A positive int representing the car's length.
    location: A tuple representing the car's head (row, col) location
    orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)

    The Car methods:
    car_coordinates: Return a list of coordinates the car is in
    possible_move: Return which direction the car can move to (u/d, l/r)
    movement_requirements: Return which coordinate must be empty based on movekey
    move: Change the car coordinates
    get_name: return the car object name
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.name = name
        self.length = length
        self.location = location
        self.orientation = orientation

    def car_coordinates(self):
        """
        The method checks wither the car is horizontal or vertical and iterate find all the other values of the car
        :return: A list of coordinates the car is in
        """
        coordinates = []
        # Check the car direction
        if self.orientation == 1:
            # add 1 to each item in self.location[1]
            for i in range(self.length):
                coordinates.append((self.location[0], self.location[1] + i))
        else:
            # add 1 to each item in self.location[0]
            for i in range(self.length):
                coordinates.append((self.location[0] + i, self.location[1]))
        return coordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        return {'u': 'Moves the chosen car up',
                'd': 'Moves the chosen car down'
                } if self.orientation == 0 else {'l': 'Moves the chosen car left',
                                                 'r': 'Moves the chosen car right'
                                                 }

    def movement_requirements(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        # Check the car direction
        if self.orientation == 0:
            # check if movekey is u/d
            if movekey == 'u':
                # We go up so the row above should be empty
                return [(self.location[0] - 1, self.location[1])]
            if movekey == 'd':
                # We go down so the row below should be empty
                return [(self.location[0] + self.length, self.location[1])]
        elif self.orientation == 1:
            # check if movekey is r/l
            if movekey == 'r':
                # We go right so the cell above should be empty
                return [(self.location[0], self.location[1] + self.length)]
            if movekey == 'l':
                # We go up so the cell below should be empty
                return [(self.location[0], self.location[1] - 1)]

    def move(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        # Check if the movekey is a possible move for that car
        if movekey in self.possible_moves().keys():
            # Change the car location settings
            if movekey == 'u':
                self.location = self.location[0] - 1, self.location[1]
            elif movekey == 'd':
                self.location = self.location[0] + 1, self.location[1]
            elif movekey == 'l':
                self.location = self.location[0], self.location[1] - 1
            # Means its d
            else:
                self.location = self.location[0], self.location[1] + 1
            return True
        return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.name

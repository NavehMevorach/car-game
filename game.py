#################################################################
# FILE : game.py
# WRITER : Naveh Mevorach , navehmevorach , 318284569
# EXERCISE : intro2cs2 ex9 2021
# DESCRIPTION: Main function and the Game object
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: none
#################################################################

class Game:
    """
    A Game object (rush hour game)
    The Game is initiated with the game rules such as: car length, valid car name etc.
    The object methods are:
    __check_valid_input: Check if the user enter a valid input
    __single_turn: one iteration of the game
    __set_valid_name: Set the valid car name in each turn
    play: Initiate the game and run until its over
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.board = board
        self.min_car_len = 2
        self.max_car_len = 4
        self.valid_cars_names = self.__set_valid_name()
        self.valid_directions = ['u', 'd', 'l', 'r']
        self.stop = '!'

    def __set_valid_name(self):
        valid_names = set([tup[0] for tup in self.board.possible_moves()])
        if valid_names:
            return valid_names
        return ''

    def __check_valid_input(self, action):
        """
        The method check if the player wrote a valid input
        If the input is valid the method check if that is indeed a possible move and if the name is a Valid car name
        Only if all of these are valid the method return True
        :param action: a string
        :return: True upon success,  False otherwise
        """
        # Check if the input is in the format (Y,d)
        if len(action) != 3 or action[2] not in self.valid_directions or action[1] != ',':
            return False
        # Check if the car he want to move is in the current valid car names
        if action[0] not in self.valid_cars_names and action[2] != 'r':
            return False
        # Check if the user want to move to the winning cell which in that case it valid
        winning_cell = self.board.cell_content((3, 6))
        if winning_cell == action[0] and action[2] == 'r':
            return True
        legal_moves = self.board.possible_moves()
        # Only if the move is in legal moves, return true
        for tup in legal_moves:
            if action[0] == tup[0] and action[2] == tup[1]:
                return True
        return False

    def __single_turn(self):
        """
        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.
        """
        print(self.board)
        user_action = input('Which car do you want to move and in what direction? \n'
                            f'Possible cars name are: {self.valid_cars_names} \n'
                            'Possible Directions are: u,d,l,r \n'
                            'Your input should look like: Y,d')
        if user_action == self.stop:
            return 'END'
        while not self.__check_valid_input(user_action):
            user_action = input('Invalid action! \n'
                                'Which car do you want to move and in what direction? \n'
                                f'Possible cars name are: {self.valid_cars_names} \n'
                                'Possible Directions are: u,d,l,r \n'
                                'Your input should look like: Y,d')
            if user_action == '!':
                return 'END'
        color, direction = user_action.split(',')
        # Move the car
        self.board.move_car(color, direction)
        # Check if win
        if self.board.cell_content(self.board.target_location()):
            return "WIN"
        self.valid_cars_names = self.__set_valid_name()

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        playing = True
        while playing:
            one_turn = self.__single_turn()
            # Check if the user wants to stop playing
            if one_turn == 'END':
                playing = False
            # Check if win
            if one_turn == 'WIN':
                print(self.board)
                playing = False


def load_cars(json, board):
    """
    A helper function to load all the valid cars into the board
    :param json: a Dictionary with all the cars objects
    :param board: a Board Object
    """
    # Iterate through all cars
    for name, details in json.items():
        # Check if the car has a valid name
        if name not in ['Y', 'G', 'R', 'B', 'O', 'W']:
            continue
        # Check if the details is list with 3 items
        if not isinstance(details, list) or len(details) != 3:
            continue
        # Unpack details after we verified its a list
        leng, loc, orien = details
        # Check if the length is valid
        if not isinstance(leng, int) or not (2 <= leng <= 4):
            continue
        # Check if the location is valid
        if not isinstance(loc, list) or not (
                isinstance(loc[0], int) and 0 <= loc[0] <= 6 and isinstance(loc[1], int) and 0 <= loc[1] <= 6):
            continue
        # Check if the orientation is valid
        if orien != 1 and orien != 0:
            continue
        # In case the car is valid, add it to the board
        board.add_car(Car(name, leng, tuple(loc), orien))


if __name__ == "__main__":
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    import sys
    from helper import load_json
    from board import Board
    from car import Car

    # Create Board
    new_board = Board()
    # Load the Json file
    json = load_json(sys.argv[1])
    # Create all the cars and place them on the board
    load_cars(json, new_board)
    # Load the game with the updated board
    game = Game(new_board)
    game.play()

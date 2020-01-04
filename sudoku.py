from copy import deepcopy

class SudokuGame(object):
    # object to hold the state of the game as well as game logic

    def __init__(self, board_file_name):
        self.board_id = board_file_name
        self.starting_board = self.initialize_board(board_file_name)
        self.game_board = deepcopy(self.starting_board)
        self.game_over = False

    def initialize_board(self, board_file_name):
        board = []
        with open('boards/' + board_file_name, 'r') as board_file:
            for line in board_file:
                line = line.strip()
                assert(len(line) == 9), 'Row lengths must be 9.'
                row = []
                for char in line:
                    assert(char.isdigit()), 'Must have only digits in input.'
                    row.append(int(char))
                board.append(row)
        assert(len(board) == 9), 'Must have 9 rows total.'
        return board
    
    def reset_board(self):
        self.game_board = deepcopy(self.starting_board)

    def check_win(self):
        # first check the rows
        for row in self.game_board:
            if set(row) != set(range(1, 10)):
                return False
        # second check the columns
        for col in range(9):
            column = [self.game_board[row][col] for row in range(9)]
            if set(column) != set(range(1, 10)):
                return False
        # lastly check the squares
        for row_block in range(3):
            for col_block in range(3):
                square = [self.game_board[row][col] 
                            for row in range(row_block * 3, (row_block + 1) * 3)
                            for col in range(col_block * 3, (col_block + 1) * 3)
                        ]
                if set(square) != set(range(1, 10)):
                    return False
        return True
from tkinter import Tk, Label, Frame, Canvas, BOTH, LEFT, RIGHT, Button
from sudoku import SudokuGame
from os import listdir
import random

MARGIN = 30
SQUARE = 50
HEIGHT = MARGIN * 2 + SQUARE * 9
WIDTH = HEIGHT

boards = listdir('boards')

class SudokuGUI(Frame):
    # A way to group and organize all widgets needed for our GUI

    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        Frame.__init__(self, parent)

        # these variables are used to keep track of which square is selected
        self.row = -1
        self.col = -1

        self.pack(fill=BOTH)

        # what we use to draw the sudoku grid
        self.canvas = Canvas(self, width=WIDTH - MARGIN, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=LEFT)

        title = Label(self, text='Sudoku', font=(None, 40))
        title.pack()

        description_text = ('The goal of Sudoku is to input numbers such that each row, column, '
                            'and 3x3 sub-grid have the numbers 1 through 9 appearing exactly once. '
                            'There should only be 1 unique solution for each grid.')
        description_label = Label(self, text=description_text, wraplength=300, justify=LEFT)
        description_label.pack()

        instructions_text = ('Click on a square to highlight it and input a number. You can save '
                            'possible numbers in a square by just adding more numbers to the square. '
                            'When you are finished and there is only one number per square, click on '
                            'the "Check Answer" button to verify your solution. If you get stuck and/or '
                            'want to start over, click the "Reset Board" button which will reset the board '
                            'to its starting state. Click on the "New Board" button to get a random new puzzle. '
                            'Lastly, click on the "Solve" button to see an interactive demo of an AI algorithm '
                            'solve the puzzle from the starting grid.')
        instructions_label = Label(self, text=instructions_text, wraplength=300, justify=LEFT, pady=10)
        instructions_label.pack()
        
        self.draw_grid()
        self.draw_numbers()

        # initialize buttons here
        check_answer_button = Button(self, text='Check Answer', command=self.check_win)
        check_answer_button.pack()

        reset_board_button = Button(self, text='Reset Board', command=self.reset_grid)
        reset_board_button.pack()

        new_board_button = Button(self, text='New Board', command=self.new_board)
        new_board_button.pack()

        solve_button = Button(self, text='Solve', command=self.solve)
        solve_button.pack()

    def draw_grid(self):
        for i in range(10):
            if i % 3 == 0:
                color = 'black'
            else:
                color = 'grey'
            
            # drawing veritcal lines
            start_x = MARGIN + i * SQUARE
            start_y = MARGIN
            end_x = start_x
            end_y = HEIGHT - MARGIN
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color)

            # drawing horizontal lines
            start_x = MARGIN
            start_y = MARGIN + i * SQUARE
            end_x = WIDTH - MARGIN
            end_y = start_y
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color)

    def draw_numbers(self):
        # we call this every time a new number is added so we have to delete the previous numbers
        self.canvas.delete('numbers')
        for row in range(9):
            for col in range(9):
                value = self.game.game_board[row][col]
                if value != 0:
                    if self.game.starting_board[row][col] == 0:
                        color = 'blue'
                    else:
                        color = 'black'
                    x = MARGIN + (row * SQUARE) + (SQUARE / 2)
                    y = MARGIN + (col * SQUARE) + (SQUARE / 2)
                    self.canvas.create_text(x, y, text=value, tag='numbers',fill=color)
                

    def check_win(self):
        pass

    def reset_grid(self):
        pass

    def new_board(self):
        pass
    
    def solve(self):
        pass


if __name__ == "__main__":
    window = Tk()
    window.title('Sudoku GUI')
    window.geometry('%dx%d' % (WIDTH + 350, HEIGHT))

    game = SudokuGame(random.choice(boards))
    gui = SudokuGUI(window, game)
    window.mainloop()
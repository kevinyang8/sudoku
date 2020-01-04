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
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, highlightthickness=0)
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

        # bind key inputs here
        self.canvas.bind('<Button-1>', self.cell_clicked)
        self.canvas.bind('<Key>', self.key_pressed)
        self.canvas.bind('<BackSpace>', self.delete_number)
        self.canvas.bind('<Escape>', self.close_circle)

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
                    x = MARGIN + (col * SQUARE) + (SQUARE / 2)
                    y = MARGIN + (row * SQUARE) + (SQUARE / 2)
                    self.canvas.create_text(x, y, text=value, tag='numbers', fill=color)
    
    def draw_box(self):
        self.canvas.delete('box')
        if self.row >= 0 and self.col >= 0:
            top_x = MARGIN + self.col * SQUARE
            top_y = MARGIN + self.row * SQUARE
            bottom_x = MARGIN + (self.col + 1) * SQUARE
            bottom_y = MARGIN + (self.row + 1) * SQUARE
            self.canvas.create_rectangle(top_x, top_y, bottom_x, bottom_y, tags='box', outline='red')

    def cell_clicked(self, event):
        if self.game.game_over:
            return

        x = event.x
        y = event.y

        # check to see if the click is in the grid
        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            self.canvas.focus_set()
            row = (y - MARGIN) // SQUARE
            col = (x - MARGIN) // SQUARE

            # if current cell is selected already, deselect it.
            # also don't select cells that weren't already prefilled
            if self.row == row and self.col == col:
                self.row = -1
                self.col = -1
            elif self.game.starting_board[row][col] == 0:
                self.row = row
                self.col = col
        self.draw_box()
        
    def key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in '123456789':
            self.game.game_board[self.row][self.col] = int(event.char)
            self.draw_numbers()
            self.draw_box()

    def delete_number(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0:
            self.game.game_board[self.row][self.col] = 0
            self.draw_numbers()
            self.draw_box()
    
    def close_circle(self, event):
        self.canvas.delete('check_win')
        # set back to false if isn't actually a win
        if not self.game.check_win():
            self.game.game_over = False

    def check_win(self):
        # always set to true so can't interact with board when this is displayed
        self.game.game_over = True 
        if self.game.check_win():
            text = '         Victory! \n Press Esc to close.'
            color = 'light green'
            outline = 'orange'
        else:
            text = 'Something is not correct. \n     Press Esc to close.'
            color = 'indian red'
            outline = 'purple'

        top_x = MARGIN + SQUARE * 2
        top_y = top_x
        bottom_x = MARGIN + SQUARE * 7
        bottom_y = bottom_x
        self.canvas.create_oval(top_x, top_y, bottom_x, bottom_y, tag='check_win', fill=color, outline=outline)

        x = MARGIN + (4 * SQUARE) + (SQUARE / 2)
        y = x
        self.canvas.create_text(x, y, tag='check_win', text=text, fill='white')
        self.canvas.focus_set()

    def reset_grid(self):
        self.canvas.delete('check_win')
        self.game.reset_board()
        if self.game.game_over:
            self.game.game_over = False
        self.row = -1
        self.col = -1
        self.draw_numbers()
        self.draw_box()

    def new_board(self):
        self.canvas.delete('check_win')
        # makes sure a different board is selected from the current one
        selected_board = random.choice(boards)
        if selected_board == self.game.board_id:
            self.new_board()
        else:
            self.game = SudokuGame(selected_board)
            self.reset_grid()
                
    def solve(self):
        pass


if __name__ == "__main__":
    window = Tk()
    window.title('Sudoku GUI')
    window.geometry('%dx%d' % (WIDTH + 350, HEIGHT))

    game = SudokuGame(random.choice(boards))
    gui = SudokuGUI(window, game)
    window.mainloop()
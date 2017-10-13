from tkinter import *

from Node import *


class App:

    def __init__(self, master):

        self.root = NumberNode(0)
        self.paren_depth = 0
        self.new_command = ''
        self.runningValue = ''
        self.buttons = []

        frame = Frame(master)
        frame.pack()

        self._layout_buttons(frame)

    def _add_normal_button(self, frame, text, row, column):
        button = Button(frame, text=text,
                        command=self._on_button(text), width=3,
                        font=("Arial", 16))
        button.grid(row=row, column=column, sticky=N+S+E+W)
        self.buttons.append(button)

    def _layout_buttons(self, frame):

        row_pad = 1
        col_pad = 1

        # pad top and sides of display
        for n in range(row_pad):
            Label(frame, text='', width=18)\
                .grid(row=n, column=0+col_pad, columnspan=4)

        for n in range(col_pad):
            Label(frame, text='', width=3).grid(row=row_pad, column=0)
            Label(frame, text='', width=3).grid(row=row_pad, column=4+col_pad)

        top_row = row_pad

        # first row is the error state. it just says "ERR" when there's an error
        self.error_state = Label(frame, text='', width=18, anchor=W)
        self.error_state.grid(row=0+top_row, column=0+col_pad, sticky=N+S+E+W, columnspan=4)

        top_row += 1

        # next row is the current evaluation
        self.show = StringVar()
        self.show.set('')
        self.display = Label(frame, textvariable=self.show, anchor=W, width=18,
                             borderwidth=3, relief=GROOVE,
                             font=("Arial", 16))
        self.display.grid(row=0+top_row, column=0+col_pad, columnspan=4, sticky=N+S+E+W)

        top_row += 1

        # there's a whole row for extra buttons, like "CLEAR"

        button = Button(frame, text='C',
                        command=self._clear, width=3,
                        font=("Arial", 16))
        button.grid(row=0+top_row, column=0+col_pad, sticky=N+S+E+W)
        self.buttons.append(button)

        self._add_normal_button(frame, '%', 0+top_row, 1+col_pad)
        self._add_normal_button(frame, '^', 0+top_row, 2+col_pad)

        top_row += 1

        # put in the numbers, 1-9
        for n in range(9):
            self._add_normal_button(frame, str(n+1), top_row+2-int(n/3), (n%3)+col_pad)

        # right below the numbers, we've got 0, (, and ).
        self._add_normal_button(frame, '0', 3+top_row, 0+col_pad)
        self._add_normal_button(frame, '(', 3+top_row, 1+col_pad)
        self._add_normal_button(frame, ')', 3+top_row, 2+col_pad)

        # next row: . and =
        self._add_normal_button(frame, '.', 4+top_row, 0+col_pad)

        # directly create this; we need to adjust the columnspan
        button = Button(frame, text='=',
                        command=self._on_compute, width=3, font=("Arial", 16))
        button.grid(row=4+top_row, column=1+col_pad, columnspan=3, sticky=N+S+E+W)

        # put the operators along the right side of the numbers.
        operator_row = top_row
        for op in ('+', '-', 'x', '/'):
            self._add_normal_button(frame, op, operator_row, 3+col_pad)
            operator_row += 1

        # tack a padding row along the bottom.
        Label(frame, text='').grid(row=5+top_row, column=0+col_pad)

    def _clear(self):
        self.root = NumberNode(0)
        self.new_command = ''
        self.show.set('')
        self.error_state.configure(text='')

    def _on_button(self, n):
        def do():
            self.show.set(self.show.get() + n)
            self.new_command += n
            self.error_state.configure(text='')

        return do

    def _on_compute(self):
        self.root, self.paren_depth = processCommand(self.root, self.paren_depth, self.new_command)
        self.new_command = ''

        try:
            self.runningValue = self.root.evaluate()
        except:
            self.error_state.configure(text='ERR', fg='red')
            self.root = NumberNode(0)

        # Don't "overcollapse": if paren_depth > 0, don't evaluate the contents of those parentheses
        self.root = self.root.collapse(self.paren_depth)
        # Show the current "running" tree, to which the user may append operations.
        self.show.set(self.root.squawk2())


root = Tk()
app = App(root)
root.mainloop()
root.destroy()

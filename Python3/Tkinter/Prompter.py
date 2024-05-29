#!/usr/bin/python3
from tkinter import *

# Note: Project now at https://github.com/soft9000/Prompter9000

# Mission: Create a way to query a user for command-line
# values. Mission statement implies the encapsulation of
# a GUI paradigm. Here is how to do so using tkinter under
# Python 3.

''' Prompter: Graphically get a dictionary of command-line
strings from a user. Dictionary result is empty when the
`cancel` button has been pressed, else the results
will contain the tag-value pairing (i.e. Dictionary keys
match the fields requested, to get the user's response
for each field.)
'''
class Prompter:
    def __init__(self):
        self._dict = None
        self._isOk = None
        self.last_row = None
        self.tk = None

    def _okay(self):
        self._isOk = True
        self.tk.quit()

    def _cancel(self):
        self._isOk = False
        self.tk.quit()

    @staticmethod
    def begin(*fields, title="Input"):
        ''' Create the frame, add the title, as well as the input fields.'''
        from collections import OrderedDict
        self = Prompter()
        self.tk = Tk()

        self._dict = OrderedDict()

        if title:
            self.tk.title(title)

        self.last_row = 0
        # zFields (A Label, plus an Entry, in a grid layout)
        for ref in fields:
            obj = Label(master=self.tk, text=str(ref))
            obj.grid(row=self.last_row, column=0)

            obj = Entry(master=self.tk, bd=5)
            obj.grid(row=self.last_row, column=1)

            self._dict[ref]=obj
            self.last_row += 1
        return self

    @staticmethod
    def end(prompter):
        ''' Add the closing buttons, center, and pack the Frame.'''
        if prompter.last_row is None:
            return False
        if isinstance(prompter, Prompter) is False:
            return False
        # zButtons (A Frame in the grid, plus the properly-centered pair of buttons)
        bottom = Frame(prompter.tk)
        bottom.grid(row=prompter.last_row, columnspan=2)
        btn = Button(bottom, text="Okay", command=prompter._okay)
        btn.pack(side=LEFT, pady=12)

        btn = Button(bottom, text="Cancel", command=prompter._cancel)
        btn.pack(side=RIGHT, padx=10)

        # zCenter (Close enough to make no odds?)
        width = prompter.tk.winfo_screenwidth()
        height = prompter.tk.winfo_screenheight()
        x = (width - prompter.tk.winfo_reqwidth()) / 2
        y = (height - prompter.tk.winfo_reqheight()) / 2
        prompter.tk.geometry("+%d+%d" % (x, y))
        return True

    def show(self):
        ''' Display the dialog - extract the results.'''
        from collections import OrderedDict
        self.tk.mainloop()
        try:
            results = OrderedDict()
            if self._isOk is not True:
                return results

            for ref in self._dict.keys():
                results[ref] = (self._dict[ref]).get()
            return results
        finally:
            try:
                self.tk.destroy()
                # self.tk = None
            except:
                pass


    @staticmethod
    def prompt(*fields, title="Input"):
        ''' Basic mission statement completed. '''
        self = Prompter.begin(*fields, title=title)
        if Prompter.end(self) is False:
            raise Exception("AddButtons: Unexpected Error.")
        return self.show()


if __name__ == "__main__":
    import sys
    cmd_name = sys.argv[0]
    if len(sys.argv) > 1:
        params = sys.argv[1:]
    else:
        params = "This", "Isa", "TEST?" 

    results = Prompter.prompt(*params, title=cmd_name)
    if not results:
        print("Cancelled")
    else:
        print(results)
        for ref in results:
            print(ref, '=', results[ref], '|', sep='', end='')
            print()

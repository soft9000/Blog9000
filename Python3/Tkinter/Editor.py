#!/usr/bin/python3
from tkinter import *
from collections import OrderedDict
# Mission: Create a way to edit the subject & content
# of a message.

class EditorParams:
    EDITBOX = "ZEDIT:"    
    def __init__(self, *fields):
        self.params = OrderedDict()
        for field in fields:
            self.params[field] = ''
        self.params[EditorParams.EDITBOX] = ''
        

class Editor:
    def __init__(self):
        self._dict = None
        self._isOk = None
        self.last_row = None
        self.text = None
        self.eparams = None

    def _okay(self):
        self._isOk = True
        self.tk.quit()

    def _cancel(self):
        self._isOk = False
        self.tk.quit()

    @staticmethod
    def begin(eparams, title="Input"):
        if not isinstance(eparams, EditorParams):
            raise Exception("begin: Instance of EditorParams expected.")
        
        ''' Create the frame, add the title, as well as the input fields.'''
        self = Editor()
        self.tk = Tk()

        self.eparams = eparams
        if self.eparams.params[EditorParams.EDITBOX] is None:
            self.eparams.params[EditorParams.EDITBOX] = ""

        self._dict = OrderedDict()

        if title:
            self.tk.title(title)

        self.last_row = 0
        # zFields (A Label, plus an Entry, in a grid layout)
        for ref in self.eparams.params:
            if ref == EditorParams.EDITBOX:
                continue
            obj = Label(master=self.tk, text=str(ref))
            obj.grid(row=self.last_row, column=0)

            if self.eparams.params[ref] is None:
                self.eparams.params[ref] = ''

            obj = Entry(master=self.tk, bd=5, width=50)
            obj.grid(row=self.last_row, column=1)
            obj.insert(0, self.eparams.params[ref])

            self._dict[ref]=obj
            self.last_row += 1
        return self

    @staticmethod
    def end(prompter):
        ''' Add the closing edit area, buttons, center, and pack the Frame.'''
        if prompter.last_row is None:
            return False
        if isinstance(prompter, Editor) is False:
            return False

        # zNotepad
        bottom = Frame(prompter.tk)
        bottom.grid(row=prompter.last_row, columnspan=2)
        prompter.text = Text(bottom, height=25, width=50)
        prompter.text.pack()
        prompter.text.insert(END, prompter.eparams.params[EditorParams.EDITBOX])
        prompter.last_row += 1

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
        from collections import OrderedDict
        self.tk.mainloop()
        try:
            results = OrderedDict()
            if self._isOk is not True:
                return results

            for ref in self._dict.keys():
                results[ref] = (self._dict[ref]).get()
            results[EditorParams.EDITBOX] = self.text.get("1.0", "end-1c")
            return results
        finally:
            try:
                self.tk.destroy()
            except:
                pass

    @staticmethod
    def prompt(*fields, title="Input"):
        ''' Basic mission statement completed. '''
        self = Editor.begin(*fields, title=title)
        if Editor.end(self) is False:
            raise Exception("AddButtons: Unexpected Error.")
        return self.show()


if __name__ == "__main__":
    # Here is how we would use the Editor from a Console Program:
    order = EditorParams("Preamble:", "Subject:")
    order.params["Subject:"] = "of a modern ..."
    order.params["Preamble:"] = "I am the very model ..."
    order.params[EditorParams.EDITBOX] = "Python interface."
    results = Editor.prompt(order, title="Just Do It!")
    if not results:
        print("Cancelled")
    else:
        print(results)
        for ref in results:
            print(ref, '=', results[ref], '|', sep='', end='')
            print()

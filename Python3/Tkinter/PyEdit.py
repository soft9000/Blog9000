#!/usr/bin/python3
from tkinter import *
from tkinter import font
from collections import OrderedDict
# File: PyEdit.py
# Mission: Graphically edit / exchange eval()uatable
# dictionaries. Record if [Okay] or [Cancel] was selected.

# Source:
# https://github.com/soft9000/Blog9000


class EditDict:
    '''Graphically exchange a dictionary of strings with a user. Dictionary keys match fields requested. Font, size, and label allignment can be selected upon construction as per Tkinter definition.

G.U.I Usage:
===========
from Prompter9000.PyEdit import *
params = {"NAME":'My', "PHONE":'123-456', "EMAIL":'a.Geekbo@zbobo.com'}
EditDict.edit(params)

NOTE: Dictionary results will be returned ONLY IF the data was changed. Otherwise an empty dictionary will be returned.

Console Usage:
=============    
python PyEdit.py "{'NAME': 'My', 'PHONE': '123-456', 'EMAIL': 'a.Geekbo@zbobo.com'}"{'NAME': 'My', 'PHONE': '123-456', 'EMAIL': 'a.Geekbo@zbobo.com', '__btn_ok': True}

NOTES: Please encode your dictionary as a single str(dict()) parameter when using the CLI. Results will be returned as a dictionary of strings. A __btn_ok key is added and will be `True` if [Okay] was selected, else is `False` if user pressed [Cancel].
'''
    def __init__(self, a_dict, font_size=16, font_name='TkFixedFont', align='e'):
        '''
        Initialize fileds. Optional horizontal alignments
        are n, s, [e], w ... Tk's `sticky` grid options.
        '''
        self._font_default_size = font_size
        self._font_default_name = font_name
        self._align = align 
        self._data = OrderedDict(a_dict)
        self._dict = OrderedDict()
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
    def begin(fields, title="Input",
             font_size=16, font_name='TkFixedFont',
             align='e'):
        ''' Create the frame, add the title, as well as the input fields.'''
        self = EditDict(fields, font_size, font_name, align)
        self.tk = Tk()

        if title:
            self.tk.title(title)
        self._font_default = font.nametofont(self._font_default_name)
        self._font_default.configure(size=self._font_default_size)
        self._font_default.configure(weight=font.NORMAL)
        self._font_bold = font.nametofont(self._font_default_name)
        self._font_bold.configure(size=self._font_default_size)
        self._font_bold.configure(weight=font.BOLD)

        self.last_row = 0
        # zFields (A Label, plus an Entry, in a grid layout)
        for ref in self._data:
            a_prompt = str(ref) + ": "
            obj = Label(master=self.tk,
                        text=a_prompt,
                        font=self._font_bold)
            obj.grid(row=self.last_row, column=0,
                     padx=4, sticky=self._align)

            a_value = self._data[ref]
            if not a_value:
                a_value = ''
            obj = Entry(master=self.tk, bd=5,
                        font=self._font_default)
            obj.insert(0, a_value)
            obj.grid(row=self.last_row, column=1)

            self._dict[ref]=obj
            self.last_row += 1
        return self

    @staticmethod
    def end(prompter):
        ''' Add the closing buttons, center, and pack the Frame.'''
        if prompter.last_row is None:
            return False
        if isinstance(prompter, EditDict) is False:
            return False
        # zButtons (A Frame in the grid, plus the properly-centered pair of buttons)
        bottom = Frame(prompter.tk)
        bottom.grid(row=prompter.last_row, columnspan=2)
        btn = Button(bottom, text="Okay",
                     command=prompter._okay,
                     font=prompter._font_bold)
        btn.pack(side=LEFT, pady=12)

        btn = Button(bottom, text="Cancel",
                     command=prompter._cancel,
                     font=prompter._font_bold)
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
            if not self._isOk:
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
    def edit(fields, title="Input",
             font_size=16, font_name='TkFixedFont',
             align='e'):
        ''' Basic mission statement completed. '''
        self = EditDict.begin(fields, title,
                              font_size,
                              font_name,
                              align=align)
        if EditDict.end(self) is False:
            raise Exception("AddButtons: Unexpected Error.")
        return self.show()


if __name__ == "__main__":
    import sys
    import os
    cmd_name = sys.argv[0]
    if cmd_name.find('\\'):
        cmd_name = cmd_name.split('\\')[-1]
    if cmd_name.find('/'):
        cmd_name = cmd_name.split('/')[-1]
    
    sz = len(sys.argv)
    params = {"NAME":'R.A. Geekbo', "PHONE":'123-456-7890', "EMAIL":'a.Geekbo@zbobo.com'}
    if sz > 2:
        print("Input: One stringified dictionary as a parameter, please.")
        print(f"Example: \"{str(params)}\"")
        print("\t(i.e: surrounding quotations are os-required)")
        quit()
    elif sz == 2:
        data = sys.argv[1:][0]
        params = eval(data)

    results = EditDict.edit(params, title=cmd_name)
    if not results:
        params['__btn_ok'] = False
        print(params)
    else:
        results['__btn_ok'] = True
        print(dict(results))
    print()

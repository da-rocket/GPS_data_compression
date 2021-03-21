from tkinter import *
from tkinter.filedialog import Directory
from tkinter.filedialog import askopenfilename

def makeFormRow(parent, label, width=15, browse=True, extend=False):
    var = StringVar()
    row = Frame(parent)
    lab = Label(row, text=label + '?', relief=RIDGE, width=width)
    ent = Entry(row, relief=SUNKEN, textvariable=var)
    row.pack(fill=X)
    lab.pack(side=LEFT)
    ent.pack(side=LEFT, expand=YES, fill=X)
    if browse:
        btn = Button(row, text='browse...')
        btn.pack(side=RIGHT)
        if not extend:
            btn.config(command=
                       lambda: var.set(Directory(title='Select folder').show() or var.get()))
        else:
            btn.config(command=
                       lambda: var.set(var.get() + ' ' + askopenfilename()))
    return var

def makeFormRowInt(parent, label, value='', width=15):
    var = IntVar()
    row = Frame(parent)
    lab = Label(row, text=label + '?', relief=RIDGE, width=width)
    ent = Entry(row, relief=SUNKEN, textvariable=var)
    row.pack(fill=X)
    lab.pack(side=LEFT)
    ent.pack(side=LEFT, expand=YES, fill=X)
    var.set(value or var.get())
    return var

def makeFormRowFloat(parent, label, value='', width=15):
    var = DoubleVar()
    row = Frame(parent)
    lab = Label(row, text=label + '?', relief=RIDGE, width=width)
    ent = Entry(row, relief=SUNKEN, textvariable=var)
    row.pack(fill=X)
    lab.pack(side=LEFT)
    ent.pack(side=LEFT, expand=YES, fill=X)
    var.set(value or var.get())
    return var

def fetchResults():
    vars = {'var1': var1.get(), 'var2': var2.get(), 'var3': var3.get(),
            'var4': var4.get(), 'var5': var5.get(), 'var6': var6.get()}
    for key in vars:
        print(key, "=>", vars[key])

if __name__ == '__main__':
    win = Toplevel()
    win.title('Enter settings')
    vars = {}
    var1 = makeFormRow(win, label='GPS files')
    var2 = makeFormRow(win, label='Output folder')
    var3 = makeFormRowInt(win, label='Integer min', value=10)
    var4 = makeFormRowInt(win, label='Integer max', value=20)
    var5 = makeFormRowFloat(win, label='Float min', value=10.5)
    var6 = makeFormRowFloat(win, label='Float max', value=20.37)

    Button(win, text='Run program', command=fetchResults).pack()

    mainloop()
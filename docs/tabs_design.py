from tkinter import ttk
from tkinter import *
from gps_formrows import *
from guimaker import *
# from test import *
from tkinter.messagebox import *

# general configuration
try:
    import config
    cfgs = config.__dict__
except Exception as e:                                      # define in client app directory
    print(e)


class myShell(GuiMakerWindowMenu):
    variables = {}

    mode = ['Application', 'Calibration']
    attr = ['Length', 'Altitude', 'Speed']

    def start(self):
        self.menuBar = [('File', 0,
             [('Settings', 0, self.onSettings),
              ('Run', 0, self.onRun)])]

    def onSettings(self):
        win = Toplevel()
        win.title('Program settings')
        win.minsize(300, 300)
        tabControl = ttk.Notebook(win)
        tabControl.config(height=300, width=300)

        # Tab 1: data cleaning
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='Data cleaning')
        self.tab1_var1 = makeFormRowFloat(tab1, 'Min altitude', cfgs['altMin'])
        self.tab1_var2 = makeFormRowFloat(tab1, 'Max altitude', cfgs['altMax'])
        self.tab1_var3 = makeFormRowFloat(tab1, 'Min speed', cfgs['spdMin'])
        self.tab1_var4 = makeFormRowFloat(tab1, 'Max speed', cfgs['spdMax'])

        # Tab 2: data directories
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text='Directories')
        self.tab2_var1 = makeFormRow(tab2, 'GPS dir')
        self.tab2_var2 = makeFormRow(tab2, 'Clean dir')
        self.tab2_var3 = makeFormRow(tab2, 'Stats dir')
        self.tab2_var4 = makeFormRow(tab2, 'Calib dir')
        self.tab2_var5 = makeFormRow(tab2, 'Compressed dir')

        # Tab 3: select a calibration or an application mode
        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3, text='Run Mode')
        tab3_lab1 = Label(tab3, text='Run mode')
        tab3_lab1.config(fg='blue', font=('Times', 10, 'italic'))
        tab3_lab1.pack(fill=X)
        self.tab3_var1 = makeFormRowInt(tab3, '0-App; 1-Cal', '0')

        tab3_lab2 = Label(tab3, text='Road attributes. 0-off, 1-on')
        tab3_lab2.config(fg='blue', font=('Times', 10, 'italic'))
        tab3_lab2.pack(fill=X)
        # self.tab3_var2 = makeFormRowInt(tab3, 'length', '0')
        # self.tab3_var3 = makeFormRowInt(tab3, 'altitude', '0')
        # self.tab3_var4 = makeFormRowInt(tab3, 'speed', '0')

        tab3_frm = Frame(tab3)
        tab3_frm.pack()

        self.tab3_var2 = IntVar()
        Checkbutton(tab3_frm, text='Length', variable=self.tab3_var2).pack(side=LEFT)
        self.tab3_var3 = IntVar()
        Checkbutton(tab3_frm, text='Altitude', variable=self.tab3_var3).pack(side=LEFT)
        self.tab3_var4 = IntVar()
        Checkbutton(tab3_frm, text='Speed', variable=self.tab3_var4).pack(side=LEFT)

        # Tab 4: calibration settings
        tab4 = ttk.Frame(tabControl)
        tabControl.add(tab4, text='Calibration')
        tab4_lab1 = Label(tab4, text='By <length> attribute')
        tab4_lab1.pack(fill=X)
        tab4_lab1.config(fg='blue', font=('Times', 10, 'italic'))

        self.tab4_var1 = makeFormRowFloat(tab4, 'angle start (deg)', cfgs['start'])
        self.tab4_var2 = makeFormRowFloat(tab4, 'angle stop (deg)', cfgs['end'])
        self.tab4_var3 = makeFormRowFloat(tab4, 'angle step (deg)', cfgs['step'])

        tab4_lab2 = Label(tab4, text='By <altitude> attribute')
        tab4_lab2.pack(fill=X)
        tab4_lab2.config(fg='blue', font=('Times', 10, 'italic'))
        self.tab4_var4 = makeFormRowInt(tab4, '# of classes (start)', cfgs['hstart'])
        self.tab4_var5 = makeFormRowInt(tab4, '# of classes (stop)', cfgs['hstop'])
        self.tab4_var6 = makeFormRowInt(tab4, '# of classes (step)', cfgs['hstep'])

        tab4_lab3 = Label(tab4, text='By <speed> attribute')
        tab4_lab3.pack(fill=X)
        tab4_lab3.config(fg='blue', font=('Times', 10, 'italic'))
        self.tab4_var7 = makeFormRowInt(tab4, '# of classes (start)', cfgs['spd_start'])
        self.tab4_var8 = makeFormRowInt(tab4, '# of classes (stop)', cfgs['spd_stop'])
        self.tab4_var9 = makeFormRowInt(tab4, '# of classes (step)', cfgs['spd_step'])

        # Tab 5: application settings
        tab5 = ttk.Frame(tabControl)
        tabControl.add(tab5, text='Application')
        tab5_lab1 = Label(tab5, text='By <length> attribute settings')
        tab5_lab1.pack(fill=X)
        tab5_lab1.config(fg='blue', font=('Times', 10, 'italic'))
        self.tab5_var1 = makeFormRowFloat(tab5, 'dev by catet (m)', cfgs['devByCathetus'])
        self.tab5_var2 = makeFormRowFloat(tab5, 'dev by angle', cfgs['devByAng'])

        tab5_lab2 = Label(tab5, text='By <altitude> attribute settings')
        tab5_lab2.pack(fill=X)
        tab5_lab2.config(fg='blue', font=('Times', 10, 'italic'))
        self.tab5_var3 = makeFormRowInt(tab5, '# of classes', cfgs['hNumClasses'])

        tab5_lab3 = Label(tab5, text='By <speed> attribute settings')
        tab5_lab3.pack(fill=X)
        tab5_lab3.config(fg='blue', font=('Times', 10, 'italic'))
        self.tab5_var4 = makeFormRowInt(tab5, '# of classes', cfgs['spd_NumClasses'])

        # buttons
        tabControl.pack(anchor=NW)


        Button(win, text='Cancel', command=win.destroy).pack(side=RIGHT)
        Button(win, text='OK', command=self.checkSettings).pack(side=RIGHT, padx=5)
        Button(win, text='Fetch', command=self.printSetting).pack(side=RIGHT, padx=5)

        # set window modality to <on>
        win.focus_set()
        win.grab_set()
        win.wait_window()

    def checkSettings(self):
        params = self.fetchSettings()
        key_list = [key for key, val in params.items() if not val or ""]
        msg = "Missing input parameters:\n"
        for par in key_list:
            msg += par + '->' + '\n'
        showinfo('GPS optimizer', msg)

    def printSetting(self):
        params = self.fetchSettings()
        for par in params:
            print(par, '->>>', params[par])

    def fetchSettings(self):
        self.variables = {
            'altMin':       self.tab1_var1.get(),
            'altMax':       self.tab1_var2.get(),
            'spdMin':       self.tab1_var3.get(),
            'spdMax':       self.tab1_var4.get(),
            'gpsDir':       self.tab2_var1.get(),
            'cleanDir':     self.tab2_var2.get(),
            'statsDir':     self.tab2_var3.get(),
            'calibDir':     self.tab2_var4.get(),
            'comprDir':     self.tab2_var5.get(),
            'runmode':      self.tab3_var1.get(),
            'length':       self.tab3_var2.get(),
            'altitude':     self.tab3_var3.get(),
            'speed':        self.tab3_var4.get(),
            'angStart':     self.tab4_var1.get(),
            'angStop':      self.tab4_var2.get(),
            'angStep':      self.tab4_var3.get(),
            'altStart':     self.tab4_var4.get(),
            'altStop':      self.tab4_var5.get(),
            'altStep':      self.tab4_var6.get(),
            'spdStart':     self.tab4_var7.get(),
            'spdStop':      self.tab4_var8.get(),
            'spdStep':      self.tab4_var9.get(),
            'devByCathetus': self.tab5_var1.get(),
            'devByAng':     self.tab5_var2.get(),
            'hNumClasses':  self.tab5_var3.get(),
            'spd_NumClasses': self.tab5_var4.get()
        }

        return self.variables

    def onRun(self):
        pass




if __name__ == '__main__':
    myShell().mainloop()
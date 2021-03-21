import sys, os                                    # platform, args, run tools
from tkinter import *                             # base widgets, constants
from tkinter.messagebox import showinfo, showerror
from tkinter.filedialog import Open, SaveAs
from tkinter import ttk
from guimaker import *
from gps_formrows import *
from gps_filter_v2 import *
from optimizer_v2 import *


helptext = \
"""
Version 2 started on June 13, 2019 to allow input settings.
This program started on March 3, 2019.
Hope to finish soon :-
"""

program_title = 'GPS Optimizer'

# general configuration
try:
    import config
    cfgs = config.__dict__
except Exception as e:                                      # define in client app directory
    print(e)

class Shell(GuiMakerWindowMenu):
    variables = {}
    startfiledir = '.'
    ftypes = [('All files', '*'),
              ('csv', '.csv'),
              ('Text files', '.txt')]
    openDialog = None

    def start(self):
        self.menuBar = [
            ('File', 0,
             [('Settings',      0, self.onSettings),
              ('See list',      0, self.onSeeList),
              ('Exit',          0, self.onQuit)]),
            ('Run',             0,
             [('Data cleaning', 0, self.onCleaningModule),
              ('Calibration',   0, self.onCalibrationModule),
              ('Application',   0, self.onApplicationModule)]),
            ('Graphs', 0,
             [('Load', 0, '')])]

        self.toolBar = [
            ('Settings',    self.onSettings,    {'side': LEFT}),
            ('See list',    self.onSeeList,     {'side': LEFT})]

    def makeWidgets(self):
        self.master.title(program_title)

        ############################
        # 1. Placeholder for routes
        ############################

        frmListBox = Frame(self)
        sbar = Scrollbar(frmListBox)
        list = Listbox(frmListBox, relief=SUNKEN)
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        frmListBox.pack(side=LEFT, fill=Y)
        sbar.pack(side=RIGHT, fill=Y)
        list.pack(side=LEFT, expand=YES, fill=BOTH)

        #################################################
        # 2. Graphs placeholder, display route properties
        #################################################

        frmCanvasBox = Frame(self)
        cnv = Canvas(frmCanvasBox)
        cnv.config(bg='beige')
        cnv.pack(side=TOP, expand=YES, fill=BOTH)
        text = Text(frmCanvasBox)
        text.config(relief=SUNKEN, bd=2, bg='grey', fg='blue', height=3, cursor='gumby')
        text.pack(fill=X)
        frmCanvasBox.pack(side=LEFT, fill=BOTH, expand=YES)
        self.listbox = list
        self.text = text

    ########################
    # File - Settings
    ########################

    def onSettings(self):
        win = Toplevel()
        win.title('Program settings')
        win.minsize(300, 300)
        tabControl = ttk.Notebook(win)
        tabControl.config(height=300, width=300)

        # Tab 1: Cleaning
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='Data cleaning')
        self.tab1_var1 = makeFormRowFloat(tab1, 'Min altitude', cfgs['altMin'])
        self.tab1_var2 = makeFormRowFloat(tab1, 'Max altitude', cfgs['altMax'])
        self.tab1_var3 = makeFormRowFloat(tab1, 'Min speed',    cfgs['spdMin'])
        self.tab1_var4 = makeFormRowFloat(tab1, 'Max speed',    cfgs['spdMax'])

        # Tab 2: Directories
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text='Directories')
        self.tab2_var1 = makeFormRow(tab2, 'GPS dir')
        self.tab2_var2 = makeFormRow(tab2, 'Clean dir')
        self.tab2_var3 = makeFormRow(tab2, 'Stats dir')
        self.tab2_var4 = makeFormRow(tab2, 'Calib dir')
        self.tab2_var5 = makeFormRow(tab2, 'Compressed dir')

        # Tab 3: Run mode [0-app; 1-calibration]
        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3, text='Run Mode')
        tab3_lab1 = Label(tab3, text='Run mode')
        tab3_lab1.config(fg='blue', font=('Times', 10, 'italic'))
        tab3_lab1.pack(fill=X)
        self.tab3_var1 = makeFormRowInt(tab3, '0-App; 1-Cal', '0')

        tab3_lab2 = Label(tab3, text='Road attributes. 0-off, 1-on')
        tab3_lab2.config(fg='blue', font=('Times', 10, 'italic'))
        tab3_lab2.pack(fill=X)

        tab3_frm = Frame(tab3)
        tab3_frm.pack()
        self.tab3_var2 = IntVar()
        self.tab3_var3 = IntVar()
        self.tab3_var4 = IntVar()
        Checkbutton(tab3_frm, text='Length',    variable=self.tab3_var2).pack(side=LEFT)
        Checkbutton(tab3_frm, text='Altitude',  variable=self.tab3_var3).pack(side=LEFT)
        Checkbutton(tab3_frm, text='Speed',     variable=self.tab3_var4).pack(side=LEFT)

        # Tab 4: Calibration settings
        tab4 = ttk.Frame(tabControl)
        tabControl.add(tab4, text='Calibration')

        tab4_lab1 = Label(tab4, text='By <length> attribute')
        tab4_lab1.pack(fill=X)
        tab4_lab1.config(fg='blue', font=('Times', 10, 'italic'))
        self.tab4_var1 = makeFormRowInt(tab4, 'angle start (deg)',  cfgs['start'])
        self.tab4_var2 = makeFormRowInt(tab4, 'angle stop (deg)',   cfgs['end'])
        self.tab4_var3 = makeFormRowFloat(tab4, 'angle step (deg)', cfgs['step'])

        tab4_lab2 = Label(tab4, text='By <altitude> attribute')
        tab4_lab2.pack(fill=X)
        tab4_lab2.config(fg='blue', font=('Times', 10, 'italic'))
        self.tab4_var4 = makeFormRowInt(tab4, '# of classes (start)',   cfgs['hstart'])
        self.tab4_var5 = makeFormRowInt(tab4, '# of classes (stop)',    cfgs['hstop'])
        self.tab4_var6 = makeFormRowInt(tab4, '# of classes (step)',    cfgs['hstep'])

        tab4_lab3 = Label(tab4, text='By <speed> attribute')
        tab4_lab3.pack(fill=X)
        tab4_lab3.config(fg='blue', font=('Times', 10, 'italic'))
        self.tab4_var7 = makeFormRowInt(tab4, '# of classes (start)',   cfgs['spd_start'])
        self.tab4_var8 = makeFormRowInt(tab4, '# of classes (stop)',    cfgs['spd_stop'])
        self.tab4_var9 = makeFormRowInt(tab4, '# of classes (step)',    cfgs['spd_step'])

        # Tab 5: Application settings
        tab5 = ttk.Frame(tabControl)
        tabControl.add(tab5, text='Application')
        tab5_lab1 = Label(tab5, text='By <length> attribute settings')
        tab5_lab1.pack(fill=X)
        tab5_lab1.config(fg='blue', font=('Times', 10, 'italic'))
        self.tab5_var1 = makeFormRowFloat(tab5, 'dev by catet (m)', cfgs['devByCathetus'])
        self.tab5_var2 = makeFormRowFloat(tab5, 'dev by angle',     cfgs['devByAng'])

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
        Button(win, text='OK', command=win.destroy).pack(side=RIGHT)
        Button(win, text='Check settings', command=self.checkSettings).pack(side=RIGHT, padx=5)
        # Button(win, text='Fetch',   command=self.printSetting).pack(side=RIGHT, padx=5)

        # set window modality to <on>
        win.focus_set()
        win.grab_set()
        win.wait_window()

    def checkSettings(self):
        params = self.fetchSettings()
        key_list = [key for key, val in params.items() if not val or ""]
        msg = "Settings accepted. Missing parameters are:\n"
        for key in key_list:
            if key == 'spdMin' or key == 'runmode':
                pass
            else:
                msg += key + '--->' + '\n'
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

    ########################
    # File - See list
    ########################

    def setMessage(self, msg):
        self.text.delete('1.0', END)
        self.text.insert('1.0', msg)

    def txtMessage(self, index, lstats):
        trackId     = lstats[index][cfgs['trackId']]
        numRecs     = lstats[index][cfgs['numRecs']]
        minHeight   = str(round(float(lstats[index][cfgs['minHeight']]),)) + 'm'
        maxHeight   = str(round(float(lstats[index][cfgs['maxHeight']]),)) + 'm'
        minSpeed    = str(round(float(lstats[index][cfgs['minSpeed']]),)) + 'km/h'
        maxSpeed    = str(round(float(lstats[index][cfgs['maxSpeed']]),)) + 'km/h'
        fileSize    = str(float(lstats[index][cfgs['fileSize']])/1000) + 'Kb'
        trackLength = str(round(float(lstats[index][cfgs['trackLength']]), 3)) + 'km'

        msg = 'Track properties:\nId: %s, \t# records: %s, \tMin height: %s, \tMax height: %s\n' \
              'Min speed: %s, \tMax speed: %s, \tFile size: %s, \tLength: %s' % \
              (trackId, numRecs, minHeight, maxHeight, minSpeed, maxSpeed, fileSize, trackLength)
        self.setMessage(msg)

    def handleList(self, lstats): # get index value of selection
        index = self.listbox.curselection()
        index = int(index[0])
        self.txtMessage(index, lstats)

    def my_askopenfilename(self):
        self.openDialog = Open(initialdir=self.startfiledir, filetypes=self.ftypes)
        return self.openDialog.show()

    def onSeeList(self):
        fstats = self.my_askopenfilename()
        with open(fstats, newline='') as f:
            lstats = [line.strip().split(',') for line in f]
        pos = 0
        for label in lstats:
            self.listbox.insert(pos, label[cfgs['trackId']])
            pos += 1
        self.listbox.bind('<Double-1>', (lambda event: self.handleList(lstats)))

    ########################
    # File - Exit
    ########################

    def onQuit(self):
        self.quit()

    #############################
    # Run - Data cleaning & stats
    #############################

    def onCleaningModule(self):
        params = self.fetchSettings()
        if params['gpsDir'] != "" and params['cleanDir'] != "" and params['statsDir'] != "":
            for (trackIdx, trackList) in fileReader(params):
                fileWriter(trackIdx, trackList, params, name='')
                statsList = stats(trackIdx, trackList, params)
                fileWriter(None, statsList, params, name='original_stats')
            showinfo('GPS Optimizer', 'Data cleaning and stats are ready')
        else:
            showerror('GPS Optimizer', 'Enter directories')

    #############################
    # Run - Calibration <runmode=1>
    #############################

    def lenIter(self, params):
        num_iter = int(params['angStop'] / params['angStep'])  # number of iterations for length optimization
        if num_iter <= 50:
            return [(round(x * params['angStep'], 1), x) for x in range(params['angStart'], num_iter)]
        elif 50 < num_iter <= 150:
            return [(round(x * params['angStep'], 1), x) for x in range(params['angStart'] * 10, num_iter)]
        else:
            showinfo('GPS Optimizer', 'Currently process is limited to 50 iterations.')

    def onCalibrationModule(self):
        params = self.fetchSettings()

        if (params['length'] and params['altitude']) or (params['length'] and params['speed']) or \
           (params['altitude'] and params['speed']) or (params['length'] and params['altitude'] and params['speed']):
            showinfo('GPS Optimizer', 'Check 1 checkbox to continue.')

        elif params['cleanDir'] == "" and params['calibDir'] == "":
            showinfo('GPS Optimizer', 'Select <clean> and <calibrated> directories.')

        elif params['runmode'] != 1:
            showinfo('GPS Optimizer', 'Select <1> to run application mode.')

        else:
            for tracks in fileReaderOpt(params['cleanDir']):  # params['runmode'] == 1:
                if params['length']:
                    iter_list = self.lenIter(params)
                    ftag = str(params['angStart']) + '-' + str(params['angStop']) + '_deg'  # e.g. from 0.1-5
                    fname = 'Cal_by_length_' + ftag         # filename to differentiate files
                    for (devByAng, iter) in iter_list:
                        calByLenRec = onLengthOptimize(tracks, devByAng, iter, params)
                        fileWriterOpt(calByLenRec, params['calibDir'], fname, params)

                elif params['altitude']:
                    ftag = str(params['altStart']) + '-' + str(params['altStop']) + '_num_classes'
                    fname = 'Cal_by_altitude_' + ftag       # filename to differentiate files
                    min_alt = math.floor(getMin(tracks, 'altIdx'))
                    max_alt = math.ceil(getMax(tracks, 'altIdx'))
                    range_alt = max_alt - min_alt
                    qty_alts = [i for i in range(params['altStart'], params['altStop'])]
                    for qty_alt in qty_alts:
                        width_alt = range_alt / qty_alt
                        calByAltRec = onAltitudeOptimize(tracks, min_alt, width_alt, qty_alt, params)
                        fileWriterOpt(calByAltRec, params['calibDir'], fname, params)

                else:  # elif params['speed']:
                    ftag = str(params['spdStart']) + '-' + str(params['spdStop']) + '_num_classes'
                    fname = 'Cal_by_speed_' + ftag          # filename to differentiate files
                    min_speed = getMin(tracks, 'speedIdx')
                    max_speed = getMax(tracks, 'speedIdx')
                    range_speed = max_speed - min_speed
                    qty_speeds = [i for i in range(params['spdStart'], params['spdStop'])]
                    for qty_speed in qty_speeds:
                        width_speed = range_speed / qty_speed
                        calBySpeedRec = onSpeedOptimize(tracks, min_speed, width_speed, qty_speed, params)
                        fileWriterOpt(calBySpeedRec, params['calibDir'], fname, params)

            showinfo('GPS Optimizer', 'Process is complete. Check results')

    #############################
    # Run - Application <runmode=0>
    #############################

    def onApplicationModule(self):
        params = self.fetchSettings()

        if not (params['length'] and params['altitude'] and params['speed']):
            showinfo('GPS Optimizer', 'Check all checkboxes to continue.')

        elif params['cleanDir'] == "" and params['comprDir'] == "":
            showinfo('GPS Optimizer', 'Select <clean> and <compressed> directories.')

        elif params['runmode'] != 0:
            showinfo('GPS Optimizer', 'Select <0> to run application mode.')

        else:
            for tracks in fileReaderOpt(params['cleanDir']):
                # length attribute application
                byLen = onLengthOptimize(tracks, params['devByAng'], 0, params)

                # altitude attribute application
                min_alt = math.floor(getMin(tracks, 'altIdx'))
                max_alt = math.ceil(getMax(tracks, 'altIdx'))
                range_alt = max_alt - min_alt
                width_alt = range_alt / params['hNumClasses']
                byAlt = onAltitudeOptimize(tracks, min_alt, width_alt, params['hNumClasses'], params)

                # speed attribute application
                min_speed = getMin(tracks, 'speedIdx')
                max_speed = getMax(tracks, 'speedIdx')
                range_speed = max_speed - min_speed
                width_speed = range_speed / cfgs['spd_NumClasses']
                bySpd = onSpeedOptimize(tracks, min_speed, width_speed, params['spd_NumClasses'], params)

                # combine all attributes
                aggSeq = (byLen + byAlt + bySpd)                    # combine all sequences
                cleanSeq = list(dict.fromkeys(aggSeq))              # remove duplicates
                cleanSeq.sort()                                     # sort
                compTrack = [tracks[index] for index in cleanSeq]   # save selected tracks

                name = tracks[0][cfgs['groupIdx']] + '_' + \
                       tracks[0][cfgs['unitIdx']] + '_' + \
                       tracks[0][cfgs['trackIdx']] + '_comp'
                fileWriterOpt(compTrack, params['comprDir'], name, params)

            showinfo('GPS Optimizer', 'Process is complete. Check results')

    ########################
    # Help
    ########################

    def help(self):
        showinfo('About Program', helptext)

if __name__ == '__main__':
    Shell().mainloop()
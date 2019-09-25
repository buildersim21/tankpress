import csv as ss  # read and write csv files, to get to and from the script file and to have all the numbers the
# script generates
# load system to run the script, makedirs to create the folders, curdir to work in the current directory (where the
# py files are), and path to create all the file and directory paths
from os import system, makedirs, curdir, path
# load Canvas for the scrollbar on the "Graphs" tab, ttk for more modern GUI look, Tk for the root window,
# PhotoImage for the images on the buttons and the graphs, Menu for the menubar, StringVar for Run Name and
# statustext variables, and DoubleVar for the floating numbers of the numerical inputs and outputs
from tkinter import Canvas, ttk, Tk, PhotoImage, Menu, StringVar, DoubleVar
from tkinter.font import Font  # used to modify the size of the Entry widget text

appVersion = '2019.06.18.1620'  # gives an idea of when the project was versioned
symdeg = '\u00b0'  # gives the unicode text for the degree symbol


class Notes:  # majority of the GUI components
    def __init__(self, root):  # provides the bulk of the GUI
        # GUI Style(s)
        sty = ttk.Style()
        sty.theme_use('xpnative')  # vista and xpnative look better than winnative
        sty.configure('TButton', font=14)  # Button widget font
        sty.configure('TLabel', font=14)  # Label widget font
        sty.configure('TNotebook.Tab', font=14)  # Notebook widget Tab font
        entry_font = Font(size=14)  # Entry widget text font
        root.statustext.set('Waiting...')  # set the status bar text

        # STRING VARIABLE
        ts = StringVar()
        # FLOAT VARIABLES
        d1 = DoubleVar()
        V2 = DoubleVar()
        p1 = DoubleVar()
        p2 = DoubleVar()
        T1 = DoubleVar()
        T2 = DoubleVar()
        dt = DoubleVar()
        T2f = DoubleVar()
        m2f = DoubleVar()
        u2f = DoubleVar()
        tf = DoubleVar()
        # Notebook GUI and Its Frames
        notebook = ttk.Notebook(root)  # call Notebook widget and set it in root window
        notebook.pack()  # display notebook by packing into the root window
        # add frame widgets to the notebook widget
        frame1 = ttk.Frame(notebook)
        frame2 = ttk.Frame(notebook)
        pframe3 = ttk.Frame(notebook)
        notebook.add(frame1, text='Input')
        notebook.add(frame2, text='Output')
        notebook.add(pframe3, text='Graphs')
        # Image Paths
        RunImg = "./GUIfiles/Run.png"
        ResetImg = "./GUIfiles/Reset.png"
        Reloadimg = "./GUIfiles/Reload.png"
        PlotsImg = "./GUIfiles/Yes.png"

        # Scrollbar with Frame3
        canvas = Canvas(pframe3, width=900, height=600)  # must use Canvas widget to attach the scrollbar
        scroll = ttk.Scrollbar(pframe3, command=canvas.yview)  # configure scrollbar with the yview command
        canvas.config(yscrollcommand=scroll.set, scrollregion=(0, 0, 7500, 6000))  # configure the scroll command and
        # region on the canvas
        canvas.pack(side='left', fill='both', expand='true')  # pack the canvas into the frame already tied to the
        # notebook widget
        frame4 = ttk.Frame(pframe3, width=800, height=600)  # create a new frame widget inside the frame widget of
        # specified dimensions
        frame4.pack(side='top', fill='both', expand='false')  # display the new frame widget
        scroll.pack(side='right', fill="y", expand='true')  # display the scrollbar
        frame3 = ttk.Frame(canvas)  # create a new frame widget inside the canvas widget
        canvas.create_window(0, 0, window=frame3, anchor='nw')  # display the new frame widget
        # Frame 1 Material: Input
        text = ttk.Label(frame1, font=14,
                         text='TankPress computes the time taken to pressurize a tank of given volume with '
                              'air.\n\nInitial Conditions')
        text.grid(row=0, column=0, columnspan=6)  # display the description label on the previous line
        sepframe1 = ttk.Separator(frame1, orient='horizontal')  # add a separator widget
        sepframe1.grid(row=1, column=0, sticky='we', columnspan=7)  # display the separator widget
        # Pipe Pressure GUI
        lbl_P1 = ttk.Label(frame1, text='Pipe Pressure, p1 =')
        entry_P1 = ttk.Entry(frame1, textvariable=p1, font=entry_font)
        unit_P1 = ttk.Label(frame1, text='psi')
        lbl_P1.grid(row=2, column=0)
        entry_P1.grid(row=2, column=1)
        unit_P1.grid(row=2, column=2)
        # we make a descriptor label, then an Entry widget, and then the unit label
        # we display these using the grid system to control where these elements end up
        # this applies up to the Run Name section

        # Tank Pressure GUI
        lbl_P2 = ttk.Label(frame1, text='Tank Pressure, p2 =')
        entry_P2 = ttk.Entry(frame1, textvariable=p2, font=entry_font)
        unit_P2 = ttk.Label(frame1, text='psi')
        lbl_P2.grid(row=2, column=4)
        entry_P2.grid(row=2, column=5)
        unit_P2.grid(row=2, column=6)

        # Pipe Temperature GUI
        lbl_T1 = ttk.Label(frame1, text='Pipe Temperature, T1 =')
        entry_T1 = ttk.Entry(frame1, textvariable=T1, font=entry_font)
        unit_T1 = ttk.Label(frame1, text=symdeg + 'F')
        lbl_T1.grid(row=3, column=0)
        entry_T1.grid(row=3, column=1)
        unit_T1.grid(row=3, column=2)

        # Tank Temperature GUI
        lbl_T2 = ttk.Label(frame1, text='Tank Temperature, T2 =')
        entry_T2 = ttk.Entry(frame1, textvariable=T2, font=entry_font)
        unit_T2 = ttk.Label(frame1, text=symdeg + 'F')
        lbl_T2.grid(row=3, column=4)
        entry_T2.grid(row=3, column=5)
        unit_T2.grid(row=3, column=6)

        # Pipe Diameter GUI
        lbl_D1 = ttk.Label(frame1, text='Pipe Diameter, d1 =')
        entry_D1 = ttk.Entry(frame1, textvariable=d1, font=entry_font)
        unit_D1 = ttk.Label(frame1, text='in.')
        lbl_D1.grid(row=4, column=0)
        entry_D1.grid(row=4, column=1)
        unit_D1.grid(row=4, column=2)

        # Tank Volume GUI
        lbl_V2 = ttk.Label(frame1, text='Tank Volume, V2 =')
        entry_V2 = ttk.Entry(frame1, textvariable=V2, font=entry_font)
        unit_V2 = ttk.Label(frame1, text='cu. ft')
        lbl_V2.grid(row=4, column=4)
        entry_V2.grid(row=4, column=5)
        unit_V2.grid(row=4, column=6)

        # Time Step GUI
        lbl_dt = ttk.Label(frame1, text='Time Step, dt =')
        entry_dt = ttk.Entry(frame1, textvariable=dt, font=entry_font)
        unit_dt = ttk.Label(frame1, text='sec')
        lbl_dt.grid(row=5, column=0)
        entry_dt.grid(row=5, column=1)
        unit_dt.grid(row=5, column=2)

        # Run Name GUI
        lbl_run = ttk.Label(frame1, text='Run Name Input =')
        entry_run = ttk.Entry(frame1, textvariable=ts, font=entry_font)
        lbl_run.grid(row=5, column=4)
        entry_run.grid(row=5, column=5)
        # we make a descriptor label and then an Entry widget
        # we display these using the grid system

        # additional separators to organize the widget layout and ease use
        sep2frame1 = ttk.Separator(frame1, orient='horizontal')
        sep2frame1.grid(row=6, column=0, sticky='we', columnspan=7)
        sep3frame1 = ttk.Separator(frame1, orient='vertical')
        sep3frame1.grid(row=1, column=3, sticky='ns', rowspan=5)

        # Start Button GUI
        Run = PhotoImage(file=RunImg)  # load the image to display on button widget
        but_start = ttk.Button(frame1, compound='left', image=Run, text='Start Run',
                               command=lambda: self.startTankPress(ts, d1, V2, p1, p2, T1, T2, dt,
                                                                   root.statustext, RunStart_lbl))
        # button widget uses lambda function to send variable inputs to the startTankPress function
        but_start.image = Run  # store the image so it's not tossed out
        but_start.grid(row=7, column=0, columnspan=2, sticky='nsew')  # display the button

        # Reset Button GUI
        Reset = PhotoImage(file=ResetImg)  # load the image to display on the button widget
        but_reset = ttk.Button(frame1, compound='left', image=Reset, text='Reset All Tabs', command=lambda: \
            self.resetTankPress(ts, d1, V2, p1, p2, T1, T2, dt, m2f, tf, u2f, T2f, graph1, graph2,
                                graph3, graph4, graph5, graph6, Run, root.statustext, RunStart_lbl))
        # uses lambda function to pass (many) inputs to the resetTankPress function
        but_reset.image = Reset  # store the image
        but_reset.grid(row=7, column=2, columnspan=3, sticky='nsew')  # display the button

        # Reload Last Inputs GUI Button
        reloadi = PhotoImage(file=Reloadimg)  # supposedly loads the image
        but_load = ttk.Button(frame1, compound='left', image=reloadi, text='Reload Last Inputs', command=lambda: \
            self.LoadPrevRun(ts, d1, V2, p1, p2, T1, T2, dt, root.statustext))
        # uses lambda function to send many variables to the function LoadPrevRun
        # supposed to load image, but doesn't right now
        but_load.image = reloadi  # supposed to store the image, but image does not show up at the moment
        but_load.grid(row=7, column=5, columnspan=2, sticky='nsew')  # display the button

        # Instructions Labels
        sep4frame1 = ttk.Separator(frame1, orient='horizontal')  # do a separator widget to separate from the buttons
        sep4frame1.grid(row=8, column=0, columnspan=7, sticky='we')  # display the separator widget
        lbl_instr = ttk.Label(frame1, text='The values of the pipe and tank pressures, pipe diameter, and tank volume '
                                           'must be greater zero.')
        lbl_instr1 = ttk.Label(frame1, text='The values of the pipe and tank temperatures must be greater than '
                                            'absolute zero (or -459.67' + symdeg + 'F).')
        lbl_instr2 = ttk.Label(frame1, text='The value of the time step must be between zero and one, not including '
                                            'zero and one.')
        lbl_instr3 = ttk.Label(frame1, text='The run name must be different each run, otherwise there will be an '
                                            'error.')
        lbl_instr4 = ttk.Label(frame1, text='The input file to the script is overwritten each run.')
        lbl_instr5 = ttk.Label(frame1, text='Always input a NEW run name before clicking "Start Run" or loading '
                                            'output or graphs; otherwise, error occurs.')
        lbl_instr6 = ttk.Label(frame1, text='---Instructions---')
        lbl_instr.grid(row=10, column=0, columnspan=7)
        lbl_instr1.grid(row=11, column=0, columnspan=7)
        lbl_instr2.grid(row=12, column=0, columnspan=7)
        lbl_instr3.grid(row=13, column=0, columnspan=7)
        lbl_instr4.grid(row=14, column=0, columnspan=7)
        lbl_instr5.grid(row=15, column=0, columnspan=7)
        lbl_instr6.grid(row=9, column=0, columnspan=7)
        sep5frame1 = ttk.Separator(frame1, orient='horizontal')
        sep5frame1.grid(row=16, column=0, columnspan=7, sticky='we')
        RunStart_lbl = ttk.Label(frame1, text='Waiting...')
        RunStart_lbl.grid(row=17, column=0)
        RunStart_lbl['text'] = 'Waiting for Input...'

        # Frame 2 Material: Output

        # Time To Pressurize Tank GUI
        lbl_TotalTime = ttk.Label(frame2, text='Time Taken to Pressurize the Tank')
        lbl_TimeOut = ttk.Entry(frame2, textvariable=tf, font=entry_font)
        lbl_TimeUnit = ttk.Label(frame2, text='seconds')
        lbl_TotalTime.grid(row=0, column=0)
        lbl_TimeOut.grid(row=0, column=1)
        lbl_TimeUnit.grid(row=0, column=2)
        # Final Tank Temp GUI
        lbl_FinTemp = ttk.Label(frame2, text='Final Temperature in Tank')
        lbl_TempOut = ttk.Entry(frame2, textvariable=T2f, font=entry_font)
        lbl_TempUnit = ttk.Label(frame2, text=symdeg + 'F')
        lbl_FinTemp.grid(row=1, column=0)
        lbl_TempOut.grid(row=1, column=1)
        lbl_TempUnit.grid(row=1, column=2)
        # Final Mass In Tank GUI
        lbl_FinMass = ttk.Label(frame2, text='Final Mass Inside Tank')
        lbl_MassOut = ttk.Entry(frame2, textvariable=m2f, font=entry_font)
        lbl_MassUnit = ttk.Label(frame2, text='lbm')
        lbl_FinMass.grid(row=2, column=0)
        lbl_MassOut.grid(row=2, column=1)
        lbl_MassUnit.grid(row=2, column=2)
        # Final Specific Internal Energy GUI
        lbl_IntNrg = ttk.Label(frame2, text='Final Specific Internal Energy in Tank')
        lbl_NrgOut = ttk.Entry(frame2, textvariable=u2f, font=entry_font)
        lbl_NrgUnit = ttk.Label(frame2, text='(ft*lbf)/lbm')
        lbl_IntNrg.grid(row=3, column=0)
        lbl_NrgOut.grid(row=3, column=1)
        lbl_NrgUnit.grid(row=3, column=2)
        # Data Output Button GUI
        Output = PhotoImage(file=PlotsImg)
        but_output = ttk.Button(frame2, compound='left', image=Output, text='Load Output', command=lambda: \
            self.TankPressOutput(ts, T2f, m2f, u2f, tf, root.statustext))
        but_output.image = Output
        but_output.grid(row=4, column=0, columnspan=3)

        # Frame 3 Material: Graphs

        # create the "graph" label widgets using a chosen image already loaded
        graph1 = ttk.Label(frame3, image=Run)
        graph2 = ttk.Label(frame3, image=Run)
        graph3 = ttk.Label(frame3, image=Run)
        graph4 = ttk.Label(frame3, image=Run)
        graph5 = ttk.Label(frame3, image=Run)
        graph6 = ttk.Label(frame3, image=Run)
        # display the "graph" label widgets
        graph1.grid(row=1, column=0)
        graph2.grid(row=2, column=0)
        graph3.grid(row=3, column=0)
        graph4.grid(row=4, column=0)
        graph5.grid(row=5, column=0)
        graph6.grid(row=6, column=0)
        # Pull Plots Button GUI
        Plots = PhotoImage(file=PlotsImg)
        but_plots = ttk.Button(frame4, compound='left', image=Plots, text='Load Plots', command=lambda: self.pullplots(
            ts, graph1, graph2, graph3, graph4, graph5, graph6, root.statustext))
        but_plots.image = Plots
        but_plots.grid(row=0, column=0)

    def startTankPress(self, ts, d1, V2, p1, p2, T1, T2, dt, stattext, lbltext):  # setup for and run main script
        # Set up for the "Input" csv for the script
        lbltext['text'] = 'Working...'
        stattext.set('Working...')
        tsa = "Run Name"
        V2a = "Tank Volume"
        d1a = "Pipe Diameter"
        p1a = "Pipe Pressure"
        p2a = "Tank Pressure"
        T1a = "Pipe Temperature"
        T2a = "Tank Temperature"
        dta = "Time Step"
        row1 = [tsa, V2a, d1a, p1a, p2a, T1a, T2a, dta]
        # get the values typed into the Entry widgets on the "Input" tab
        ts = ts.get()
        V2 = V2.get()
        d1 = d1.get()
        p1 = p1.get()
        p2 = p2.get()
        T1 = T1.get()
        T2 = T2.get()
        dt = dt.get()
        row2 = [ts, V2, d1, p1, p2, T1, T2, dt]
        # generate the folder directories and file paths
        MainPath = path.relpath('TankPress-' + ts, start=curdir)
        DataPath = path.join(MainPath, 'Data')
        FigPath = path.join(MainPath, 'Figures')
        EpsPath = path.join(FigPath, 'eps')
        PngPath = path.join(FigPath, 'png')
        makedirs(DataPath)
        makedirs(FigPath)
        makedirs(EpsPath)
        makedirs(PngPath)
        csvfile_sel = path.join(DataPath, 'TankPress-' + ts + '-select.csv')
        csvfile_ful = path.join(DataPath, 'TankPress-' + ts + '-full.csv')
        # the input csv currently cannot be with ts because the script won't know what ts is until it loads the csv,
        # consider this a limitation of this method.
        csvpath = path.relpath('TankPressInput', start=curdir)
        # if the folder doesn't exist, the if statement will cause it to be created
        if not path.exists(csvpath):
            makedirs(csvpath)
        csvfile_input = path.join(csvpath, 'TankPressInput.csv')
        # create the csv files: the full results, the select results, and the output
        with open(csvfile_sel, 'w', newline='') as csvsel:
            writ = ss.writer(csvsel, dialect='excel')
        with open(csvfile_ful, 'w', newline='') as csvful:
            wrote = ss.writer(csvful, dialect='excel')
        with open(csvfile_input, 'w', newline='') as csvfiling:
            writing = ss.writer(csvfiling, dialect='excel')
            writing.writerow(row1)  # write the input file contents
            writing.writerow(row2)
        system('python TPscript.py')  # run the script file
        lbltext['text'] = 'Finished.'  # change the status bar text when the script finishes
        stattext.set('Script Completed.')

    def resetTankPress(self, ts, d1, V2, p1, p2, T1, T2, dt, m2f, tf, u2f, T2f, graph1, graph2, graph3,
                       graph4, graph5, graph6, Run, stattext, lbltext):  # to reset all three tabs to initial GUI setup
        # "Input" tab reset
        ts.set('')
        d1.set(0.0)
        V2.set(0.0)
        p1.set(0.0)
        p2.set(0.0)
        T1.set(0.0)
        T2.set(0.0)
        dt.set(0.0)
        # "Output" tab reset
        m2f.set(0.0)
        tf.set(0.0)
        u2f.set(0.0)
        T2f.set(0.0)
        # "Graphs" tab reset
        graph1.configure(image=Run)
        graph2.configure(image=Run)
        graph3.configure(image=Run)
        graph4.configure(image=Run)
        graph5.configure(image=Run)
        graph6.configure(image=Run)
        # Status Bar text reset
        stattext.set('Tabs successfully reset. Waiting...')
        lbltext['text'] = 'Waiting...'

    def LoadPrevRun(self, ts, d1, V2, p1, p2, T1, T2, dt, stattext):  # loads the values from the input csv, except ts
        ts = ts.get()  # whatever Run Name is typed in, better be a previous run so it can be loaded in the "Output"
        # and "Graphs" tabs
        # ensure that the function has the file path of the csv input file
        csvpath = path.relpath('TankPressInput', start=curdir)
        csvfile_input = path.join(csvpath, 'TankPressInput.csv')
        with open(csvfile_input, 'r', newline='') as csvfiling:  # open the csv file for reading
            reading = ss.DictReader(csvfiling, dialect='excel')  # decide the reading mode provided by csv module
            for row in reading:  # use for loop to pull the data, even though in this case it is one row
                d1.set(row['Pipe Diameter'])  # using the DictReader method allows getting the data by name
                V2.set(row['Tank Volume'])
                p1.set(row['Pipe Pressure'])
                p2.set(row['Tank Pressure'])
                T1.set(row['Pipe Temperature'])
                T2.set(row['Tank Temperature'])
                dt.set(row['Time Step'])
        stattext.set('Previous Run Loaded.')
        return ts  # decided to ensure that ts is returned by this function (command) just in case

    def TankPressOutput(self, ts, T2f, m2f, u2f, tf, stattext):  # returns four of the potential values to be
        # displayed on the
        # "Output" tab
        ts = ts.get()  # get the Run Name
        # Make the paths necessary to ease reading the csv results file
        MainPath = path.relpath('TankPress-' + ts, start=curdir)
        DataPath = path.join(MainPath, 'Data')
        csvfile_results = path.join(DataPath, 'TankPressResults.csv')
        with open(csvfile_results, 'r', newline='') as readfile:  # open the csv results file for reading
            reading = ss.DictReader(readfile, dialect='excel')  # choose DictReader to ease data capture
            for row in reading:  # use for loop to get data from the data row using the header names
                T2f.set(row['Tank Temperature'])
                m2f.set(row['Tank Mass'])
                u2f.set(row['Internal Energy'])
                tf.set(row['Time'])
        stattext.set('TankPress Results Output Loaded.')

    def pullplots(self, ts, graph1, graph2, graph3, graph4, graph5, graph6, stattext):  # load the plots into the
        # "Graphs"
        # tab
        ts = ts.get()  # get the Run Name
        # set up the paths to read the graph images
        MainPath = path.relpath('TankPress-' + ts, start=curdir)
        FigPath = path.join(MainPath, 'Figures')
        PngPath = path.join(FigPath, 'png')
        image1path = path.join(PngPath, 'P2-Time-Rel-' + ts + '.png')
        image2path = path.join(PngPath, 'T2-Time-Rel-' + ts + '.png')
        image3path = path.join(PngPath, 'P2-T2-Rel-' + ts + '.png')
        image4path = path.join(PngPath, 'M2-Time-Rel-' + ts + '.png')
        image5path = path.join(PngPath, 'MFR-Time-Rel-' + ts + '.png')
        image6path = path.join(PngPath, 'INTNRG-Time-Rel-' + ts + '.png')
        # load the images using the paths just specified and PhotoImage from tkinter
        image1 = PhotoImage(file=image1path)
        image2 = PhotoImage(file=image2path)
        image3 = PhotoImage(file=image3path)
        image4 = PhotoImage(file=image4path)
        image5 = PhotoImage(file=image5path)
        image6 = PhotoImage(file=image6path)
        # save the images to the "graph" label widgets' image "config"
        graph1.image = image1
        graph2.image = image2
        graph3.image = image3
        graph4.image = image4
        graph5.image = image5
        graph6.image = image6
        # here we configure the "graph" label widgets to change the widget display to the generated graphs
        graph1.configure(image=image1)
        graph2.configure(image=image2)
        graph3.configure(image=image3)
        graph4.configure(image=image4)
        graph5.configure(image=image5)
        graph6.configure(image=image6)
        stattext.set('TankPress Graphs Loaded.')


def main():  # we set up the main function call
    # root window
    root = Tk()  # we call for a root window
    root.wm_title('TankPress Version ' + appVersion)  # we change the title bar text
    # menubar
    mainmenu = Menu(root)  # we add a menu bar
    mainmenu.add_command(label="Exit Program", command=root.destroy)  # add a command "button" to the menu bar
    root.config(menu=mainmenu)  # tie the menu bar to the root window
    # we configure the root window further
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    resources = path.relpath('GUIfiles', start=curdir)  # set the image path
    programico = path.join(resources, 'run_program.ico')  # set the icon path
    root.iconbitmap(programico)  # set the program icon seen in the title bar and task bar
    root.config(height=400, width=400)  # base size of window
    root.statustext = StringVar()  # sets the status bar text variable
    status = ttk.Label(root, textvariable=root.statustext, relief="sunken", anchor='w')  # adds a label widget to
    # display status text
    status.pack(side='bottom', fill='x')  # pack the status bar label
    Notes(root)  # call the class containing the bulk of the GUI
    root.mainloop()  # GUI persistence so it doesn't close on its own


if __name__ == "__main__":
    main()

# TODO add validation routines, fix the image not loading issue

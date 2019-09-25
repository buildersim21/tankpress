# Tank Pressurization Program
# Jeanette Zatowski
#
# Version
# '2019.0618.1620'
import csv as ss  # read and write csv files
from os import path, curdir  # to reference the current directory and generate the file paths
# where we use something not already a part of the base Python distribution, matplotlib, to generate graphs that look
# a lot like those one would make in MATLAB
from matplotlib.pyplot import xlim, figure, ylabel, plot, grid, savefig, xlabel, title, close, get_fignums, ylim
from math import sqrt, pi  # need the square root and pi functions of the math module for calculations
from matplotlib.backends.backend_pdf import PdfPages  # specifically to make a multipage pdf

symdeg = 'u00b0'  # provide a unicode degree symbol


def multipage(filename, figs=None):  # create a multipage pdf file from the graphs
    with PdfPages(filename) as pdf:
        if figs is None:
            figs = [figure(n) for n in get_fignums()]
        for fig in figs:
            pdf.savefig(fig)
    return


def plotation(xvar, yvar, xlab, ylab, figtitle, figname):  # the main part of making graphs
    figure(dpi=150, figsize=[6, 6])  # set figure size and resolution
    plot(xvar, yvar)  # plot them using matplotlib
    xlim(min(xvar), max(xvar))  # set the x-axis limit
    ylim(min(yvar), max(yvar))  # set the y-axis limit
    title(figtitle, size='large', style='oblique', va='baseline', weight='bold')  # set the graph title
    xlabel(xlab)  # set the x-axis label
    ylabel(ylab)  # set the y-axis label
    grid(b='on', which='major', axis='both')  # display a grid
    pngfile = path.join(PngPath, figname + '-' + ts + '.png')  # png file path
    epsfile = path.join(EpsPath, figname + '-' + ts + '.eps')  # eps file path
    savefig(pngfile, dpi=150, format='png')  # save the graph in png format
    savefig(epsfile, format='eps')  # save the graph in eps format (typically used in past LaTeX documents)
    return


def PDFplot(PRESSURE, TEMPERATURE, MASS, MFR, INTNRG, TIME):  # sets up to go to the part that makes the graphs
    pdffile = path.join(FigPath, 'TankPress-' + ts + '.pdf')  # create the pdf path
    y1var = PRESSURE  # set the pressure array to a y-axis variable
    y2var = TEMPERATURE  # set the temperature array to a y-axis variable
    y3var = y1var  # set the variable of graph 3 to the first y-axis variable
    y4var = MASS  # set the mass array to a y-axis variable
    y5var = MFR  # set the mfr array to a y-axis variable
    y6var = INTNRG  # set the intnrg array to a y-axis variable
    x1var = TIME  # set the time array to a x-axis variable
    x2var = y2var  # set the y-axis variable of graph 2 to a x-axis variable
    # fig 1 labels
    fig1_xlab = 'Time(s)'
    fig1_ylab = 'Pressure Inside Tank (psia)'
    fig1_pt = 'Pressure Inside Tank Over Time'
    fig1_name = 'P2-Time-Rel'
    # fig 2 labels
    fig2_xlab = fig1_xlab
    fig2_ylab = 'Temperature Inside Tank (°F)'
    fig2_pt = 'Temperature Inside Tank Over Time'
    fig2_name = 'T2-Time-Rel'
    # fig 3 labels
    fig3_ylab = fig1_ylab
    fig3_xlab = fig2_ylab
    fig3_pt = 'Pressure-Temperature Relationship'
    fig3_name = 'P2-T2-Rel'
    # fig 4 labels
    fig4_xlab = fig1_xlab
    fig4_ylab = 'Mass Inside Tank (lbm)'
    fig4_pt = 'Mass Inside Tank Over Time'
    fig4_name = 'M2-Time-Rel'
    # fig 5 labels
    fig5_xlab = fig1_xlab
    fig5_ylab = 'Mass Flow Rate Into Tank (lbm/s)'
    fig5_pt = 'Mass Flow Rate Into Tank Over Time'
    fig5_name = 'MFR-Time-Rel'
    # fig 6 labels
    fig6_xlab = fig1_xlab
    fig6_ylab = 'Specific Internal Energy (ft*lbf/lbm)'
    fig6_pt = 'Specific Internal Energy Over Time'
    fig6_name = 'INTNRG-Time-Rel'
    # run the graph generation functions
    fig1 = plotation(x1var, y1var, fig1_xlab, fig1_ylab, fig1_pt, fig1_name)
    fig2 = plotation(x1var, y2var, fig2_xlab, fig2_ylab, fig2_pt, fig2_name)
    fig3 = plotation(x2var, y3var, fig3_xlab, fig3_ylab, fig3_pt, fig3_name)
    fig4 = plotation(x1var, y4var, fig4_xlab, fig4_ylab, fig4_pt, fig4_name)
    fig5 = plotation(x1var, y5var, fig5_xlab, fig5_ylab, fig5_pt, fig5_name)
    fig6 = plotation(x1var, y6var, fig6_xlab, fig6_ylab, fig6_pt, fig6_name)
    # create a multipage pdf of the graphs
    multipage(pdffile)
    close()  # finish
    return

# inputs from csv from GUI
# folder/file structure


csvpath = path.relpath('TankPressInput', start=curdir)
csvfile_input = path.join(csvpath, 'TankPressInput.csv')

with open(csvfile_input, 'r', newline='') as csvinput:  # open the input csv file for reading
    CSVINPUT = ss.DictReader(csvinput, dialect='excel') # use DictReader to simplify data assignments
    for line in CSVINPUT:  # even though there is one row, we still use a for loop
        ts = line["Run Name"]  # the header row provides the names to use to load the data to variables
        V2 = float(line["Tank Volume"])  # all but ts require the data to be stored as floats
        d1 = float(line["Pipe Diameter"])
        p1 = float(line["Pipe Pressure"])
        p2 = float(line["Tank Pressure"])
        T1 = float(line["Pipe Temperature"])
        T2 = float(line["Tank Temperature"])
        dt = float(line["Time Step"])
# set up the paths needed to create the files
MainPath = path.relpath('TankPress-' + ts, start=curdir)
DataPath = path.join(MainPath, 'Data')
FigPath = path.join(MainPath, 'Figures')
EpsPath = path.join(FigPath, 'eps')
PngPath = path.join(FigPath, 'png')
csvfile_sel = path.join(DataPath, 'TankPress-' + ts + '-select.csv')
csvfile_ful = path.join(DataPath, 'TankPress-' + ts + '-full.csv')
csvfile_results = path.join(DataPath, 'TankPressResults.csv')

# time step: csvfile_sel.csv, select data criterion
if 0.00001 <= dt and not dt >= 0.0001:
    dt_sel = 500
elif 0.0001 <= dt and not dt >= 0.001:
    dt_sel = 250
elif 0.001 <= dt and not dt >= 0.01:
    dt_sel = 100
elif 0.01 <= dt and not dt >= 0.50:
    dt_sel = 25
else:
    dt_sel = 10

# CONSTANTS
k, Cp, CV, R, g = 1.4, 0.24, 0.17, 53.331032102174674, 32.174049
# k = specific heat ratio
# Cp = constant-pressure specific heat
# CV = constant-volume specific heat
# R = air gas constant
# g = gravitation acceleration

# Calculate Pipe Area, A1, using pipe diameter, d1
r1 = (d1 / 12) / 2  # convert d1 to ft and then halve to get radius
A1 = pi * r1 ** 2  # area of a pipe cross-section

# Pipe Temperature saved to new variable and then converted to degree Rankine
T1old = T1
T1 = T1old + 459.67
# Tank Temperature saved to new variable and then converted to degree Rankine
T2old = T2
T2 = T2old + 459.67
# Pipe Pressure saved to new variable and then converted to psf
p1old = p1
p1 = p1old * 12 ** 2
# Pipe Pressure saved to new variable and then converted to psf
p2old = p2
p2 = p2old * 12 ** 2
# Calculate specific enthalpy and specific internal energy of system
h1 = Cp * T1
u2 = CV * T2
# Calculate initial mass in tank  in lbm
m2 = (p2 * V2) / (R * T2)
# Initialize t (time) and mfr (mass flow rate) to zero.
t, mfr, iteration = 0.0, 0.0, 0

# Generate the arrays that are used to generate the plots.
PRESSURE, TEMPERATURE, MASS, MFR, INTNRG, TIME = [], [], [], [], [], []  # Set arrays
PRESSURE.append(p2old)  # append the initial conditions to the arrays
TEMPERATURE.append(T2old)
MASS.append(m2)
MFR.append(mfr)
INTNRG.append(u2)
TIME.append(t)

# MAIN PIECE
# set the headers of the csv files
a1 = 'TankPressure (PSI)'
b1 = 'Tank Temperature (' + symdeg + 'F)'
c1 = 'Mass in Tank (lbm)'
d2 = 'Mass Flow Rate into Tank (lbm/s)'
e1 = 'Specific Internal Energy (ft*lbf/lbm)'
f1 = 'Time Taken to Pressurize Tank (s)'
row1 = [f1, a1, b1, c1, d2, e1]
row2 = [t, p2old, T2old, m2, mfr, u2]  # create a row for the first row of data to the csv files
with open(csvfile_ful, 'w', newline='') as csvfile:  # open the full csv file for writing and write the header and
    # initial data rows
    CSVDATA = ss.writer(csvfile, dialect='excel')
    CSVDATA.writerow(row1)
    CSVDATA.writerow(row2)
    with open(csvfile_sel, 'w', newline='') as selcsv:  # open the select csv file for writing and write the header
        # and initial data rows
        SELDATA = ss.writer(selcsv, dialect='excel')
        SELDATA.writerow(row1)
        SELDATA.writerow(row2)
        with open(csvfile_results, 'w', newline='') as results:  # open the results file for writing
            while p2 < p1:  # while tank pressure is less than the supply line (pipe) pressure, do the following
                iteration += 1  # increment iteration by 1
                t += dt  # increment time t by time step dt
                u2old = u2  # store current value of u2 as u2old
                m2old = m2  # store current value of m2 as m2old
                p2old = p2  # store current value of p2 as p2old
                T2old = T2  # store current value of T2 as T2old
                if (p2 / p1) < ((2 / (k + 1)) ** (k / (k - 1))):  # we check if one formula of critical pressure is
                    # less than another formula of it. If the first is less than the second, we take the second;
                    # otherwise, we take the first and regardless store as pCrit
                    pCrit = (2 / (k + 1)) ** (k / (k - 1))
                else:
                    pCrit = p2 / p1
                mfr = A1 * sqrt(
                    2 * k * (p1 ** 2) * g * (pCrit ** (2 / k)) * (1 - pCrit ** ((k - 1) / k)) / ((k - 1) * R * T2old))
                # the mass flow rate mfr is a complicated formula using only T2 as the changing variable
                m2 = m2old + mfr * dt  # using the old tank mass value, we add this to the product of the just
                # calculated mass flow rate mfr and time step dt
                u2 = (m2old * u2old + mfr * dt * h1) / m2  # calculate the sum of the products of m2old and u2old and
                # mfr, dt, and h1, the result of which is divided by m2
                T2 = u2 / CV  # calculate a new temperature by dividing the just calculated u2 by CV
                p2 = (m2 * R * T2) / V2  # calculate a new p2 using a form of the ideal gas law
                p2conv = p2 / 144  # convert the pressure just calculated to psi from psf and store in p2conv
                T2conv = T2 - 459.67  # convert the temperature just calculated to deg F from deg R

                # append the current values to the arrays
                PRESSURE.append(p2conv)
                TEMPERATURE.append(T2conv)
                MASS.append(m2)
                MFR.append(mfr)
                INTNRG.append(u2)
                TIME.append(t)
                row3 = [t, p2conv, T2conv, m2, mfr, u2]  # set up the row for the csv files
                CSVDATA.writerow(row3)  # write the row to the full csv file
                if (iteration % dt_sel) == 0:  # if the iteration modulo dt_sel is zero, we write the row to the
                    # select csv file
                    SELDATA.writerow(row3)
            # set up the header row for the results csv
            timing = 'Time'
            pressure = 'Tank Pressure'
            temping = 'Tank Temperature'
            massing = 'Tank Mass'
            massflow = 'Mass Flow Rate'
            intnrge = 'Internal Energy'
            # results csv rows
            row4 = [timing, pressure, temping, massing, massflow, intnrge]
            row3 = [t, p2conv, T2conv, m2, mfr, u2]
            RESDATA = ss.writer(results, dialect='excel')  # choose the regular writer of csv module to write the rows
            RESDATA.writerow(row4)  # write header row
            RESDATA.writerow(row3)  # write data row

# PLOTS
PDFplot(PRESSURE, TEMPERATURE, MASS, MFR, INTNRG, TIME)  # generate the graphs using the functions defined at the
# beginning of the script using the arrays

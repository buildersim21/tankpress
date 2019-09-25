# Tank Pressurization Program
# Jeanette Zatowski
#
# Version
ver = '2019.0618.1620'
import csv as ss
import time
from os import makedirs, path, curdir

import matplotlib.pyplot as plt
#
# Requirements
# Python 3.6.6
# matplotlib 2.0.0+ and dependents
# math
# csv
# os
#
# Symbols with Descriptions and Units
# Symbol    # Unit              # Description
# m         # lbm               # mass
# mfr       # lbm/s             # mass flow rate
# u         # Btu/lbm           # specific internal energy
# T         # F or R            # temperature
# p         # psia or psfa      # pressure
# R         # (ft*lbf)/(lbm*R)  # specific gas constant
# k         # unitless          # specific heat ratio
# Cp        # Btu/(lbm*R)       # constant-pressure specific heat
# CV        # Btu/(lbm*R)       # constant-volume specific heat
# h         # (ft*lbf)/lbm      # specific enthalpy
# length    # in or ft          # length
# V         # ft**3 [cu. ft]    # volume
# A         # ft**2 [sq. ft]    # area
# t         # s, sec, seconds   # time
# dt        # s, sec, seconds   # time step
# 1                             # pipe conditions
# 2                             # tank conditions
# es        # unitless          # error of calculation
# pCrit     # unitless          # critical pressure
# g         # ft/(s**2)         # gravitational constant
# old                           # designates the previous value of a variable
# Unit                          # stores the unit desired to convert to
#
# Import Required Modules
from math import pi, sqrt
from matplotlib.backends.backend_pdf import PdfPages


#
def Conversion_Temperature(T, Unit):
    if Unit == 'Farenheit':
        return T + 459.67
    elif Unit == 'Rankine':
        return T - 459.67
    else:
        print("Semantic Error: Temperature conversion failed. Choose either 'Rankine' or 'Farenheit'.")


def Conversion_Pressure(p, Unit):
    if Unit == 'psi':
        return p * 144
    elif Unit == 'psf':
        return p / 144
    else:
        print("Semantic Error: Pressure conversion failed. Choose either 'psi' or 'psf'.")


def Conversion_Length(length, Unit):
    if Unit == 'ft':
        return length * 12
    elif Unit == 'in':
        return length / 12
    else:
        print("Semantic Error: Length conversion failed. Choose either 'ft' or 'in'.")


def Area(diameter):
    return pi * ((diameter / 2) ** 2)


def CritPressA(k):
    return (2 / (k + 1)) ** (k / (k - 1))


def CritPressB(p1, p2):
    return (p2 / p1)


def MassGasLaw(p2, V2, R, T2):
    return (p2 * V2) / (R * T2)


def Enthalpy_Specific(Cp, T1):
    return Cp * T1


def Internal_Specific(CV, T2):
    return CV * T2


def Pressurization(p2old, T2old, m2, mfr, u2, es, t, p2, T2, CV, Cp, k, dt, V2, d1, R, iteration, A1, p1, dt_sel, h1,
                   p1old):
    a1 = 'Tank Pressure (PSI)'
    b1 = 'Tank Temperature (F)'
    c1 = 'Mass in Tank (lbm)'
    d2 = 'Mass Flow Rate into Tank (lbm/s)'
    e1 = 'Specific Internal Energy (ft*lbf/lbm)'
    f1 = 'Error of Calculations'
    g1 = 'Time Taken to Pressurize Tank (s)'
    row1 = [g1, a1, b1, c1, d2, e1, f1]
    row2 = [t, p2old, T2old, m2, mfr, u2, es]
    with open(csvfile_ful, 'w', newline='') as csvfile:
        CSVDATA = ss.writer(csvfile, dialect='excel')
        CSVDATA.writerow(row1)
        CSVDATA.writerow(row2)
        with open(csvfile_sel, 'w', newline='') as selcsv:
            SELDATA = ss.writer(selcsv, dialect='excel')
            SELDATA.writerow(row1)
            SELDATA.writerow(row2)
            while p2 < p1:
                iteration += 1
                t += dt
                u2old = u2
                m2old = m2
                p2old = p2
                T2old = T2
                if CritPressB(p1, p2) < CritPressA(k):
                    pCrit = CritPressA(k)
                else:
                    pCrit = CritPressB(p1, p2)
                mfr = A1 * sqrt(2 * k * (p1 ** 2) * g * (pCrit ** (2 / k)) * (1 - pCrit ** ((k - 1) / k)) / ((k - 1) * R * T2))
                m2 = m2old + (mfr * dt)
                u2 = (m2old * u2old + mfr * dt * h1) / m2
                T2 = u2 / CV
                p2 = (m2 * R * T2) / V2
                es = abs(p2 - p1) / p1
                p2conv = Conversion_Pressure(p2, 'psf')
                T2conv = Conversion_Temperature(T2, 'Rankine')
                PRESSURE.append(p2conv)
                TEMPERATURE.append(T2conv)
                MASS.append(m2)
                MFR.append(mfr)
                INTNRG.append(u2)
                ERR.append(es)
                TIME.append(t)
                row3 = [t, p2conv, T2conv, m2, mfr, u2, es]
                CSVDATA.writerow(row3)
                if (iteration % dt_sel) == 0:
                    SELDATA.writerow(row3)
            # print results to screen
            print(z * 3)
            print('It took {0:5d} iterations to complete this simulation model.'.format(iteration))
            print('The final pressure inside the tank is {0:3.6f} psia.'.format(Conversion_Pressure(p2, 'psf')))
            print('The final temperature inside the tank is {0: 3.6f}°F.'.format(Conversion_Temperature(T2, 'Rankine')))
            print('The final mass inside the tank is {0:3.6f} lbm.'.format(m2))
            print('The final mass flow rate into the tank is {0:3.6f} lbm/s.'.format(mfr))
            print('The final specific internal energy inside the tank is {0:3.6f} ft * lbf / lbm.'.format(u2))
            print('The final error of the calculations is {0:3.6f} (unitless).'.format(es))
            print('The time taken to pressurize the tank is {0:3.6f} seconds.'.format(t))
            print(z * 3)
            # print results to file
            with open(logfile, 'a') as log:
                log.write(z * 3)
                log.write('It took {0:5d} iterations to complete this simulation model.\n'.format(iteration))
                log.write(
                    'The final pressure inside the tank is {0:3.6f} psia.\n'.format(Conversion_Pressure(p2, 'psf')))
                log.write('The final temperature inside the tank is {0: 3.6f}°F.\n'.format(
                    Conversion_Temperature(T2, 'Rankine')))
                log.write('The final mass inside the tank is {0:3.6f} lbm.\n'.format(m2))
                log.write('The final mass flow rate into the tank is {0:3.6f} lbm / s.\n'.format(mfr))
                log.write('The final specific internal energy inside the tank is {0:3.6f} ft * lbf / lbm.\n'.format(u2))
                log.write('The final error of the calculations is {0:.6f} (unitless).\n'.format(es))
                log.write('The time taken to pressurize the tank is {0:3.6f} seconds.\n.'.format(t))
                log.write(z * 3)


# __________________________________________
# Plotting Definition #
#
def multipage(filename, figs=None, dpi=300):
    with PdfPages(filename) as pdf:
        if figs is None:
            figs = [plt.figure(n) for n in plt.get_fignums()]
        for fig in figs:
            pdf.savefig(fig)


def plotation(xvar, yvar, xlab, ylab, figtitle, figname):
    plt.figure(dpi=300, figsize=[6, 6])
    plt.plot(xvar, yvar)
    plt.xlim(min(xvar), max(xvar))
    plt.ylim(min(yvar), max(yvar))
    plt.title(figtitle, size='large', style='oblique', va='baseline', weight='bold')
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.grid(b='on', which='major', axis='both')
    pngfile = path.join(PngPath, figname + '-' + ts + '.png')
    epsfile = path.join(EpsPath, figname + '-' + ts + '.eps')
    plt.savefig(pngfile, dpi=300, format='png')
    plt.savefig(epsfile, format='eps')


def PDFplot(PRESSURE, TEMPERATURE, MASS, MFR, INTNRG, ERR, TIME):
    pdffile = path.join(FigPath, 'TankPress-' + ts + '.pdf')
    y1var = PRESSURE
    y2var = TEMPERATURE
    y3var = y1var
    y4var = MASS
    y5var = MFR
    y6var = ERR
    x1var = TIME
    x2var = y2var
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
    fig6_ylab = 'Error of Calculations (Unitless)'
    fig6_pt = 'Error of Calculations Over Time'
    fig6_name = 'ERR-Time-Rel'

    fig1 = plotation(x1var, y1var, fig1_xlab, fig1_ylab, fig1_pt, fig1_name)
    fig2 = plotation(x1var, y2var, fig2_xlab, fig2_ylab, fig2_pt, fig2_name)
    fig3 = plotation(x2var, y3var, fig3_xlab, fig3_ylab, fig3_pt, fig3_name)
    fig4 = plotation(x1var, y4var, fig4_xlab, fig4_ylab, fig4_pt, fig4_name)
    fig5 = plotation(x1var, y5var, fig5_xlab, fig5_ylab, fig5_pt, fig5_name)
    fig6 = plotation(x1var, y6var, fig6_xlab, fig6_ylab, fig6_pt, fig6_name)
    multipage(pdffile)
    plt.close()


# __________________________________________
# Divisor for display
#
dots = '.................................\n'
# __________________________________________
# Print to Screen
#
print('Hello, user.')
print('Welcome to TankPress version ' + ver + '.')
while True:
    try:
        ts = input('Please select and input a string of characters to distinguish this run.\t')
        MainPath = path.relpath('TankPress-' + ts, start=curdir)
        if not path.exists(MainPath):
            DataPath = path.join(MainPath, 'Data')
            FigPath = path.join(MainPath, 'Figures')
            LogPath = path.join(MainPath, 'Log')
            EpsPath = path.join(FigPath, 'eps')
            PngPath = path.join(FigPath, 'png')
            makedirs(DataPath)
            makedirs(FigPath)
            makedirs(LogPath)
            makedirs(EpsPath)
            makedirs(PngPath)
            break
    except Exception:
        print('Free up the folder space for the new run')
        continue
logfile = path.join(LogPath, 'TankPress' + ts + '.txt')
csvfile_sel = path.join(DataPath, 'TankPress-' + ts + '-select.csv')
csvfile_ful = path.join(DataPath, 'TankPress-' + ts + '-full.csv')
#
# __________________________________________
# Start log file
#
with open(logfile, 'w') as log:
    a = 'Welcome to TankPress version ' + ver + '.'
    b = 'Please select and input a string of characters to distinguish this run.\t'
    c = 'Initially, a rigid insulated tank of air at an initial pressure and temperature and a supply line are connected by a valve.'
    d = 'Air flows through the supply line with a pressure and temperature.'
    e = 'When the valve opens, air enters the tank until the pressure equalizes to that of the supply line, at which point the valve is closed.'
    f = 'This program calculates the final values of the pressure, temperature, and mass of air inside the tank, as well as the last mass flow rate before valve closure, the time it takes to pressurize the tank, and the error of the calculations.'
    cc = 'Enter the supply line diameter in inches.\t'
    h = 'Please try again. The input must be a number.'
    i = 'Enter the tank volume in cubic feet.\t\t'
    j = 'Enter the supply line temperature in °F.\t'
    bb = 'Enter the initial tank temperature in °F\t'
    l = 'Enter the supply line pressure in psia.\t\t'
    m = 'Enter the initial tank pressure in psia.\t'
    aa = 'The initial tank pressure must be less than the supply line pressure. [p2 < p1]'
    o = 'Enter the time step in seconds.\t\t\t'
    p = 'Please try again. The tank volume must be greater than zero. [V2 > 0]'
    q = 'Please try again. The temperature must be greater than absolute zero. [T > - 459.67°F]'
    r = 'Please try again. The pressure must be greater than zero. [p > 0]'
    s = 'Please try again. The time step must be greater than zero and less than one. [dt = (0.00001, 1)]'
    dd = 'Please try again. The supply line diameter must be greater than zero. [d1 > 0]'
    y = '\n'
    z = '.................................\n'
    print(z * 3)
    print(c)
    print(d)
    print(e)
    print(f)
    print(z * 3)
    log.write(a + y)
    log.write(b + y)
    log.write(z * 3)
    log.write(c + y)
    log.write(d + y)
    log.write(e + y)
    log.write(f + y)
    log.write(z * 3)
    # __________________________________________
    # Input pipe diameter #
    while True:
        try:
            d1 = float(input(cc))
            log.write(cc + '{0}'.format(d1) + y)
        except ValueError:
            print(h)
            log.write(h + y)
            continue
        if d1 <= 0:
            print(dd)
            log.write(dd + y)
            continue
        else:
            break
    # __________________________________________
    # Input tank volume
    while True:
        try:
            V2 = float(input(i))
            log.write(i + '{0}'.format(V2) + y)
        except ValueError:
            print(h)
            log.write(h + y)
            continue
        if V2 <= 0:
            print(p)
            log.write(p + y)
            continue
        else:
            break
    # __________________________________________
    # Input pipe temperature
    while True:
        try:
            T1 = float(input(j))
            log.write(j + '{0}'.format(T1) + y)
        except ValueError:
            print(h)
            log.write(h + y)
            continue
        if T1 < -459.67:
            print(q)
            log.write(q + y)
            continue
        else:
            break
    # __________________________________________
    # Input initial tank temperature
    while True:
        try:
            T2 = float(input(bb))
            log.write(j + '{0}'.format(T2) + y)
        except ValueError:
            print(h)
            log.write(h + y)
            continue
        if T2 < -459.67:
            print(q)
            log.write(q + y)
            continue
        else:
            break
    # __________________________________________
    # Input pipe and tank pressures
    while True:
        try:
            while True:
                try:
                    p1 = float(input(l))
                    log.write(l + '{0}'.format(p1) + y)
                except ValueError:
                    print(h)
                    log.write(h + y)
                    continue
                if p1 <= 0:
                    print(r)
                    log.write(r + y)
                    continue
                else:
                    break
            while True:  # currently continually asking for tank pressure #TODO!!
                try:
                    p2 = float(input(m))
                    log.write(m + '{0}'.format(p2) + y)
                except ValueError:
                    print(h)
                    log.write(h + y)
                    continue
                if p2 <= 0:
                    print(r)
                    log.write(r + y)
                    continue
                else:
                    break
        except ValueError:
            print(h)
            log.write(h + y)
            continue
        if p2 >= p1:
            print(aa)
            log.write(aa + y)
            continue
        else:
            break
    # __________________________________________
    # Input time step
    while True:
        try:
            dt = float(input(o))
            log.write(o + '{0}'.format(dt) + y)
        except ValueError:
            print(h)
            log.write(h + y)
            continue
        if dt >= 1:
            print(s)
            log.write(s + y)
        elif dt <= 0.00001:
            print(s)
            log.write(s + y)
        else:
            if dt >= 0.00001 and dt < 0.0001:
                dt_sel = 500
                break
            elif dt >= 0.0001 and dt < 0.001:
                dt_sel = 250
                break
            elif dt >= 0.001 and dt < .01:
                dt_sel = 100
                break
            elif dt >= 0.01 and dt < 0.50:
                dt_sel = 25
                break
            else:
                dt_sel = 10
                break
# __________________________________________
#
start_time = time.time()
# __________________________________________
# Constants
k, Cp, CV, R, g = 1.4, 0.24, 0.17, 53.331032102174674, 32.174049
# __________________________________________
# Conversions and Calculations
A1 = Area(Conversion_Length(d1, 'in'))
T1 = Conversion_Temperature(T1, 'Farenheit')
T2old = T2  # save unconverted T2 for csv and plot steps
T2 = Conversion_Temperature(T2, 'Farenheit')
p1old = p1
p1 = Conversion_Pressure(p1, 'psi')
p2old = p2  # save unconverted P2 for csv and plot steps
p2 = Conversion_Pressure(p2, 'psi')
h1 = Enthalpy_Specific(Cp, T1)
u2 = Internal_Specific(CV, T2)
m2 = MassGasLaw(p2, V2, R, T2)
t, iteration, mfr = 0.0, 0, 0.0
es = abs((p2 - p1) / p1)
# __________________________________________
# Initialize and Append Initial Values to Arrays
PRESSURE, TEMPERATURE, MASS, MFR, INTNRG, ERR, TIME = [], [], [], [], [], [], []
#
PRESSURE.append(p2old)
TEMPERATURE.append(T2old)
MASS.append(m2)
MFR.append(mfr)
INTNRG.append(u2)
ERR.append(es)
TIME.append(t)
# __________________________________________
# Main Calculation
Pressurization(p2old, T2old, m2, mfr, u2, es, t, p2, T2, CV, Cp, k, dt, V2, d1, R, iteration, A1, p1, dt_sel, h1, p1old)
# __________________________________________
# Plots
PDFplot(PRESSURE, TEMPERATURE, MASS, MFR, INTNRG, ERR, TIME)
# __________________________________________
end_time = time.time()
timing = end_time - start_time
print(
    'It took {0:.4f} seconds to go through the process after inputting the initial conditions to creating a multipage PDF of the plots.'.format(
        timing))
print(dots)
with open(logfile, 'a') as log:
    log.write(
        'It took {0:.4f} seconds to go through the process after inputing the initial conditions to creating a multipage PDF of the plots.\n'.format(
            timing))
    # __________________________________________
    log.write(dots)
    log.write('Press any key to exit.\n')
endgame = input('Press any key to exit.')

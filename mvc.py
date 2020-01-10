import tkinter as tk

import matplotlib as mpl
mpl.use("TkAgg")  # MUST be invoked prior to importing mpl backends!
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)  # NavigationToolbar2TkAgg was deprecated
import numpy as np
import PySimpleGUI as sg


# To test PySimpleGUI, the MPLgraph class was borrowed from my other code projects.
class MPLgraph(FigureCanvasTkAgg):
    """The canvas-like matplotlib object used by View.

    """
    def __init__(self, figure, parent=None, **options):
        """
        argument:
            figure: a matplotlib.figure.Figure object
        """
        FigureCanvasTkAgg.__init__(self, figure, parent, **options)
        self.figure = figure
        self.add = figure.add_subplot(111)
        # .show() was deprecated and changed to .draw(). See:
        # https://github.com/matplotlib/matplotlib/pull/9275
        self.draw()
        self.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self, parent)
        self.toolbar.update()

    def plot(self, x, y):
        """Take two arrays for x and y coordinates and plot the data."""
        self.add.plot(x, y)
        self.figure.canvas.draw()  # DRAW IS CRITICAL TO REFRESH

    def clear(self):
        """Erase the plot."""
        self.add.clear()
        self.figure.canvas.draw()


def powerplot(base, exponent):
    """
    Calculates data for plotting the function: y = (base * x) ** exponent,
    for x = 0...10.
    Arguments: base and exponent as floats
    Returns: two numpy arrays of x and y coordinates (length 800).
    """

    x = np.linspace(0, 10, 800)
    y = (x * base) ** exponent
    return x, y


figure_w, figure_h = 500, 500
layout = [
    [sg.Text('base'), sg.InputText('1'), sg.Text('exponent'), sg.InputText('1')],
    [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
    [sg.Submit(), sg.Exit()]
]
window = sg.Window('MVC Test', layout, grab_anywhere=True, finalize=True)
figure = mpl.figure.Figure(figsize=(5, 4), dpi=100)
canvas = MPLgraph(figure, window['-CANVAS-'].TKCanvas)
canvas._tkcanvas.pack(side=tk.BOTTOM, expand=tk.YES, fill=tk.BOTH)
canvas.plot(*powerplot(1, 1))

while True:
    event, values = window.Read()  # event = name of event; values = {0: str, 0: str} of entry values
    if event in (None, 'Exit'):  # If user closed window with X or if user clicked "Exit" event then exit
        break
    if event == 'Submit':
        x, y = powerplot(float(values[0]), float(values[1]))
        canvas.clear()
        canvas.plot(x, y)
window.close()

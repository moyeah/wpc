#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gobject
import gtk
import itertools

from numpy import arange
from scipy.stats import exponweib
from math import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
from matplotlib.backend_bases import key_press_handler

class WindGraph(gtk.Window):
  def table(self, winds, subplot, step):
    x = []
    y = []

    for wind, next_wind in itertools.izip(winds, winds[1:]):
      u = float(wind[0])
      u1 = float(next_wind[0])

      while u < u1:
        x.append(u)
        y.append(float(eval(wind[1])))
        u += step*(u1-u)

    x.append(float(winds[-1][0]))
    y.append(float(eval(winds[-1][1])))

    subplot.plot(x, y)

  def weibull(self, weibull, subplot, step):
    shape = weibull[0]
    scale = weibull[1]
    stop = weibull[2]
    numargs = exponweib.numargs
    [a, c] = [weibull[0]] * numargs
    rv = exponweib(a, c, scale=weibull[1])
    x = arange(start=0, stop=weibull[2], step=step)
    subplot.plot(x, rv.pdf(x)*100)

  def __init__(self, winds=None, weibull=None, step=0.5, title="Wind Graph", parent=None):
    gtk.Window.__init__(self)
 
    try:
      self.set_screen(parent.get_screen())
    except AttributeError:
      self.connect('destroy', lambda *w: self.destroy())

    if parent is not None:
      self.set_parent(parent)
    self.set_title(title)
    self.set_destroy_with_parent(True)
    self.set_default_size(600, 400)

    vbox = gtk.VBox()
    self.add(vbox)

    figure = Figure(figsize=(5,4), dpi=100)
    subplot = figure.add_subplot(111)
    subplot.set_title("Wind Distribution")
    subplot.set_xlabel("Speed (u) [m/s]")
    subplot.set_ylabel("Probability density [%]")
    subplot.grid(True)

    if winds is not None:
      self.table(winds, subplot, step)
    elif weibull is not None:
      self.weibull(weibull, subplot, step/2)

    self.canvas = FigureCanvas(figure)
    self.canvas.mpl_connect('key_press_event', self.on_key_event)
    vbox.pack_start(self.canvas)

    self.toolbar = NavigationToolbar(self.canvas, self)
    vbox.pack_start(self.toolbar, False, False)

    self.show_all()

  def on_key_event(self, event):
    key_press_handler(event, self.canvas, self.toolbar)

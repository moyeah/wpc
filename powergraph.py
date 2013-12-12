#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gobject
import gtk
import itertools

from numpy import linspace
from math import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
from matplotlib.backend_bases import key_press_handler

class PowerGraph(gtk.Window):
  def __init__(self, powers, step=0.5, title="Power Graph", parent=None):
    x = []
    y = []

    for power, next_power in itertools.izip(powers, powers[1:]):
      u = float(power[0])
      u1 = float(next_power[0])

      while u < u1:
        x.append(u)
        y.append(float(eval(power[1])))
        u += step*(u1-u)

    x.append(float(powers[-1][0]))
    y.append(float(eval(powers[-1][1])))

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
    subplot.plot(x, y)
    subplot.set_title("Power Graph")
    subplot.set_xlabel("Speed (u) [m/s]")
    subplot.set_ylabel("Power [kW]")
    subplot.grid(True)

    self.canvas = FigureCanvas(figure)
    self.canvas.mpl_connect('key_press_event', self.on_key_event)
    vbox.pack_start(self.canvas)

    self.toolbar = NavigationToolbar(self.canvas, self)
    vbox.pack_start(self.toolbar, False, False)

    self.show_all()

  def on_key_event(self, event):
    key_press_handler(event, self.canvas, self.toolbar)

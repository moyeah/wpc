#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gobject
import gtk
import itertools

from scipy.stats import exponweib
from math import *

import powercells as pc
import powergraph as pg
import wpcutils as wpc
import windcells as wc
import windgraph as wg

authors = ["Daniel Sousa <1000146@isep.ipp.pt>",
           "Eugénio Xavier <1130200@isep.ipp.pt>",
           "António Correia <1130199@isep.ipp.pt>"]

class WeibullDist:
  def __init__(self, table):
    self.scale = 0.0
    self.shape = 0.0

    self.label = []
    self.entry = []

    self.label.append(gtk.Label())
    self.label[-1].set_alignment(xalign=0.0, yalign=0.5)
    self.label[-1].set_text_with_mnemonic("S_cale (c) [m/s]:")
    table.attach(self.label[-1], 0, 1, 1, 2,
                 xoptions=gtk.FILL, yoptions=gtk.FILL)

    self.entry.append(gtk.Entry())
    self.entry[-1].set_text(str(self.scale))
    self.entry[-1].connect_after('focus-out-event', self.on_focus_out_scale)
    self.label[-1].set_mnemonic_widget(self.entry[-1])
    table.attach(self.entry[-1], 1, 2, 1, 2, yoptions=gtk.FILL)

    self.label.append(gtk.Label())
    self.label[-1].set_alignment(xalign=0.0, yalign=0.5)
    self.label[-1].set_text_with_mnemonic("S_hape (k):")
    table.attach(self.label[-1], 0, 1, 3, 4,
                 xoptions=gtk.FILL, yoptions=gtk.FILL)

    self.entry.append(gtk.Entry())
    self.entry[-1].set_text(str(self.shape))
    self.entry[-1].connect_after('focus-out-event', self.on_focus_out_shape)
    self.label[-1].set_mnemonic_widget(self.entry[-1])
    table.attach(self.entry[-1], 1, 2, 3, 4, yoptions=gtk.FILL)

  def destroy(self):
    for l in self.label:
      l.destroy()

    for e in self.entry:
      e.destroy()

  def set_entry(self, widget):
    try:
      widget.set_text(str(fabs(float(eval(widget.get_text())))))
      retval = True
    except (SyntaxError, NameError, TypeError, ValueError), error:
      wpc.error_dialog(error)
      retval = False

    return retval

  def on_focus_out_scale(self, widget, event):
    if self.set_entry(widget):
      self.scale = float(widget.get_text())
      return False

    widget.set_text(str(self.scale))
    return False

  def on_focus_out_shape(self, widget, event):
    if self.set_entry(widget):
      self.shape = float(widget.get_text())
      return False

    widget.set_text(str(self.shape))
    return False

  def get_scale(self):
    return self.scale

  def get_shape(self):
    return self.shape

class AppWindow(gtk.Window):
  def about_dialog_clicked(self, widget):
    dialog = gtk.AboutDialog()
    dialog.set_program_name("Wind Power Calculator")
    dialog.set_version("v1.0")
    dialog.set_copyright("Dezember 2013")
    dialog.set_authors(authors)
    dialog.show_all()
    dialog.run()
    dialog.destroy()

  def on_open_clicked(self, button, power_cells):
    pass

  def on_cbox_changed(self, widget, table):
    index = widget.get_active()

    if index == 0:
      try:
        self.wc.destroy()
        self.wbbox.destroy()
      except:
        pass
      self.wd = WeibullDist(table)
      table.show_all()
      return

    if index == 1:
      try:
        self.wd.destroy()
        self.wc.destroy()
        self.wbbox.destroy()
      except:
        pass
      table.show_all()
      return

    if index == 2:
      try:
        self.wd.destroy()
      except:
        pass
      self.wc = wc.WindCells(border=0)
      table.attach(self.wc, 0, 2, 1, 2)
      table.show_all()

      self.wbbox = wc.WindButtonBox(self.box, self.wc)
      self.box.show_all()
      return

  def on_plot_wind_clicked(self, widget, cbox):
    index = cbox.get_active()

    if index == 0:
      wg.WindGraph(weibull=[self.wd.get_shape(),
                            self.wd.get_scale(),
                            float(self.power_cells.get_powers()[-1][0])])
      return

    if index == 1:
      return

    if index == 2:
      wg.WindGraph(winds=self.wc.get_winds())


  def __init__(self, parent=None, title="Wind Power Calculator"):
    gtk.Window.__init__(self)

    try:
      self.set_screen(parent.get_screen())
    except AttributeError:
      self.connect('destroy', lambda *w: gtk.main_quit())

    self.set_title(title)
    self.set_default_size(800, 600)
    self.set_border_width(5)
    self.set_position(gtk.WIN_POS_CENTER)

    main_vbox = gtk.VBox()
    self.add(main_vbox)

    hbox = gtk.HBox()
    main_vbox.pack_start(hbox)

    frame = gtk.Frame("Power")
    hbox.pack_start(frame, padding=5)

    box = gtk.VBox()
    frame.add(box)

    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(gtk.BUTTONBOX_END)
    bbox.set_spacing(5)
    box.pack_start(bbox, False, False)

    button = gtk.Button(stock='gtk-open')
    button.connect('clicked', lambda *w: gtk.main_quit())
    bbox.add(button)

    button = gtk.Button(stock='gtk-save')
    button.connect('clicked', lambda *w: gtk.main_quit())
    bbox.add(button)

    self.power_cells = pc.PowerCells()
    box.pack_start(self.power_cells)

    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(gtk.BUTTONBOX_END)
    bbox.set_spacing(5)
    box.pack_start(bbox, False, False)

    button = gtk.Button(stock='gtk-add')
    button.connect('clicked', lambda *w: self.power_cells.add_item())
    bbox.add(button)

    button = gtk.Button(stock='gtk-remove')
    button.connect('clicked', lambda *w: self.power_cells.remove_item())
    bbox.add(button)

    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(gtk.BUTTONBOX_END)
    bbox.set_spacing(5)
    box.pack_start(bbox, False, False)

    button = gtk.Button(label='Plot _Power Graph')
    button.connect('clicked', lambda *w: pg.PowerGraph(self.power_cells.get_powers()))
    bbox.add(button)

    frame = gtk.Frame("Wind")
    hbox.pack_start(frame, padding=5)

    box = gtk.VBox()
    self.box = box
    frame.add(box)

    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(gtk.BUTTONBOX_END)
    bbox.set_spacing(5)
    box.pack_start(bbox, False, False)

    button = gtk.Button(stock='gtk-open')
    button.connect('clicked', lambda *w: gtk.main_quit())
    bbox.add(button)

    button = gtk.Button(stock='gtk-save')
    button.connect('clicked', lambda *w: gtk.main_quit())
    bbox.add(button)

    table = gtk.Table()
    table.set_border_width(5)
    table.set_row_spacings(5)
    table.set_col_spacings(5)
    box.pack_start(table)

    label = gtk.Label()
    label.set_alignment(xalign=0.0, yalign=0.5)
    label.set_text_with_mnemonic("_Type:")
    table.attach(label, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL)

    texts = ("Weibull Distribution",
             "Rayleigh Distribution",
             "Table")

    cbox = gtk.combo_box_new_text()
    for text in texts:
      cbox.append_text(text)
    cbox.connect('changed', self.on_cbox_changed, table)
    cbox.set_active(0)
    label.set_mnemonic_widget(cbox)
    table.attach(cbox, 1, 2, 0, 1, yoptions=gtk.FILL)

    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(gtk.BUTTONBOX_END)
    bbox.set_spacing(5)
    box.pack_end(bbox, False, False)

    button = gtk.Button(label='Plot _Wind Graph')
    button.connect('clicked', self.on_plot_wind_clicked, cbox)
    bbox.add(button)

    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(gtk.BUTTONBOX_END)
    bbox.set_spacing(5)
    main_vbox.pack_end(bbox, False, False)

    button = gtk.Button(stock='gtk-close')
    button.connect('clicked', lambda *w: gtk.main_quit())
    bbox.add(button)

    button = gtk.Button(stock='gtk-execute')
    button.connect('clicked', self.on_execute_clicked, cbox)
    bbox.add(button)

    button = gtk.Button(stock='gtk-about')
    button.connect('clicked', self.about_dialog_clicked)
    bbox.add(button)

    self.show_all()

  def on_execute_clicked(self, widget, cbox, step=.5):
    pg.PowerGraph(self.power_cells.get_powers())
    self.on_plot_wind_clicked(widget, cbox)

    powers = self.power_cells.get_powers()
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

    energy = 0.0
    shape = float(self.wd.get_shape())
    scale = float(self.wd.get_scale())
    index = cbox.get_active()
    if index == 0:
      for i in range(len(x)):
        u = float(x[i])
        power = float(y[i])
        if(power > 0):
          energy += power * (shape/scale) * (u / scale)**(shape - 1) * exp(-(u / scale)**shape) * 8.760
      return

    if index == 1:
      return

    if index == 2:
      return

  def main(self):
    gtk.main()

if __name__ == '__main__':
  AppWindow().main()

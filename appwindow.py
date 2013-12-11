#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gobject
import gtk

import powercells as pc

class AppWindow(gtk.Window):
  def about_dialog_clicked(self, widget):
    dialog = gtk.AboutDialog()
    dialog.set_program_name("Wind Power Calculator")
    dialog.set_version("v1.0")
    dialog.set_copyright("Dezember 2013")
    dialog.set_authors(["Daniel Sousa", "Eugénio Xavier", "António"])
    dialog.show_all()
    dialog.run()
    dialog.destroy()

  def __init__(self, parent=None, title="Wind Power Calculator"):
    gtk.Window.__init__(self)

    try:
      self.set_screen(parent.get_screen())
    except:
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

    power_cells = pc.PowerCells()
    box.pack_start(power_cells)

    frame = gtk.Frame("Wind")
    hbox.pack_start(frame, padding=5)

    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(gtk.BUTTONBOX_END)
    bbox.set_spacing(5)
    main_vbox.pack_end(bbox, False, False)

    button = gtk.Button(stock='gtk-close')
    button.connect('clicked', lambda *w: gtk.main_quit())
    bbox.add(button)

    button = gtk.Button(stock='gtk-execute')
    button.connect('clicked', lambda *w: gtk.main_quit())
    bbox.add(button)

    button = gtk.Button(stock='gtk-about')
    button.connect('clicked', self.about_dialog_clicked)
    bbox.add(button)

    self.show_all()

  def main(self):
    gtk.main()

if __name__ == '__main__':
  AppWindow().main()

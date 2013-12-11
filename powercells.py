#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gobject
import gtk

# columns
(
  COLUMN_SPEED,
  COLUMN_POWER,
  COLUMN_EDITABLE
) = range(3)

# data
powers = [["0.0", "0.0", True]]

class PowerCells(gtk.ScrolledWindow):
  def __init__(self, parent=None, border=5):
    gtk.ScrolledWindow.__init__(self)

    self.set_border_width(border)
    self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
    self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

    # create data
    model = self.__create_model()

    # create treeview
    treeview = gtk.TreeView(model)
    treeview.set_rules_hint(True)
    treeview.get_selection().set_mode(gtk.SELECTION_SINGLE)
    self.add(treeview)

    self.__add_columns(treeview)

    self.show_all()

  def __create_model(self):
    # create list store
    model = gtk.ListStore(gobject.TYPE_STRING,
                          gobject.TYPE_STRING,
                          gobject.TYPE_BOOLEAN)

    # add itens
    for item in powers:
      iter = model.append()

      model.set(iter,
                COLUMN_SPEED, item[COLUMN_SPEED],
                COLUMN_POWER, item[COLUMN_POWER],
                COLUMN_EDITABLE, item[COLUMN_EDITABLE])

    return model

  def __add_columns(self, treeview):
    model = treeview.get_model()

    # speed column
    renderer = gtk.CellRendererText()
    renderer.set_data("column", COLUMN_SPEED)
    renderer.connect('edited', self.on_cell_edited, model)

    column = gtk.TreeViewColumn("u [m/s]", renderer,
                                text=COLUMN_SPEED,
                                editable=COLUMN_EDITABLE)
    treeview.append_column(column)

    # power column
    renderer = gtk.CellRendererText()
    renderer.set_data("column", COLUMN_POWER)
    renderer.connect('edited', self.on_cell_edited, model)

    column = gtk.TreeViewColumn("P(u) [kW]", renderer,
                                text=COLUMN_POWER,
                                editable=COLUMN_EDITABLE)
    treeview.append_column(column)

  def on_cell_edited(self, cell, path_string, new_text, model):
    iter = model.get_iter_from_string(path_string)
    path = model.get_path(iter)[0]
    column = cell.get_data("column")

    if column == COLUMN_SPEED:
      powers[path][COLUMN_SPEED] = new_text
      model.set(iter, column, powers[path][COLUMN_SPEED])

    elif column == COLUMN_POWER:
      powers[path][COLUMN_POWER] = new_text
      model.set(iter, column, powers[path][COLUMN_POWER])

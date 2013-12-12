#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gobject
import gtk

from math import *

import wpcutils as wpc

# columns
(
  COLUMN_SPEED,
  COLUMN_WIND,
  COLUMN_EDITABLE
) = range(3)

# data
winds = [["0.0", "0.0", True]]

class WindButtonBox(gtk.HButtonBox):
  def __init__(self, box, wc):
    gtk.HButtonBox.__init__(self)
    self.set_border_width(5)
    self.set_layout(gtk.BUTTONBOX_END)
    self.set_spacing(5)
    box.pack_start(self, False, False)

    button = gtk.Button(stock='gtk-add')
    button.connect('clicked', lambda *w: wc.add_item())
    self.add(button)

    button = gtk.Button(stock='gtk-remove')
    button.connect('clicked', lambda *w: wc.remove_item())
    self.add(button)

class WindCells(gtk.ScrolledWindow):
  def __init__(self, parent=None, border=5):
    gtk.ScrolledWindow.__init__(self)

    self.set_border_width(border)
    self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
    self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

    # create data
    self.model = self.__create_model()

    # create treeview
    self.treeview = gtk.TreeView(self.model)
    self.treeview.set_rules_hint(True)
    self.treeview.get_selection().set_mode(gtk.SELECTION_SINGLE)
    self.add(self.treeview)

    self.__add_columns(self.treeview)

    self.show_all()

  def __create_model(self):
    # create list store
    model = gtk.ListStore(gobject.TYPE_STRING,
                          gobject.TYPE_STRING,
                          gobject.TYPE_BOOLEAN)

    self.__add_itens(model)

    return model

  def __add_itens(self, model):

    # add itens
    for item in winds:
      iter = model.append()

      model.set(iter,
                COLUMN_SPEED, item[COLUMN_SPEED],
                COLUMN_WIND, item[COLUMN_WIND],
                COLUMN_EDITABLE, item[COLUMN_EDITABLE])

  def __add_columns(self, treeview):
    model = treeview.get_model()

    # speed column
    renderer = gtk.CellRendererText()
    renderer.set_data("column", COLUMN_SPEED)
    renderer.connect('edited', self.on_cell_edited, model)

    column = gtk.TreeViewColumn("u [m/s]", renderer,
                                text=COLUMN_SPEED,
                                editable=COLUMN_EDITABLE)
    column.set_sort_column_id(COLUMN_SPEED)
    treeview.append_column(column)

    # wind column
    renderer = gtk.CellRendererText()
    renderer.set_data("column", COLUMN_WIND)
    renderer.connect('edited', self.on_cell_edited, model)

    column = gtk.TreeViewColumn("f(u) [%]", renderer,
                                text=COLUMN_WIND,
                                editable=COLUMN_EDITABLE)
    column.set_sort_column_id(COLUMN_WIND)
    treeview.append_column(column)

  def on_cell_edited(self, cell, path_string, new_text, model):
    column = cell.get_data("column")

    try:
      value = float(eval(new_text))
      if(value < 0):
        value = 0.0
    except (SyntaxError, TypeError, ValueError), error:
      wpc.error_dialog(error)
    except NameError:
      if column == COLUMN_WIND:
        u = 1
        try:
          float(eval(new_text))
          value = new_text
        except (SyntaxError, TypeError, ValueError, NameError), error:
          wpc.error_dialog(error)

    if 'value' in locals():
      iter = model.get_iter_from_string(path_string)
      path = model.get_path(iter)[0]

      if column == COLUMN_SPEED:
        winds[path][COLUMN_SPEED] = str(value)
        winds.sort(key = lambda x: float(x[0]))
        model.clear()
        self.__add_itens(model)

      elif column == COLUMN_WIND:
        winds[path][COLUMN_WIND] = str(value)
        model.set(iter, column, winds[path][COLUMN_WIND])

  def get_winds(self):
    return winds

  def get_model(self):
    return self.model

  def add_item(self):
    new_item = ["0.0", "0.0", True]
    winds.insert(0, new_item)

    iter = self.model.insert_before(self.model.get_iter_root())
    self.model.set(iter,
                   COLUMN_SPEED, new_item[COLUMN_SPEED],
                   COLUMN_WIND, new_item[COLUMN_WIND],
                   COLUMN_EDITABLE, new_item[COLUMN_EDITABLE])

  def remove_item(self):
    selection = self.treeview.get_selection()
    model, iter = selection.get_selected()

    if iter:
      path = model.get_path(iter)[0]
      model.remove(iter)

      del winds[path]

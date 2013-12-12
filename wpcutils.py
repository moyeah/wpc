#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gobject
import gtk

def error_dialog(error):
  error = str(error)
  error = error[:1].upper() + error[1:]
  dialog = gtk.MessageDialog(None,
                             gtk.DIALOG_DESTROY_WITH_PARENT,
                             gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                             error)
  dialog.set_title("Error...")
  dialog.run()
  dialog.destroy()

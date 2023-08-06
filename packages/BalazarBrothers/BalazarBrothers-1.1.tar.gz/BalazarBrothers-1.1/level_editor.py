# Balazar Brothers
# Copyright (C) 2006-2007 Jean-Baptiste LAMY
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import soya, soya.editor

import balazar_brothers, balazar_brothers.init_editobj
from balazar_brothers.platform import Platform, PortailPlatform
from balazar_brothers.level import Level

import editobj, editobj.main, editobj.editor as editor, editobj.custom as custom
import Tkinter, dircache, os, os.path


class LevelEditor(Tkinter.Toplevel):
  def __init__(self):
    # Get, or create if needed, the root Tk.
    try:
      from Tkinter import _default_root
      tkroot = _default_root
    except ImportError: pass
    if not tkroot:
      tkroot = Tkinter.Tk(className = "Balazar Brothers Level Editor")
      tkroot.withdraw()
      
    tkroot.option_add("*bd", 1)
    tkroot.option_add("*List.background", "#FFFFFF")
    tkroot.option_add("*Text.background", "#FFFFFF")
    tkroot.option_add("*Text.relief", "flat")
    tkroot.option_add("*Entry.background", "#FFFFFF")
    tkroot.option_add("*Entry.relief", "flat")
    
    Tkinter.Toplevel.__init__(self, tkroot)

    soya.MainLoop()
    
    self.new_level_button = Tkinter.Button(self, text = _(u"New level..."), command = self.on_new_level)
    self.new_level_button.pack(fill = Tkinter.BOTH, side = Tkinter.BOTTOM)
    
    self.level_list = Tkinter.Listbox(self, background = "#FFFFFF", selectbackground = "#CCCCFF")
    for i, filename in enumerate(Level.availables()):
      self.level_list.insert(i, filename)
    self.level_list.pack(expand = 1, fill = Tkinter.BOTH, side = Tkinter.LEFT)
    self.level_list.bind("<ButtonRelease>", self.on_edit_level)
    
    self.scroll_bar = Tkinter.Scrollbar(self)
    self.scroll_bar.pack(side = Tkinter.RIGHT, fill = Tkinter.BOTH)
    self.level_list['yscrollcommand'] = self.scroll_bar.set
    self.scroll_bar['command'] = self.level_list.yview
    
  def on_edit_level(self, event = None):
    level_name = self.level_list.get(self.level_list.curselection()[0])
    soya.editor.edit(Level.get(level_name))
    
  def on_new_level(self, event = None):
    level = Level()
    level.filename = ""
    level.random_terrain()
    soya.editor.edit(level)
    
  

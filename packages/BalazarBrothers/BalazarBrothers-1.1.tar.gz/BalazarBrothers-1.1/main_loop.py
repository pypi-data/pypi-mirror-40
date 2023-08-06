# -*- coding: latin-1 -*-
# Balazar Brothers
# Copyright (C) 2003-2007 Jean-Baptiste LAMY
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

import os, os.path, time, random
import cerealizer, soya.tofu as tofu, soya, soya.sdlconst as sdlconst, soya._soya, soya.widget as widget, soya.opengl as opengl
import balazar_brothers, balazar_brothers.globdef as globdef, balazar_brothers.controller as controller
from balazar_brothers.camera     import Traveling
from balazar_brothers.weather    import WeatherAtmosphere
from balazar_brothers.discussion import Bubble


def init():
  if not soya.inited:
    soya.init(title = "Balazar Brothers", width = globdef.SCREEN_WIDTH, height = globdef.SCREEN_HEIGHT, fullscreen = globdef.FULLSCREEN, sound = 1, sound_reference_distance = 3.0, sound_doppler_factor = 0)
    soya.set_quality(globdef.QUALITY)
    soya.set_sound_volume(globdef.SOUND_VOLUME)
    
    SHADER_DEFAULT_MATERIAL = soya.Material.get("shader")
    SHADER_DEFAULT_MATERIAL.filename = "__SHADER_DEFAULT_MATERIAL__"
    soya._soya._set_shader_default_material(SHADER_DEFAULT_MATERIAL)
    
    widget.big_font     = widget.default_font
    widget.default_font = widget.default_font #soya.Font(os.path.join(soya.DATADIR, "FreeSans.ttf"), 40, 48)
    
  soya.render()
  soya.root_widget = None
  

class MainLoop(tofu.MainLoop):
  def __init__(self, scene = None):
    self.music              = None
    self.min_frame_duration = globdef.MIN_FRAME_DURATION
    
    tofu.MainLoop.__init__(self, scene)
    
  def init_interface(self):
    self.camera = soya.MAIN_LOOP.scenes[0].camera = soya.TravelingCamera(soya.MAIN_LOOP.scenes[0])
    self.camera.back = 100.0
    self.camera.speed = 0.03
    self.traveling = Traveling()
    self.camera.add_traveling(self.traveling)
    
    self.root_widget = widget.Group()
    self.root_widget.add(self.camera)
    soya.set_root_widget(self.root_widget)
    if globdef.FPS_LABEL: soya.widget.FPSLabel(self.root_widget)
    
    self.level_label = widget.Label(self.root_widget, _("(loading...)"), font = FUN_FONT)
    self.level_label.width = 10000
    self.level_label.top = -10
    self.score_label = ImageLabel  (self.root_widget, None, "score", soya.Material.get("coffre2D"), 0)
    self.keys_label  = ImageLabel  (self.root_widget, None, "keys" , soya.Material.get("clef2D"  ), 1)
    
    self.left_bubble   = Bubble(self.root_widget, -1, "test -1", (1.0, 0.0, 0.0, 1.0))
    self.middle_bubble = Bubble(self.root_widget,  0, "test  0", (0.0, 0.0, 0.0, 1.0))
    self.right_bubble  = Bubble(self.root_widget,  1, "", (0.0, 0.0, 1.0, 1.0))
    self.entry         = None
    
    scene = self.scenes[0]
    scene.atmosphere = WeatherAtmosphere(scene)
    self.listener = controller.EventListener(scene)
    
  def advance_time(self, proportion):
    tofu.MainLoop.advance_time(self, proportion)
    
    if self.scenes[0].atmosphere: self.scenes[0].atmosphere.advance_time(proportion)

BIG_FONT          = soya.Font(os.path.join(soya.DATADIR, "FreeSans.ttf"), 50, 60)
#INDIGO_JOKER_FONT = soya.Font.get("indigo.ttf@30x30")
FUN_FONT = soya.Font.get("PenguinAttack.ttf@40x40")
import balazar_brothers.platform_
balazar_brothers.platform_.Label3D._font = FUN_FONT # Hack !
  

class ImageLabel(widget.Label):
  def __init__(self, master = None, character = None, attr = "", material = None, pos = 0):
    self.character = character
    self.attr      = attr
    self.material  = material
    self.pos       = pos
    
    widget.Label.__init__(self, master, font = FUN_FONT, align = 0)
    
    self.old      = getattr(character, attr, 0)
    self.text     = unicode(self.old)
    
  def set_text(self, text):
    widget.Label.set_text(self, text)
    
    self.resize(self.master.left, self.master.top, self.master.width, self.master.height)
  text = property(widget.Label.get_text, set_text)
  
  def build_display_list(self):
    widget.Label.build_display_list(self)
    
    self.material.activate()
    opengl.glEnable(opengl.GL_BLEND)
    
    opengl.glBegin(opengl.GL_QUADS)
    opengl.glTexCoord2f(0.0, 0.0); opengl.glVertex2f(self.left + self.width - 50, self.top     )
    opengl.glTexCoord2f(0.0, 1.0); opengl.glVertex2f(self.left + self.width - 50, self.top + 50)
    opengl.glTexCoord2f(1.0, 1.0); opengl.glVertex2f(self.left + self.width     , self.top + 50)
    opengl.glTexCoord2f(1.0, 0.0); opengl.glVertex2f(self.left + self.width     , self.top     )
    opengl.glEnd()
    
    soya.DEFAULT_MATERIAL.activate()
    opengl.glDisable(opengl.GL_BLEND)
    
  def widget_begin_round(self):
    dif = getattr(self.character, self.attr, 0) - self.old
    if   dif > 0:
      self.old += 1
      self.text = unicode(self.old)
      
    elif dif < 0:
      self.old -= 1
      self.text = unicode(self.old)
      
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    w, h = self.font.get_print_size(self._text)
    
    self.left   = parent_left + parent_width  - 10 - 50 - w
    self.top    = 5 + 52 * self.pos
    self.width  = 50 + 5 + w
    self.height = 50
    self._changed = -2


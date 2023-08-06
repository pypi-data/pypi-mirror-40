# BalazarBrothers
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

import weakref, time

import soya

import balazar_brothers
import balazar_brothers.main_loop
from balazar_brothers.bonus    import *
from balazar_brothers.platform import *
from balazar_brothers.trap     import *
from balazar_brothers.level    import Level

import editobj, editobj.main, editobj.editor as editor, editobj.custom as custom
import Tkinter, dircache, os, os.path

editobj.EVAL_ENV.update({
  "balazar_brothers" : balazar_brothers,
  "bonus"            : balazar_brothers.bonus,
  "platform"         : balazar_brothers.platform,
  "trap"             : balazar_brothers.trap,
  })

custom.register_attr("round"               , None, Level)
custom.register_attr("active"              , None, Level)
custom.register_attr("active"              , None, Level)

custom.register_attr("terrain"                , None, Level)
custom.register_attr("static_part"         , None, Level)
custom.register_attr("center"              , None, Level)
custom.register_attr("atmosphere"          , None, Level)
custom.register_attr("mobiles"             , None, Level)
custom.register_attr("parent"              , None, Level)
custom.register_attr("scale_x"             , None, Level)
custom.register_attr("scale_y"             , None, Level)
custom.register_attr("scale_z"             , None, Level)
custom.register_attr("model"               , None, Level)
custom.register_attr("model_builder"       , None, Level)
custom.register_attr("solid"               , None, Level)
custom.register_attr("uid"                 , None, Level)
custom.register_attr("visible"             , None, Level)
custom.register_attr("x"                   , None, Level)
custom.register_attr("y"                   , None, Level)
custom.register_attr("z"                   , None, Level)

custom.register_attr("atmosphere"          , None)
custom.register_attr("bot"                 , None)
custom.register_attr("characters_on"       , None)
custom.register_attr("controller"          , None)
custom.register_attr("doer"                , None)
custom.register_attr("interpolate_factor"  , None)
custom.register_attr("label"               , None, PortailPlatform)
custom.register_attr("level"               , None)
custom.register_attr("parent"              , None)
custom.register_attr("platform_position"   , None)
custom.register_attr("player_name"         , None)
custom.register_attr("round"               , None)
custom.register_attr("model_builder"       , None)
custom.register_attr("solid"               , None)
custom.register_attr("state1"              , None)
custom.register_attr("state2"              , None)
custom.register_attr("uid"                 , None)
custom.register_attr("sprite"              , None)
custom.register_attr("animation"           , None, Bonus)
custom.register_attr("attached_coordsysts" , None)
custom.register_attr("attached_meshes"     , None)
custom.register_attr("auto_static"         , None)
custom.register_attr("deforms"             , None)
custom.register_attr("static"              , None)

# ODE stuff
custom.register_attr("angular_velocity"               , None)
custom.register_attr("auto_disable"                   , None)
custom.register_attr("auto_disable_angular_threshold" , None)
custom.register_attr("auto_disable_linear_threshold"  , None)
custom.register_attr("auto_disable_steps"             , None)
custom.register_attr("auto_disable_time"              , None)
custom.register_attr("cfm"                            , None)
custom.register_attr("contact_max_correcting_velocity", None)
custom.register_attr("contact_surface_layer"          , None)
custom.register_attr("enabled"                        , None)
custom.register_attr("erp"                            , None)
custom.register_attr("finite_rotation_axis"           , None)
custom.register_attr("finite_rotation_mode"           , None)
custom.register_attr("force"                          , None)
custom.register_attr("geom"                           , None)
custom.register_attr("gravity"                        , None)
custom.register_attr("gravity_mode"                   , None)
custom.register_attr("has_space"                      , None)
custom.register_attr("linear_velocity"                , None)
custom.register_attr("mass"                           , None)
custom.register_attr("num_joints"                     , None)
custom.register_attr("ode"                            , None)
custom.register_attr("odeWorld"                       , None)
custom.register_attr("ode_parent"                     , None)
custom.register_attr("pushable"                       , None)
custom.register_attr("quickstep_num_iterations"       , None)
custom.register_attr("space"                          , None)
custom.register_attr("state_counter"                  , None)
custom.register_attr("torque"                         , None)

custom.register_attr("water"               , editor.BoolEditor, Fountain)


custom.register_available_children([
  "platform.PortailPlatform()",
  "platform.Coqueliform()",
  "platform.RotatingCoqueliform()",
  "platform.FallingCoqueliform()",
  "platform.Fountain()",
  "platform.RotatingFountain()",
  "platform.Mushroom()",
  "platform.RotatingMushroom()",
  "platform.Fasme()",
  "platform.RotatingFasme()",
  "platform.UpDownFasme()",
  "platform.Tower()",
  "platform.RotatingTower()",
  "platform.FallingTower()",
  "platform.StartingPlatform()",
  "platform.Door()",
  "bonus.SmallChest()",
  "bonus.BigChest()",
  "bonus.Key()",
  "trap.Fruit()",
  "trap.RotatingFruit()",
  "trap.Balancelle()",
  "trap.RotatingBalancelle()",
  "trap.Balazarette()",
  "trap.BalazarGris()",
  "platform.TreePompon()",
  "platform.Farm()",
  ], Level)

custom.register_children_attr("children"  , "add_or_add_mobile", "del_or_del_mobile", clazz = Level)

custom.register_method("rotate_incline"      , Level, None)
custom.register_method("rotate_lateral"      , Level, None)
custom.register_method("rotate_vertical"     , Level, None)
custom.register_method("random_terrain"      , Level)

def change_camera_mode(level):
  LEVEL_CUSTOM_EDITS[level].set_camera_mode(1 - LEVEL_CUSTOM_EDITS[level].camera_mode)
  
custom.register_method(change_camera_mode , Level)

# Disable soya editor
custom.register_on_edit(None, soya.World)

custom.register_attr("hour"                , editor.FloatEditor)
custom.register_attr("weather"             , editor.ListEditor(["sun", "rain", "snow"]))
custom.register_attr("next_level_name"     , editor.LambdaListEditor(lambda obj: Level.availables()))

custom.register_attr("animation"           , editor.ListEditor(["balance", "balance2", "balance3"]), Fruit)


CURRENT = None
def on_edit_level(level, window):
  if not LEVEL_CUSTOM_EDITS.has_key(level):
    ed = LevelCustomEdit(level, window)
    
    def on_activate(event = None):
      global CURRENT
      
      if CURRENT: CURRENT.set_active(0)
      ed.set_active(1)
      CURRENT = ed
      
    window.bind("<FocusIn>" , on_activate)

custom.register_on_edit(on_edit_level, Level)


LEVEL_CUSTOM_EDITS = weakref.WeakKeyDictionary()

class LevelCustomEdit(object):
  def __init__(self, level, window):
    self.active = 0
    self.level  = level
    self.window = window
    
    self.scene  = soya.World()
    self.scene.atmosphere = soya.Atmosphere()
    self.scene.atmosphere.ambient = (0.8, 0.8, 0.8, 1.0)
    self.scene.add(level)
    
    self.main_loop = soya.MainLoop(self.scene)
    
    self.camera = soya.Camera(self.scene)
    self.camera.back = 250.0
    
    self.camera_matrices = []
    
    self.camera.set_xyz(0.0, 50.0, 0.0)
    self.camera.look_at(soya.Vector(self.scene, 0.0, -1.0, 0.0))
    self.camera_matrices.append(self.camera.matrix)
    
    self.camera.set_identity()
    self.camera.set_xyz(0.0, 0.0, 50.0)
    self.camera_matrices.append(self.camera.matrix)
    
    self.camera_mode = 0
    self.camera.matrix = self.camera_matrices[0]
    self.camera.ortho = 1
    self.camera.fov = 1000.0
    
    self.selections  = set()
    self.button_down = 0
    self.mouse = soya.Point()
    self.impact = None
    self.last_click_time = 0
    
    LEVEL_CUSTOM_EDITS[level] = self
    
  def set_camera_mode(self, camera_mode):
    self.camera_matrices[self.camera_mode] = self.camera.matrix
    self.camera_mode = camera_mode
    self.camera.matrix = self.camera_matrices[self.camera_mode]
    if camera_mode == 0:
      self.camera.ortho = 1
      self.camera.fov = 1000.0
    else:
      self.camera.ortho = 0
      self.camera.fov = 60.0
      
  def set_active(self, active):
    if active != self.active:
      self.active = active
      if active:
        soya.set_root_widget(self.camera)
        self.update_soya()
      else:
        self.window.after_cancel(self.cancel)
        
  def update_soya(self):
    self.cancel = self.window.after(50, self.update_soya)
    
    if self.active:
      self.main_loop.update()
      for event in soya.coalesce_motion_event(soya.process_event()): self.on_event(event)
      
  def on_event(self, event):
    #print event
    if   event[0] == soya.sdlconst.MOUSEMOTION:
      if   self.button_down == 1: # Move
        new_mouse = self.camera.coord2d_to_3d(event[1], event[2], (self.impact and self.impact.z) or 0.0)
        v = self.mouse >> new_mouse
        for obj in self.selections: obj += v
        self.mouse = new_mouse
        
      elif self.button_down == 3: # Rotate
        new_mouse = self.camera.coord2d_to_3d(event[1], event[2], (self.impact and self.impact.z) or 0.0)
        v = self.mouse >> new_mouse
        for obj in self.selections:
          if not isinstance(obj, soya.Terrain):
            obj.look_at(self.camera.coord2d_to_3d(event[1], event[2], (obj % self.camera).z))
        self.mouse = new_mouse
        
    elif event[0] == soya.sdlconst.MOUSEBUTTONDOWN:
      if self.last_click_time + 0.2 > time.time():
        self.last_click_time = time.time()
        if self.selections: self.window.edit(list(self.selections)[0])
        else:               self.window.edit(self.level)
        return
      
      self.last_click_time = time.time()
      self.button_down = event[1]
      
      if   self.button_down == 2: # Repeat add
        if self.selections: to_clone = list(self.selections)[0]
        else:               to_clone = self.level.children[-1]
        obj = to_clone.__class__()
        self.level.add_or_add_mobile(obj)
        self.mouse = self.camera.coord2d_to_3d(event[2], event[3], (self.impact and self.impact.z) or 0.0)
        obj.move(self.mouse); obj.y = to_clone.y
        self.button_down = 1 # continue with the move tool
        
      if not(soya.get_mod() & soya.sdlconst.MOD_SHIFT): self.selections = set()
      
      self.mouse = self.camera.coord2d_to_3d(event[2], event[3])
      if self.camera.ortho: result = self.scene.raypick(self.mouse, soya.Vector(self.scene, 0.0, -1.0, 0.0))
      else:                 result = self.scene.raypick(self.camera, self.camera.vector_to(self.mouse))
      
      #print self.mouse % self.scene
      
      if result:
        self.impact, normal = result
        selection = self.impact
        while not selection.parent is self.level: selection = selection.parent
        self.selections.add(selection)
        self.impact.convert_to(self.camera)
        self.mouse = self.camera.coord2d_to_3d(event[2], event[3], self.impact.z)
      #print self.selections

    elif event[0] == soya.sdlconst.MOUSEBUTTONUP:
      self.button_down = 0
      
    elif event[0] == soya.sdlconst.KEYDOWN:
      # Left, right, up, down, +, -
      if   event[1] == 276: self.camera += soya.Vector(self.camera, -10.0 +  9.0 * (soya.get_mod() & soya.sdlconst.MOD_SHIFT),  0.0, 0.0)
      elif event[1] == 275: self.camera += soya.Vector(self.camera,  10.0 -  9.0 * (soya.get_mod() & soya.sdlconst.MOD_SHIFT),  0.0, 0.0)
      elif event[1] == 273: self.camera += soya.Vector(self.camera,   0.0,  10.0 - 9.0 * (soya.get_mod() & soya.sdlconst.MOD_SHIFT), 0.0)
      elif event[1] == 274: self.camera += soya.Vector(self.camera,   0.0, -10.0 + 9.0 * (soya.get_mod() & soya.sdlconst.MOD_SHIFT), 0.0)
      elif event[1] == 270: self.camera += soya.Vector(self.camera,   0.0,   0.0, -10.0 + 9.0 * (soya.get_mod() & soya.sdlconst.MOD_SHIFT))
      elif event[1] == 269: self.camera += soya.Vector(self.camera,   0.0,   0.0,  10.0 - 9.0 * (soya.get_mod() & soya.sdlconst.MOD_SHIFT))
      

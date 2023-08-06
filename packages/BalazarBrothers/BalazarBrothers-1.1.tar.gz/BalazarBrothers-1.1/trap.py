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

import random

import cerealizer, soya, soya.tofu as tofu

import balazar_brothers, balazar_brothers.globdef as globdef, balazar_brothers.platform_ as platform

MESSAGE_OPEN   = "O"
MESSAGE_CLOSE  = "C"
MESSAGE_PUSHED = "P"

DURATIONS = {
  "balance"  : 35,
  "balance2" : 50,
  }
class Fruit(tofu.Mobile):
  animating = 0
  radius    = 1.5
  
  def __init__(self):
    tofu.Mobile.__init__(self)
    
    self.body = soya.Body(self, soya.AnimatedModel.get("fruit"))
    #self.body.animate_blend_cycle("balance")
    self.kill_point_world = soya.World(self)
    self.kill_point       = soya.Point(self.kill_point_world, 0.0, 1.0, 0.0)
    self.body.attach_to_bone(self.kill_point_world, "fruit2")
    
    self.animation = "balance"
    #self.body.animate_blend_cycle("balance")
    #self.body.begin_round()
    #self.body.advance_time(0.1)
    
  def __getstate__(self):
    state = super(Fruit, self).__getstate__()
    if self.animating:
      del state[1]["animating"]
    return state
  
  def do_physics(self):
    if self.level.round % DURATIONS[self.animation] == 0:
      self.body.animate_clear_cycle(self.animation)
      self.body.animate_reset()
      self.body.animate_blend_cycle(self.animation)
      
    elif not self.animating:
      self.animating = 1
      self.body.animate_blend_cycle(self.animation)
      self.body.advance_time(self.level.round % 50)
      
  def do_collisions(self):
    for character in self.level.mobiles:
      if isinstance(character, balazar_brothers.character.Character):
        if self.kill_point.distance_to(character.center) < self.radius:
          if (character.dying == 0) or (character.dying > 10):
            #character.doer.action_done(balazar_brothers.character.SoundState(character, "coup.wav", 12.0))
            character.send_message("!coup.wav 12")
          if self.animation == "balance2":
            if character.platform and isinstance(character.platform, balazar_brothers.character.Character): continue
            #character.die(soya.Vector(self, 1.1, 4.0, -0.0))
            character.die(soya.Vector(self, 0.2, 0.8, -0.0))
          else:
            #character.die(soya.Vector(self, 0.0, 1.0, -2.0))
            character.die(soya.Vector(self, 0.0, 0.2, -0.4))
cerealizer.register(Fruit)


class RotatingFruit(Fruit):
  def advance_time(self, proportion):
    Fruit.advance_time(self, proportion)
    self.rotate_lateral(5.0 * proportion)
cerealizer.register(RotatingFruit)


class Balancelle(platform.BasePlatform):
  radius = 1.5
  def __init__(self):
    super(Balancelle, self).__init__()
    
    self.model  = soya.Model.get("balancelle")
    self.speed  =  3.0
    self.sens   = -1.0
    self.platform_position = soya.Point(self, 0.0, -5.0, 0.0)
    self.kill_point        = soya.Point(self, 0.0, -6.0, 0.0)
    #self.orientate_character = 1

#  def __setstate__(self, state):
#    super(Balancelle, self).__setstate__(state)
#    self.kill_point = soya.Point(self, 0.0, -6.0, 0.0)
#    self.speed  =  3.0
#    self.sens   = -1.0
    
  def advance_time(self, proportion):
    super(Balancelle, self).advance_time(proportion)
    
    self.turn_x(self.speed)
    
    self.speed += self.sens * 0.2 * proportion
    if abs(self.speed) > 3.0:
      self.sens = -1.0 * self.sens
      if self.speed > 3.0: self.speed =  3.0 - (self.speed - 3.0)
      else:                self.speed = -3.0 - (self.speed + 3.0)
      
    for character in self.characters_on:
      if not self.orientate_character:
        character.next_state.look_at_y(soya.Vector(self.level, 0.0, 1.0, 0.0))
        
  def do_collisions(self):
    for character in self.level.mobiles:
      if isinstance(character, balazar_brothers.character.Character):
        if self.kill_point.distance_to(character.center) < self.radius:
          if character.platform and isinstance(character.platform, balazar_brothers.character.Character): continue
          if (character.dying == 0) or (character.dying > 10): character.send_message("!coup.wav 12")
          if self.speed > 0.0: character.die(soya.Vector(self, 0.0, 0.2, -0.4))
          else:                character.die(soya.Vector(self, 0.0, 0.2,  0.4))
cerealizer.register(Balancelle)
      
      

class RotatingBalancelle(platform.BasePlatform):
  radius = 1.5
  def __init__(self):
    super(RotatingBalancelle, self).__init__()
    
    self.model  = soya.Model.get("balancelle2")
    self.sens   = 1.0
    self.platform_position = soya.Point(self, 3.2, -3.8, 0.0)
    self.kill_point        = soya.Point(self, 3.8, -4.6, 0.0)
    
  def advance_time(self, proportion):
    super(RotatingBalancelle, self).advance_time(proportion)
    
    self.rotate_y(self.sens * 6.0 * proportion)
    
    for character in self.characters_on:
      if not self.orientate_character:
        character.next_state.look_at_y(soya.Vector(self.level, 0.0, 1.0, 0.0))
        
  def do_collisions(self):
    for character in self.level.mobiles:
      if isinstance(character, balazar_brothers.character.Character):
        if self.kill_point.distance_to(character.center) < self.radius:
          if character.platform and isinstance(character.platform, balazar_brothers.character.Character): continue
          if (character.dying == 0) or (character.dying > 10): character.send_message("!coup.wav 12")
          if self.speed > 0.0: character.die(soya.Vector(self, 0.0, 0.2, -0.4))
          else:                character.die(soya.Vector(self, 0.0, 0.2,  0.4))
cerealizer.register(RotatingBalancelle)
      

class BigGrid(tofu.Mobile):
  def __init__(self):
    super(BigGrid, self).__init__()
    
    self.model  = soya.Model.get("mur_passage")
    self.harrow = soya.Body(self, soya.Shape.get("herse2@grille1"))
    self.harrow.y = -2.0
    self.opened = 0
    self.next_platforms = []
    
  @tofu.side("single", "server")
  def open(self):
    self.send_message(MESSAGE_OPEN)
    
  def do_message(self, message):
    if   message == MESSAGE_OPEN : self.opened = 1
    elif message == MESSAGE_CLOSE:
      self.opened = 0
      for platform in self.next_platforms:
        for character in platform.characters_on: character.die()
        platform.platform_position = soya.Point(platform, 0.0, 10000.0, 0.0)
        
  def advance_time(self, proportion):
    super(BigGrid, self).advance_time(proportion)
    if self.opened:
      if self.harrow.y < 15.0: self.harrow.y = min(self.harrow.y + proportion * 0.10, 15.0)
      else:
        for platform in self.next_platforms: platform.platform_position = platform
        
    elif self.harrow.y > -2.0:
      self.harrow.y = max(self.harrow.y - proportion * 0.15, -2.0)
      
cerealizer.register(BigGrid)
    
class Balazarette(tofu.Mobile):
  def __init__(self):
    super(Balazarette, self).__init__()
    self.model = soya.AnimatedModel.get("balazarette")
    self.animated = 0
    
  def __setstate__(self, state):
    super(Balazarette, self).__setstate__(state)
    self.animated = 0
    
  def begin_round(self):
    super(Balazarette, self).begin_round()
    if self.animated == 0:
      self.animated = 1
      if self.model is soya.AnimatedModel.get("balazarette"):
        self.animate_blend_cycle("danse")
      else:
        self.animate_blend_cycle("danse2")
cerealizer.register(Balazarette)

class BalazarGris(tofu.Mobile):
  def __init__(self):
    super(BalazarGris, self).__init__()
    self.model = soya.AnimatedModel.get("balazar@gris")
    self.animated = 0
    self.current_discussion = ""
  def __setstate__(self, state):
    super(BalazarGris, self).__setstate__(state)
    self.animated = 0
    self.current_discussion = ""
    
  def begin_round(self):
    super(BalazarGris, self).begin_round()
    if self.animated == 0:
      self.animated = 1
      self.animate_blend_cycle("sort1")
cerealizer.register(BalazarGris)

# class Grid(platform.BasePlatform):
#   def __init__(self):
#     super(Grid, self).__init__()
    
#     self.model  = soya.Model.get("tour_plate")
#     self.grid   = soya.Body(self)
#     self.harrow = soya.Body(self)
#     self.set_type(1)
#     self.opened = 0
    
#   def set_type(self, type):
#     self.type = type
#     self.grid.model   = soya.Model.get("grille@grille%s" % type)
#     self.harrow.model = soya.Model.get("herse@grille%s"  % type)
    
#   def do_message(self, message):
#     if   message == MESSAGE_OPEN : self.opened = 1
#     elif message == MESSAGE_CLOSE: self.opened = 0
    
#   def advance_time(self, proportion):
#     super(Grid, self).advance_time(proportion)
#     if        self.opened  and self.harrow.y < 2.3: self.harrow.y = max(self.harrow.y + proportion * 0.05, 2.3)
#     elif (not self.opened) and self.harrow.y > 0.0: self.harrow.y = min(self.harrow.y - proportion * 0.05, 0.0)
# cerealizer.register(Grid)


# class TrappedTile(platform.BasePlatform):
#   def __init__(self):
#     super(TrappedTile, self).__init__()
    
#     self.platform_position = soya.Point(self.tile, 0.0, 0.4, 0.0)
#     self.model = soya.Model.get("tour_plate")
#     self.tile = soya.World(self)
#     self.set_type(1)
    
#   def set_type(self, type):
#     self.type = type
#     self.tile.model = soya.Model.get("dalle@grille%s" % type)
    
#   def advance_time(self, proportion):
#     super(TrappedTile, self).advance_time(proportion)
#     if not self.characters_on:
#       if self.tile.y <  0.0 : self.tile.y = min( 0.0 , self.tile.y + proportion * 0.01)
#     elif self.tile.y > -0.38:
#       self.tile.y = max(-0.38, self.tile.y - proportion * 0.01)
#       if self.tile.y == -0.38:
#         self.pushed()

#   @tofu.side("single", "server")
#   def pushed(self):
#     self.send_message(MESSAGE_PUSHED)
    
#   def do_message(self, message):
#     if message == MESSAGE_PUSHED:
#       for grid in self.level:
#         if isinstance(grid, Grid) and grid.type == self.type:
#           grid.send_message(MESSAGE_OPEN)
# cerealizer.register(TrappedTile)
    



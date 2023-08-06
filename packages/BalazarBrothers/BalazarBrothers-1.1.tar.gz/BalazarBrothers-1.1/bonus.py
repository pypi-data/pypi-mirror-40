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

import cerealizer, soya, soya.tofu as tofu

import balazar_brothers, balazar_brothers.globdef as globdef
from balazar_brothers.character import Balazar
from balazar_brothers.player import Player


class Bonus(tofu.Mobile):
  TAKEN_SOUND = "ouais.wav"
  
  def __init__(self):
    tofu.Mobile.__init__(self)
    
    self.radius    = 1.0
    self.animation = 0
    
  def suitable_for(self, character): return isinstance(character, Balazar)
  
  def get_network_state(self):
    if self.visible and not self.animation: return "1"
    else:                                   return "0"
    
  def read_network_state(self, f):
    if f.read(1) == "1": self.resurrected()
    else:                self.taken()

  def do_collisions(self):
    tofu.Mobile.do_collisions(self)
    
    if self.visible and not self.animation:
      for character in self.level.mobiles:
        if self.suitable_for(character) and self.distance_to(character.center) < self.radius:
          self.taken_by(character)
          self.set_current_state_importance(2)
          break
        
  def set_state(self, state):
    if   isinstance(state, BonusTakenState):
      self.taken_by(state.character)
      
    elif isinstance(state, BonusResurrectedState):
      self.resurrected()
      
  def taken_by(self, character): self.taken()
  
  def taken(self):
    self.animation = 1
    soya.SoundPlayer(self, soya.Sound.get(self.TAKEN_SOUND), gain = 10.0)
    
  def resurrected(self):
    self.set_scale_factors(1.0, 1.0, 1.0)
    self.visible   = 1
    self.animation = 0
    
  def advance_time(self, proportion):
    if self.visible:
      if self.animation:
        self.rotate_lateral((0.2 * self.animation + 4.0) * proportion)
        
        self.animation += 1
        
        if   self.animation <  50.0: self.y += 0.15 * proportion
        elif self.animation <  80.0: pass
        elif self.animation < 100.0: self.scale(0.9, 0.9, 0.9)
        else:
          self.visible   = 0
          self.animation = 0
          
      else:
        self.rotate_lateral(4.0 * proportion)


class SmallChest(Bonus):
  def __init__(self):
    Bonus.__init__(self)
    
    self.model = soya.Model.get("coffre1@typ1")
    self.lid   = soya.Body(self, soya.Model.get("coffre_couvercle1@typ1"))
    self.lid.set_xyz(0.0, 2.0, 1.0)
    self.scale(0.5, 0.5, 0.5)
    
    self.sprite = soya.Sprite(self, soya.Material.get("x_lumiere_1"))
    self.sprite.y = 1.5
    self.sprite.width = self.sprite.height = 2.0
    self.sprite.lit = 0
    
  def taken_by(self, character):
    Bonus.taken_by(self, character)
    Player.get(character.player_name).add_bonus(score = 1)
    
  def resurrected(self):
    Bonus.resurrected(self)
    self.set_scale_factors(0.5, 0.5, 0.5)
    self.lid.set_identity(); self.lid.set_xyz(0.0, 2.0, 1.0)
    
  def advance_time(self, proportion):
    Bonus.advance_time(self, proportion)
    if self.visible and self.animation: self.lid.rotate_vertical(3.0 * proportion)
cerealizer.register(SmallChest)
      

class BigChest(Bonus):
  def __init__(self):
    Bonus.__init__(self)
    
    self.model = soya.Model.get("coffre1@typ2")
    self.lid   = soya.Body(self, soya.Model.get("coffre_couvercle1@typ2"))
    self.lid.set_xyz(0.0, 2.0, 1.0)
    
    self.sprite = soya.Sprite(self, soya.Material.get("x_lumiere_1"))
    self.sprite.y = 1.5
    self.sprite.width = self.sprite.height = 6.0
    self.sprite.lit = 0
    
  def taken_by(self, character):
    Bonus.taken_by(self, character)
    Player.get(character.player_name).add_bonus(score = 5)
    
  def resurrected(self):
    Bonus.resurrected(self)
    self.lid.set_identity(); self.lid.set_xyz(0.0, 2.0, 1.0)
    
  def advance_time(self, proportion):
    Bonus.advance_time(self, proportion)
    if self.visible and self.animation: self.lid.rotate_vertical(3.0 * proportion)
cerealizer.register(BigChest)
      
      
class Key(Bonus):
  def __init__(self):
    Bonus.__init__(self)
    
    self.model = soya.Model.get("clef")
    
    self.sprite = soya.Sprite(self, soya.Material.get("x_lumiere_1"))
    self.sprite.y = 1.5
    self.sprite.width = self.sprite.height = 6.0
    self.sprite.lit = 0
    
  def taken_by(self, character):
    Bonus.taken_by(self, character)
    Player.get(character.player_name).add_bonus(keys = 1)
cerealizer.register(Key)
    

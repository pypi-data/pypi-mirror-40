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

import math
import soya, soya.tofu as tofu

from balazar_brothers.platform_ import BumpablePlatform


class Traveling(soya.Traveling):
  def __init__(self, characters = None):
    soya.Traveling.__init__(self)
    
    self.characters = characters or []
    
    self.incline_as      = None
    self.smooth_move     = 1
    self.smooth_rotation = 0
    
    self.position  = soya.Point()
    self.direction = soya.Point()
    
    self.step  = soya.Vector()
    self.v     = soya.Vector()
    self.p     = soya.Point()
    
    self.custom_distance = 0.0
    self.custom_angle    = 0.0
    
    self.last_step = None
    
  def add_character(self, character, index = -1): self.characters.insert(index, character)
  
  def best_position(self, camera):
    v    = self.v
    p    = self.p
    step = self.step
    
    for character in self.characters:
      if character.level:
        level = character.level
        break
    else: return self.position # All characters are dead      
    
    self.direction.parent = camera.parent
    self.direction.set_xyz(0.0, 0.0, 0.0)
    nb = 0
    for character in self.characters:
      if not character.platform:
        if not character.next_platform:
          nb += 1
          #p.clone(character.jump_start_position)
          p.clone(character)
          p.convert_to(self.direction.parent)
          self.direction.add_xyz(p.x, p.y, p.z)
        else:
          nb += 1
          v.set_start_end(character.jump_start_position, character.next_platform.platform_position)
          p.clone(character.jump_start_position)
          p.add_mul_vector(character.jump_proportion, v)
          p.convert_to(self.direction.parent)
          self.direction.add_xyz(p.x, p.y, p.z)
      elif not character.platform in self.characters:
        nb += 1
        p.clone(character)
        p.convert_to(self.direction.parent)
        self.direction.add_xyz(p.x, p.y, p.z)
        if isinstance(character.platform, BumpablePlatform): self.direction.y -= character.platform.bumped_y

    if nb == 0: return self.position # All characters are dead
    
    self.direction.x /= nb
    self.direction.y /= nb
    self.direction.z /= nb
    self.direction.y += 2.0
    
    self.position.clone(self.direction)
    
    v.set_start_end(self.characters[-1], self.characters[0])
    v.convert_to(camera.parent)
    if v.length() < abs(v.y) + 0.01:
      #step.set_start_end(level.center, self.characters[0])
      if not self.last_step:
        self.last_step = level.center >> camera
        self.last_step.convert_to(camera.parent)
        #step.set_start_end(level.center, camera)
      step.clone(self.last_step)
      step.convert_to(camera.parent)
      
    else:
      self.last_step = None
      soya.Vector(None, 0.0, 1.0, 0.0).cross_product(v, step)
      step.convert_to(camera.parent)
      
    step.set_length(2.0)
    step.y = 0.4
    
    if self.custom_angle:
      x = step.x
      z = step.z
      cos = math.cos(self.custom_angle)
      sin = math.sin(self.custom_angle)
      step.x = cos * x + sin * z
      step.z = -sin * x + cos * z
    
    min_dist = 15.0
    
    for i in range(50):
      for character in self.characters:
        v.set_start_end(character, self.position)
        if v.length() < min_dist: break
        if v.angle_to(step) > 25.0: break
      else: break
      self.position.add_vector(step)

    if self.custom_distance:
      self.position.add_mul_vector(self.custom_distance, step)
      
    return self.position
  
  def best_direction(self, camera):
    return self.direction
  

    

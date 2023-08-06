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
import soya.label3d

import balazar_brothers, balazar_brothers.globdef as globdef


class Platform(object):
  JUMP_SOUND = "jump1.wav"
  FALL_SOUND = "chute.wav"
  discussion = None
  orientate_character = 0
  
  def __init__(self):
    super(Platform, self).__init__()
    self.characters_on = []
    
  def characters_on_recursive(self):
    for character in self.characters_on:
      yield character
      for character2 in character.characters_on_recursive(): yield character2
      
  def suitable_for(self, character):
    if self.characters_on and not character.want_to_kill(self.characters_on[0]): return 0
    return 1
  
  def add_character(self, character, change_level = 0, multi = 0):
    if self.characters_on and (not multi):
      if character.can_kill(self.characters_on[0]): self.characters_on[0].die(soya.Vector(character, 0.0, 0.0, -1.0))
      else: character.die(soya.Vector(character, 0.0, 0.0, 1.0)); return
      
    self.characters_on.append(character)
    if isinstance(self.platform_position, soya.World):
      self.platform_position.add(character)
      character.next_state.convert_to(self.platform_position)
      #if self.orientate_character: character.next_state.look_at_y(soya.Vector(self.platform_position, 0.0, 1.0, 0.0))
      #else:                        character.next_state.look_at_y(soya.Vector(self.level, 0.0, 1.0, 0.0))
    else:
      self.platform_position.parent.add(character)
      character.next_state.convert_to(self.platform_position.parent)
      #if self.orientate_character: character.next_state.look_at_y(soya.Vector(self.platform_position.parent, 0.0, 1.0, 0.0))
      #else:                        character.next_state.look_at_y(soya.Vector(self.level, 0.0, 1.0, 0.0))
      
    #character.next_state.convert_to(self)
    character.next_state.move(self.platform_position)
    character.speed.set_identity()
    if self.discussion and not character.bot: character.start_discussion(self.discussion)
    
  def remove_character(self, character):
    if character in self.characters_on: self.characters_on.remove(character)
    if self.level: self.level.add(character)
    
  def radius(self, direction = None): return 0.0
  
  def set_next_for_character(self, character): pass
  

class MultiCharactersPlatform(Platform):
  def __init__(self): super(MultiCharactersPlatform, self).__init__()
    
  def suitable_for(self, character): return 1
  
  def add_character(self, character, change_level = 0):
    Platform.add_character(self, character, change_level, 1)
    
class BumpablePlatform(Platform):
  BUMP_SPEED   =  0.1
  UNBUMP_SPEED =  0.05
  MAX_BUMP     = -0.5
  def __init__(self):
    super(BumpablePlatform, self).__init__()
    
    self.bumped_y = 0.0
    
  def advance_time(self, proportion):
    super(BumpablePlatform, self).advance_time(proportion)
    if not self.characters_on:
      if self.bumped_y < 0.0:
        dy = self.UNBUMP_SPEED * proportion
        self.bumped_y += dy
        self.y        += dy
    elif self.bumped_y > self.MAX_BUMP:
      dy = self.BUMP_SPEED * proportion
      self.bumped_y -= dy
      self.y        -= dy

      
class BasePlatform(Platform, tofu.Mobile):
  def __init__(self):
    super(BasePlatform, self).__init__()
    
    self.platform_position = self
    self.platid            = 0
    
  def __setstate__(self, state):
    super(BasePlatform, self).__setstate__(state)
    

    

class Coqueliform(BumpablePlatform, BasePlatform):
  def __init__(self):
    super(Coqueliform, self).__init__()
    self.model = soya.Model.get("coqueliforme")
cerealizer.register(Coqueliform, classname = "balazar_brothers.platform.Coqueliform")
    
    
class FallingCoqueliform(BumpablePlatform, BasePlatform):
  BUMP_SPEED   =  0.1
  UNBUMP_SPEED =  0.03
  MAX_BUMP     = -10.0
  
  def __init__(self):
    super(FallingCoqueliform, self).__init__()
    self.model = soya.Model.get("coqueliforme@bordeau")
cerealizer.register(FallingCoqueliform, classname = "balazar_brothers.platform.FallingCoqueliform")
    

class RotatingCoqueliform(Coqueliform):
  def __init__(self):
    super(RotatingCoqueliform, self).__init__()
    self.model = soya.Model.get("coqueliforme@bleu")
    
  def advance_time(self, proportion):
    super(RotatingCoqueliform, self).advance_time(proportion)
    self.rotate_lateral(4.0 * proportion)
cerealizer.register(RotatingCoqueliform, classname = "balazar_brothers.platform.RotatingCoqueliform")


class Mushroom(BumpablePlatform, BasePlatform):
  def __init__(self):
    super(Mushroom, self).__init__()
    self.model = soya.Model.get("champignon@pos1")
cerealizer.register(Mushroom, classname = "balazar_brothers.platform.Mushroom")

class RotatingMushroom(Mushroom):
  def __init__(self):
    super(RotatingMushroom, self).__init__()
    self.model = soya.Model.get("champignon@bleupos1")
    
  def advance_time(self, proportion):
    super(RotatingMushroom, self).advance_time(proportion)
    self.rotate_lateral(3.0 * proportion)
cerealizer.register(RotatingMushroom, classname = "balazar_brothers.platform.RotatingMushroom")
    

class Fasme(BumpablePlatform, BasePlatform):
  def __init__(self):
    super(Fasme, self).__init__()
    self.model = soya.Model.get("fasme@pos1")
cerealizer.register(Fasme, classname = "balazar_brothers.platform.Fasme")

class RotatingFasme(Fasme):
  def __init__(self):
    super(RotatingFasme, self).__init__()
    self.model = soya.Model.get("fasme@bleupos1")
    
  def advance_time(self, proportion):
    super(RotatingFasme, self).advance_time(proportion)
    self.rotate_lateral(3.0 * proportion)
cerealizer.register(RotatingFasme, classname = "balazar_brothers.platform.RotatingFasme")

class UpDownFasme(Fasme):
  def __init__(self):
    super(Fasme, self).__init__()
    self.model  = None
    self.body = soya.Body(self, soya.AnimatedModel.get("fasme"))
    self.attached_world = soya.World(self)
    self.platform_position = soya.Point(self.attached_world, 0.0, 0.3, 0.0)
    self.body.attach_to_bone(self.attached_world, "Bone_005")
    self.pos = 0
    
    self.body.animate_blend_cycle("haut")
    self.body.begin_round()
    self.body.advance_time(0.1)
    
  def __setstate__(self, state):
    super(Fasme, self).__setstate__(state)
    if hasattr(self, "volume"):
      self.body = self.volume
      
  def begin_round(self):
    Fasme.begin_round(self)
    if self.pos == 30: self.pos = 35
    if   (self.level.round + self.pos) % 70 == 0:
      self.body.animate_clear_cycle("bas", 0.4)
      self.body.animate_blend_cycle("haut")
    elif (self.level.round + self.pos) % 70 == 35:
      self.body.animate_clear_cycle("haut", 0.4)
      self.body.animate_blend_cycle("bas")
      
  def advance_time(self, proportion):
    Fasme.advance_time(self, proportion)
    for character in self.characters_on:
      if not self.orientate_character:
        character.next_state.look_at_y(soya.Vector(self.level, 0.0, 1.0, 0.0))
        
    
cerealizer.register(UpDownFasme, classname = "balazar_brothers.platform.UpDownFasme")

class Fountain(BasePlatform):
  def __init__(self):
    super(Fountain, self).__init__()
    self.model = soya.Model.get("fontaine")
    self.water = None
    
  def set_water(self, has_water):
    if   self.water and not has_water:
      self.remove(self.water)
      self.water = None
    elif has_water and not self.water:
      self.water = soya.Body(self, soya.Model.get("fontaine_eau"))
      
  def advance_time(self, proportion):
    super(Fountain, self).advance_time(proportion)

    if self.water:
      if self.characters_on:
        self.water.y = -3.0
        
      elif (not self.characters_on) and self.water.y < 0.0 :
        self.water.y += proportion * 0.1
cerealizer.register(Fountain, classname = "balazar_brothers.platform.Fountain")

class RotatingFountain(Fountain):
  def __init__(self):
    super(RotatingFountain, self).__init__()
    self.model = soya.Model.get("fontaine@bleu")
    
  def advance_time(self, proportion):
    super(RotatingFountain, self).advance_time(proportion)
    self.rotate_lateral(3.0 * proportion)
cerealizer.register(RotatingFountain, classname = "balazar_brothers.platform.RotatingFountain")

class Tower(BasePlatform):
  def __init__(self):
    super(Tower, self).__init__()
    self.model = soya.Model.get("tour")
    wall = soya.Body(self, soya.Model.get("mur"))
    wall.y = -5.0
cerealizer.register(Tower, classname = "balazar_brothers.platform.Tower")

class RotatingTower(Tower):
  def __init__(self):
    super(RotatingTower, self).__init__()
    self.model = soya.Model.get("tour@bleu")
    
  def advance_time(self, proportion):
    super(RotatingTower, self).advance_time(proportion)
    self.rotate_lateral(3.0 * proportion)
cerealizer.register(RotatingTower, classname = "balazar_brothers.platform.RotatingTower")

class FallingTower(BumpablePlatform, BasePlatform):
  BUMP_SPEED   =  0.1
  UNBUMP_SPEED =  0.03
  MAX_BUMP     = -10.0
  
  def __init__(self):
    super(FallingTower, self).__init__()
    self.model = soya.Model.get("tour@marron")
cerealizer.register(FallingTower, classname = "balazar_brothers.platform.FallingTower")
    

# import soya.spc_material
# m = soya.spc_material.MovingMaterial(soya.Image.get("fontaine_eau.png"), 0.0, -0.03)
# m.additive_blending = 1
# m.filename = "fontaine_eau"
# m.save()

# w = soya.World.get("fontaine_eau")
# for f in w:
#   print f
#   f.lit = 1
#   for p in f:
#     if p.z < -2.0:
#       print p
#       p.color = (0.0, 0.0, 0.0, 1.0)
#       #p.color = (1.0, 1.0, 1.0, 0.0)
# w.save()

#import soya.spc_material
#m = soya.spc_material.ZoomingMaterial(soya.Image.get("portail.png"), 0.2, 0.2)
#m.additive_blending = 1
#m.filename = "portail"
#m.save()

class StartingPlatform(MultiCharactersPlatform, BasePlatform):
  def __init__(self):
    super(StartingPlatform, self).__init__()
    self.model = soya.Model.get("plateforme")
    
  def add_character(self, character, change_level = 0):
    super(StartingPlatform, self).add_character(character)

    if   len(self.characters_on) == 1: P1 = soya.Point(self, -1.0, 0.0, 0.0)
    elif len(self.characters_on) == 2: P1 = soya.Point(self,  1.0, 0.0, 0.0)
    elif len(self.characters_on) == 3: P1 = soya.Point(self, -0.5, 0.0, 0.0)
    elif len(self.characters_on) == 4: P1 = soya.Point(self,  0.5, 0.0, 0.0)
    else:                              P1 = soya.Point(self,  0.0, 0.0, 0.0)
    
    character.move(P1)
    character.next_state.convert_to(character.parent)
    character.next_state.move(P1)
    character.next_state.hack = 1
    
cerealizer.register(StartingPlatform, classname = "balazar_brothers.platform.StartingPlatform")


class PortailPlatform(MultiCharactersPlatform, BasePlatform):
  FALL_SOUND = "menu2.wav"
  
  def __init__(self, next_level_name = ""):
    super(PortailPlatform, self).__init__()
    
    self.next_level_name = next_level_name
    self.model = soya.Model.get("plateforme-1")
    
    self.label = Label3D(self, "Label")
    self.label.y = 7.5
    self.label.size = 0.03
    self.label.lit = 0
    self.label.center_y = 1
    
  def add_character(self, character, change_level = 1):
    from balazar_brothers.character import Balazar
    from balazar_brothers.player    import Player
    
    if not isinstance(character, Balazar): change_level = 0
    
    if change_level:
      if tofu.has_side("client"): return
      else:
        from balazar_brothers.level import Level
        if self.next_level_name in Level.availables():
          next_level = Level.get(self.next_level_name)
          for other_platform in next_level.mobiles:
            if isinstance(other_platform, PortailPlatform) and (other_platform.next_level_name == self.level.filename): break
          else: other_platform = self.level.get_by_class(StartingPlatform)
          
          player = Player.get(character.player_name)
          player.current_level_name  = self.next_level_name
          player.previous_level_name = character.level.filename
          
          for c in player.mobiles:
            c.previous_level_name = c.level.filename
            if c.platform:
              c.platform.remove_character(c)
              c.platform = None
            c.next_platform = None
            c.level.remove_mobile(c)
            c.platform = other_platform # Needed BEFORE calling next_level.add_mobile !
            next_level.add_mobile(c)
            c.set_platform(other_platform, change_level = 0)
          return
        
    super(PortailPlatform, self).add_character(character)
    
    if   len(self.characters_on) == 1: P1 = soya.Point(self, -1.0, 0.0, 0.0)
    elif len(self.characters_on) == 2: P1 = soya.Point(self,  1.0, 0.0, 0.0)
    elif len(self.characters_on) == 3: P1 = soya.Point(self, -0.5, 0.0, 0.0)
    elif len(self.characters_on) == 4: P1 = soya.Point(self,  0.5, 0.0, 0.0)
    else:                              P1 = soya.Point(self,  0.0, 0.0, 0.0)
    P1.convert_to(self.parent)
    character.move(P1)
    character.next_state.move(P1)
    
cerealizer.register(PortailPlatform, classname = "balazar_brothers.platform.PortailPlatform")
    

class Label3D(soya.label3d.Label3D):
  _font = None
  def __init__(self, parent = None, text = "", font = None, size = 0.01):
    soya.label3d.Label3D.__init__(self, parent, text, font, size)
    
    del self._font

  def loaded(self):
    from balazar_brothers.level import level_display_name
    
    if self.parent.parent.get_country_name() == self.parent.next_level_name[:self.parent.next_level_name.rfind("_")]:
      self.text = self.parent.next_level_name[self.parent.next_level_name.rfind("_") + 1:]
      self.size = 0.07
    else:
      self.text = _(u"Towards %s") % level_display_name(self.parent.next_level_name)
      self.size = 0.03
      
    from balazar_brothers.level import Level
    if not self.parent.next_level_name in Level.availables():
      self.text = _("__unavailable_level__")
cerealizer.register(Label3D, classname = "balazar_brothers.platform.Label3D")


class Openable(object):
  OPEN_SOUND  = ""
  CLOSE_SOUND = ""
  SOUND_GAIN = 1.0
  
  def __init__(self):
    super(Openable, self).__init__()
    
    self.opened             = 0
    self.close_duration     = 0
    self.autoclose_duration = 0
    
  def get_network_state(self):
    if self.opened: return "1"
    else:           return "0"
    
  def read_network_state(self, f):
    if f.read(1) == "1": self.set_opened(1)
    else:                self.set_opened(0)
    
  def do_collision(self):
    if self.opened and self.close_duration:
      self.close_duration -= 1
      if self.close_duration == 0: self.set_opened(0)
      
  def set_opened(self, opened):
    if opened != self.opened:
      self.opened = opened
      self.set_current_state_importance(2)
      if opened:
        self.close_duration = self.autoclose_duration
        soya.SoundPlayer(self, soya.Sound.get(self.OPEN_SOUND), gain = self.SOUND_GAIN)
      else:
        soya.SoundPlayer(self, soya.Sound.get(self.CLOSE_SOUND), gain = self.SOUND_GAIN)
        
        
class Door(Openable, BasePlatform):
  OPEN_SOUND = "door_open.wav"
  SOUND_GAIN = 10.0
  def __init__(self):
    super(Door, self).__init__()
    self.model = soya.Model.get("portique1")
    
    self.door1 = soya.Body(self, soya.Model.get("porte"))
    self.door1.set_xyz(-1.0, 0.0, 0.72)
    
    self.door2 = soya.Body(self, soya.Model.get("porte_m"))
    self.door2.set_xyz( 1.0, 0.0, 0.72)
    
    self.rotation = 0.0
    
  def suitable_for(self, character):
    return super(Door, self).suitable_for(character) and (self.opened or character.keys >= 7)
  
  def set_next_for_character(self, character):
    if character.keys >= 7:
      self.set_opened(1)
      if tofu.has_side("single") or tofu.has_side("server"):
        tofu.Player.get(character.player_name).add_bonus(keys = -7)
        
        
  def advance_time(self, proportion):
    if       self.opened and self.rotation < 150.0:
      self.rotation += 3 * proportion
      self.door1.rotate_lateral(-3 * proportion)
      self.door2.rotate_lateral( 3 * proportion)
      
    elif not self.opened and self.rotation >   0.0:
      self.rotation -= 3 * proportion
      self.door1.rotate_lateral( 3 * proportion)
      self.door2.rotate_lateral(-3 * proportion)
cerealizer.register(Door, classname = "balazar_brothers.platform.Door")


class TreePompon(soya.Body):
  def __init__(self, parent = None):
    soya.Body.__init__(self, parent, soya.Model.get("scn-tree5"))
cerealizer.register(TreePompon, classname = "balazar_brothers.platform.TreePompon")
  
class Farm(soya.World):
  def __init__(self, parent = None):
    soya.World.__init__(self, parent, soya.Model.get("ferme_champignon"))
    self.farm = soya.Body(self, soya.Model.get("ferme"))
cerealizer.register(Farm, classname = "balazar_brothers.platform.Farm")

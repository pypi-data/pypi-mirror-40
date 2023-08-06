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

import struct
import cerealizer, soya, soya.cerealizer4soya, soya.tofu as tofu

import balazar_brothers
from balazar_brothers.character import BlueBalazar, RedBalazar, MESSAGE_UPDATE_SCORE
from balazar_brothers.level     import Level, create_demo_level
from balazar_brothers.platform_ import StartingPlatform, PortailPlatform

class Player(tofu.Player):
  def __init__(self, player_id):
    tofu.Player.__init__(self, player_id)
    
    self.score = 0
    self.keys  = 0
    
    self.current_level_name  = balazar_brothers.globdef.START_LEVEL
    if not "_" in self.current_level_name[-3:]: self.current_level_name += "_1"
    self.previous_level_name = "__new__"
    
    self.current_level_name  = "tutorial_1"
    #self.current_level_name  = "fountain_river_1"
    #self.current_level_name  = "coqueliform_field_1"
    #self.current_level_name  = "pompon_forest_1"
    #self.current_level_name  = "hopeless_castle_1"
    #self.previous_level_name = "hopeless_castle_8"
    
    self.create_characters()
    
  def restart_world(self):
    self.current_level_name  = self.current_level_name[:self.current_level_name.rfind("_")] + "_1"
    self.previous_level_name = "__new__"
    for mobile in self.mobiles: mobile.die()
    
  def add_bonus(self, score = 0, keys = 0):
    self.score += score
    self.keys  += keys
    
    for character in self.mobiles:
      character.send_message("%s%s" % (MESSAGE_UPDATE_SCORE, struct.pack("!HH", self.score, self.keys)))
      
  def create_characters(self):
    level = Level.get(self.current_level_name)
    
    for starting_platform in level.mobiles:
      if isinstance(starting_platform, PortailPlatform) and (starting_platform.next_level_name == self.previous_level_name): break
    else:
      starting_platform = level.get_by_class(StartingPlatform)
      if not starting_platform:
        portails = level.get_all_by_class(PortailPlatform)
        for starting_platform in portails:
          if starting_platform.next_level_name[:-1] != level.filename[:-1]: break
          
    v = soya.Vector(starting_platform, 0.0, 0.0, -1.0) % level
    v.parent = None
    
    #starting_platform.add_xyz(1.5, 0.0, 3.0)
    
    character  = RedBalazar()
    character.previous_level_name = self.previous_level_name
    character.score = self.score
    character.keys  = self.keys
    #level.add_mobile(character)
    character.level = level
    character.platform = starting_platform
    #character.platform.rotate_lateral(180.0)
    #character.look_at(soya.Vector(character.platform, 0.0, 0.0, -1.0) % character.level)
    #character.next_state.look_at(soya.Vector(character.platform, 0.0, 0.0, -1.0) % character.level)
    character.look_at(v)
    character.next_state.look_at(v)
    self.add_mobile(character)
    #character.set_platform(starting_platform, change_level = 0)
    
    character  = BlueBalazar()
    character.previous_level_name = self.previous_level_name
    character.score = self.score
    character.keys  = self.keys
    #level.add_mobile(character)
    character.level = level
    character.platform = starting_platform
    character.look_at(v)
    character.next_state.look_at(v)
    self.add_mobile(character)
    #character.set_platform(starting_platform, change_level = 0)
    
  def login(self, sock, udp_address):
    if not self.mobiles:
      self.create_characters()
      
    tofu.Player.login(self, sock, udp_address)
    
    if tofu.has_side("server"):
      for mobile in self.mobiles:
        if mobile.platform and mobile.platform.discussion: mobile.start_discussion(mobile.platform.discussion)
      
    
    
  def remove_mobile(self, mobile):
    for character in self.mobiles:
      if not character.dying: character.die()
      
    tofu.Player.remove_mobile(self, mobile)
    
    
  def killed(self):
    self.score = max(0, self.score - 1)
    tofu.Player.killed(self, 1)
    
cerealizer.register(Player, soya.cerealizer4soya.SavedInAPathHandler(Player))


tofu.CREATE_PLAYER = Player

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
import cerealizer, soya, soya.label3d, soya.tofu as tofu

import balazar_brothers
from balazar_brothers.platform_ import Platform, MultiCharactersPlatform

ACTION_JUMP          = "J"
ACTION_STOP_JUMPING  = "j"
ACTION_SAY           = "S"
ACTION_CHAT          = "C"

STATE_ABSOLUTE       = "A"
STATE_ON_PLATFORMS   = "P"

MESSAGE_UPDATE_SCORE = "S"
MESSAGE_DISCUSSION   = "D"
MESSAGE_SAY          = "s"
MESSAGE_CHAT         = "C"
MESSAGE_SOUND        = "!"

P1 = soya.Point ()
V1 = soya.Vector()

    
class Character(tofu.SpeedInterpolatedMobile, tofu.AnimatedMobile, Platform):
  COUIC_SOUND      = "couic2.wav"
  ANIMATION_SUFFIX = ""
  
  def __init__(self):
    super(Character, self).__init__()
    Platform.__init__(self)
    
    self.platform_position   = soya.Point(self, 0.0, 2.1, 0.0)
    self.center              = soya.Point(self, 0.0, 1.1, 0.0)

    self.power               = 8.0 # How far the character can jump ?
    self.speed_factor        = 0.1
    self.platform            = None
    self.next_platform       = None
    self.front               = soya.Vector(self, 0.0, 0.0, -1.0)
    self.jump_proportion     = 0.0
    self.jump_start_position = soya.Point()
    self.dying               = 0
    self.current_discussion  = None
    self.want_to_jump        = 0
    self.wait_before_suicide = 20
    
  def get_network_state(self):
    if self.platform or self.next_platform: return STATE_ON_PLATFORMS + tofu.Unique.dumpsuid_or_none(self.platform) + tofu.Unique.dumpsuid_or_none(self.next_platform) + struct.pack("!f", self.jump_proportion)
    return STATE_ABSOLUTE + tofu.Unique.dumpsuid_or_none(self.platform) + tofu.Unique.dumpsuid_or_none(self.next_platform) + super(Character, self).get_network_state()
  
  def read_network_state(self, f):
    code = f.read(1)
    
    self.network_last_state_round = self.network_next_state_round
    self.network_next_state_round = self.level.round

    platform      = tofu.Unique.undumpsuid(f.read(2))
    next_platform = tofu.Unique.undumpsuid(f.read(2))
    
    if not platform is self.platform:
      if self.platform: self.platform.remove_character(self)
      
      if platform:
        self.platform      = platform
        self.next_platform = next_platform
        self.jump_ended()
      else:
        if not self.platform: self.jump_ended()
        self.platform      = platform
        self.next_platform = next_platform
        self.jump()
        
    elif not next_platform is self.next_platform:
      if not self.platform:
        self.platform = self.next_platform
        self.jump_ended()
        self.next_platform = next_platform
        self.jump()
        
      else:
        self.next_platform = next_platform

    if (self.platform is None) and (self.next_platform is None):
      self.die()
      
    if   code == STATE_ON_PLATFORMS:
      self.jump_proportion = struct.unpack("!f", f.read(4))[0]
      
    elif code == STATE_ABSOLUTE:
      super(Character, self).read_network_state(f)
      
    else: raise ValueError("Unkown state code '%s'!" % code)
    
    
  def __getstate__(self):
    front = soya.Vector(self, 0.0, 0.0, -1.0)
    front.convert_to(self.level)
    
    for i in self.characters_on: self.remove(i)
    parent = self.parent
    if parent: parent.remove(self)
    if self.level: self.level.add(self)
    self.look_at(front)
    
    state = super(Character, self).__getstate__()
    state = map(lambda i: (isinstance(i, list) and i[:]) or i, state[0]), state[1].copy()
    
    if parent: parent.add(self)
    self.look_at(front)
    for i in self.characters_on: self.add(i)
    
    del state[1]["current_discussion" ]
    del state[1]["platform"           ]
    del state[1]["next_platform"      ]
    del state[1]["jump_start_position"]
    del state[1]["characters_on"      ]
    del state[1]["last_state"         ]
    del state[1]["next_state"         ]
    del state[1]["speed"              ]
    
    state[1]["platform_platid"] = self.platid
    
    return state
  
  def __setstate__(self, state):
    super(Character, self).__setstate__(state)
    
    self.current_discussion  = None
    self.platform            = None
    self.next_platform       = None
    self.jump_start_position = soya.Point()
    self.characters_on       = []
    self.last_state          = soya.CoordSystState(self)
    self.next_state          = soya.CoordSystState(self)
    self.speed               = soya.CoordSystSpeed(None)
    
  def loaded(self):
    super(Character, self).loaded()
    self.put_on_platform()
    
  def put_on_platform(self):
    if self.platform: # For newly created characters
      if not self in self.platform.characters_on:
        self.platform.add_character(self, change_level = 0)
      return
    
    if self.platform_platid == 0:
      if not tofu.has_side("client"): self.die()
    else:
      self.platform = self.level.platforms[self.platform_platid]
      if self in self.platform.characters_on:
        self.platform.remove_character(self)
        self.platform.add_character(self, change_level = 0)
      else:
        while (self.platform.characters_on) and not (self.platform.suitable_for(self)):
          self.platform = self.platform.characters_on[0]
        if not self in self.platform.characters_on:
          if isinstance(self.platform, balazar_brothers.platform.PortailPlatform):
            self.set_platform(self.platform, change_level = 0)
          else:
            self.platform.add_character(self, change_level = 0)
            
    del self.platform_platid
    
  def set_platform(self, platform, **kargs):
    if self.platform and (self in self.platform.characters_on): self.platform.remove_character(self)
    
    self.platform = platform
    
    if platform:
      platform.add_character(self, **kargs)
      self.next_state.look_at(soya.Vector(platform, 0.0, 0.0, -1.0) % platform.level)
      
      self.set_animation("attente")
      self.dying = 0
      self.speed.set_identity()
      
  def get_platid(self):
    if self.platform     : return self.platform     .platid
    if self.next_platform: return self.next_platform.platid
    return 0
  platid = property(get_platid)
  
  def find_next_platform(self, position = None, front = None, power = None, max_angle = 75.0, angle_factor = 0.07, exclude = []):
    if not position: position = self
    if not front   : front    = self.front
    if not power   : power    = self.power
    
    best_platform = None
    best_distance = power
    
    for platform in self.level.mobiles:
      if isinstance(platform, Platform) and (not platform is self) and (not platform is self.platform) and platform.suitable_for(self) and (not platform in exclude):
        if isinstance(self.platform, Character) and (self.platform.next_platform is platform) and (not self.platform.platform): continue
        if isinstance(platform, Character) and platform.dying: continue
        V1.set_start_end(position, platform.platform_position)
        if V1.y <= 0.0: V1.y /= 100.0 # Don't limit how far the character can fall down.
        
        angle = front.angle_to(V1)
        
        if (angle < max_angle) and V1.y < 2.5:
          if (V1.y > 1.0) and isinstance(platform, Character): continue
          distance = V1.length() + angle_factor * angle
          
          if distance < best_distance:
            best_distance = distance
            best_platform = platform
            
    if best_platform: best_platform.set_next_for_character(self)
    return best_platform
  
  def compute_trajectory(self, start_position, end_position, jump_proportion):
    global P1, V1
    V1.set_start_end(self, end_position)
    V1.convert_to(self)
    V1 *= self.speed_factor / (1.0 - jump_proportion)
    self.speed.set_identity()
    self.speed.move(V1)
    self.speed.y += -0.4 * (((jump_proportion - 4.0 * self.speed_factor) * 2.0) - 1.0)
    
    V1.set_start_end(start_position, end_position)
    V1.y = 0.0
    angle = min(self.front.angle_to(V1), 100.0 * self.speed_factor)
    
    P1.clone(end_position)
    P1.convert_to(self)
    if P1.x > 0.0: angle *= -1.0
    
    self.speed.rotate_lateral(angle)
    
  def can_kill    (self, character): return 1
  def want_to_kill(self, character): return self.can_kill(character)
  
  def die(self, dying_sens = None, move = 1):
    if (not self.dying) or (self.dying > 20):
      self.set_current_state_importance(2)
      self.dying = 1
      
      self.jump_start_position.clone(self)
      self.next_platform = None
      self.set_animation("couicavant")
      if self.platform:
        self.platform.remove_character(self)
        self.platform = None
      if move:
        if not dying_sens: dying_sens = soya.Vector(self, 0.0, 0.4, -0.2)
        look_dir = dying_sens % self.level
        look_dir.y = 0.0
        self.next_state.look_at(look_dir)
        dying_sens = dying_sens % self.next_state
        self.speed.set_xyz(dying_sens.x, dying_sens.y, dying_sens.z)
        
    if self.characters_on:
      V1.__init__(self, 0.0, 0.0, -1.0)
      self.characters_on[0].look_at(V1)
      self.characters_on[0].next_state.look_at(V1)
      self.characters_on[0].set_animation("freresurf")
      self.characters_on[0].set_current_state_importance(2)
      soya.SoundPlayer(self, soya.Sound.get("brother_surf.wav"))
      
  def kill(self):
    if not self.dying: self.dying = 1 # Must have dying == 1 for being killed
    for character in self.characters_on:
      character.kill()
    super(Character, self).kill()
    
  @tofu.side("client")
  def start_discussion(self, gettext_key): pass
  
  @tofu.side("single", "server")
  def start_discussion(self, gettext_key):
    self.send_message(MESSAGE_DISCUSSION + gettext_key.encode("utf8"))
    
  def do_action(self, action):
    if   action[0] == ACTION_JUMP: self.want_to_jump = 1
    
    elif action[0] == ACTION_STOP_JUMPING: self.want_to_jump = 0
    
    elif action[0] == ACTION_SAY:
      if self.current_discussion: self.send_message(MESSAGE_SAY)
      
    elif action[0] == ACTION_CHAT:
      self.send_message(action)
      
    else: raise ValueError("Unkown action code '%s'!" % code)
    
  def jump(self):
    if self.next_platform:
      self.wait_before_suicide = 20
      if self.platform: self.jump_start_position.clone(self.platform.platform_position)
      else:             self.jump_start_position.clone(self)
      self.jump_start_position.convert_to(self.level)
      self.jump_proportion = 0.0
      self.set_animation("saute")
      if self.platform:
        self.platform.remove_character(self)
        self.platform = None
      self.set_current_state_importance(2)
    else:
      if self.wait_before_suicide: self.wait_before_suicide -= 1
      else:                        self.die()
      
  def jump_ended(self):
    self.set_current_state_importance(2)
    self.platform.add_character(self)
    
    if not self.platform: return # Occurs if the platform is already occuped by someone you cannot kill. Implies that the character is currently dying.
    soya.SoundPlayer(self, soya.Sound.get(self.platform.FALL_SOUND))
    self.speed.set_identity()
    self.set_animation("attente")
    
  def do_physics(self):
    if self.platform:
      if not self.current_animation: self.set_animation("attente")
      
    if self.dying:
      
      #if self.dying == 1:
      #  self.set_current_state_importance(2)
      self.set_current_state_importance(1)
      if self.dying <  60:
        #if   self.dying == 1: self.speed.turn_vertical(-5.0)
        #elif self.dying == 8: self.speed.turn_vertical( 5.0)
        if self.characters_on:
          self.speed.y -= 0.01
        else:
          self.speed.y -= 0.02
          
      if self.characters_on:
        self.dying += 0.25
      else:
        if self.dying == 10.0:
          soya.SoundPlayer(self, soya.Sound.get(self.COUIC_SOUND))
        self.dying += 1
        
    elif not self.platform:
      self.set_current_state_importance(1)
      if self.jump_proportion < 0.96: # Jumping
        self.compute_trajectory(self.jump_start_position, self.next_platform.platform_position, self.jump_proportion)
        
        if (self.jump_proportion > 0.8) and not self.current_animation.startswith("attente"):
          self.set_animation("attente")
          
      else: # Jump is ended.
        self.platform = self.next_platform
        self.jump_ended()
        
    if self.dying and self.characters_on:
      self.speed.set_xyz(self.speed.x / 2.0, self.speed.y / 2.0, self.speed.z / 2.0)
      
    super(Character, self).do_physics()
    
    if self.dying and self.characters_on:
      self.speed.set_xyz(self.speed.x * 2.0, self.speed.y * 2.0, self.speed.z * 2.0)
      
  def do_collisions(self):
    if self.y < -50.0:
      self.kill()
      return
    
    if self.platform:
      next_platform = self.find_next_platform()
      if not next_platform is self.next_platform:
        self.next_platform = next_platform
        self.set_current_state_importance(2)
        
      if self.want_to_jump: self.jump()
      else:                 self.wait_before_suicide = 20
      
  def get_discussion(self, gettext_key):
    characters = { "owner" : self }
    if isinstance(self, Balazar):
      characters["red" ], characters["blue"] = self.get_teamates()
      
    return balazar_brothers.discussion.Discussion(gettext_key, characters)
    
  def add_character(self, character, change_level = 0):
    Platform.add_character(self, character)
    animation = (self.current_animation or "attente").split("_")[0]
    if animation == "bonus": animation = "attente"
    self.set_animation(animation)
    character.set_animation("attente")
    
  def remove_character(self, character):
    Platform.remove_character(self, character)
    animation = (self.current_animation or "attente").split("_")[0]
    if animation == "bonus": animation = "attente"
    self.set_animation(animation)
    
  def set_animation(self, animation, fade = 0.1):
    if (animation == "attente") and (self.current_animation.startswith("bonus")) and (not self.characters_on): return
    if animation == "bonus" and self.characters_on: return
    if   animation == "attente":
      if   self.characters_on:                   animation += "_portage"
      elif isinstance(self.platform, Character): animation += "_porte"
    elif animation == "saute":
      if   self.characters_on:                   animation += "_portage"
    if not animation.endswith(self.ANIMATION_SUFFIX): animation += self.ANIMATION_SUFFIX
    
    super(Character, self).set_animation(animation, fade)
    
  def advance_time(self, proportion):
    if not self.platform:
      if self.dying: pass
      else: self.jump_proportion += proportion * self.speed_factor
      
    super(Character, self).advance_time(proportion)
    


class Balazar(Character):
  def __init__(self):
    Character.__init__(self)
    
    self.events              = []
    self.previous_level_name = ""
    
    self.score = 0
    self.keys  = 0

  @tofu.side("client")
  def loaded(self):
    Character.loaded(self)
    
    label = soya.label3d.Label3D(self, self.player_name, font = balazar_brothers.main_loop.BIG_FONT, size = 0.01)
    label.y = 3.5
    label.lit = 0
    label.auto_flip = 1
    
  def want_to_kill(self, character):
    if isinstance(character, Balazar) and (character.player_name == self.player_name): return 0
    return Character.want_to_kill(self, character)
  
  def control_owned(self):
    super(Balazar, self).control_owned()
    
    soya.MAIN_LOOP.camera.zap()
    self.arrow.visible = 1
    
  def generate_actions(self):
    for event in self.events:
      if   event == ACTION_JUMP:         self.send_action(ACTION_JUMP + ((self.next_platform and self.next_platform.dumpsuid()) or struct.pack("!H", 0)))
      elif event == ACTION_STOP_JUMPING: self.send_action(ACTION_STOP_JUMPING)
      elif event == ACTION_SAY         : self.send_action(ACTION_SAY)
    self.events *= 0
    
    
  @tofu.side("server")
  def get_teamates(self):
    player = tofu.Player.get(self.player_name)
    return [player.mobiles[0], player.mobiles[-1]]
    
  @tofu.side("single", "client")
  def get_teamates(self):
    if soya.MAIN_LOOP.traveling.characters:
      return [soya.MAIN_LOOP.traveling.characters[ 0], soya.MAIN_LOOP.traveling.characters[-1]]
      
    else:
      teamates = [None, None]
      level = self.level
      if not level:
        level = self.platform
        while not isinstance(level, balazar_brothers.level.Level): level = level.parent
      if level:
        for i in level.recursive():
          if isinstance(i, Character):
            if i.player_name == self.player_name:
              if   isinstance(i, RedBalazar ): teamates[0] = i
              elif isinstance(i, BlueBalazar): teamates[1] = i
      return teamates
    
  def added_into(self, level):
    super(Balazar, self).added_into(level)
    
  def do_message(self, message):
    if   message.startswith(MESSAGE_UPDATE_SCORE):
      self.score, self.keys = struct.unpack("!HH", message[1:])
      
    elif message.startswith(MESSAGE_DISCUSSION):
      self.do_discussion(message[1:].decode("utf-8"))
      
    elif message.startswith(MESSAGE_SAY):
      self.current_discussion.on_validate()
      
    elif message.startswith(MESSAGE_CHAT):
      self.do_say_chat(message[1:].decode("utf-8"))
      
    elif message.startswith(MESSAGE_SOUND):
      if " " in message:
        sound, gain = message[1:].split(" ")
        gain = int(gain)
      else:
        sound = message[1:]
        gain = 1.0
      soya.SoundPlayer(self, soya.Sound.get(sound), gain = gain)
    else: raise ValueError("Unknown message code '%s'!" % message[0])
    
  @tofu.side("server")
  def do_discussion(self, gettextkey):
    discussion = self.get_discussion(gettextkey) # Sets self.current_discussion
    
  @tofu.side("single", "client")
  def do_discussion(self, gettextkey):
    discussion = self.get_discussion(gettextkey)
    if discussion.can_say(): discussion.show()
    
  @tofu.side("server")
  def do_say_chat(self, text):
    print "* BalazarBrothers * %s says '%s'" % (self.player_name, text)
    
  @tofu.side("single", "client")
  def do_say_chat(self, text):
    from balazar_brothers.discussion import ChatLabel
    ChatLabel(soya.MAIN_LOOP.root_widget, self, text)

class BlueBalazar(Balazar):
  ANIMATION_SUFFIX = "_blu"
  
  def __init__(self):
    Balazar.__init__(self)
    
    self.set_model(soya.AnimatedModel.get("balazar"), ["perso"])
    
    self.arrow = Arrow(self, (0.3, 0.0, 1.0, 1.0))
    self.arrow.visible = 0
    
  def control_owned(self):
    Balazar.control_owned(self)

    for i in soya.MAIN_LOOP.traveling.characters[:]:
      if isinstance(i, self.__class__): soya.MAIN_LOOP.traveling.characters.remove(i)
    soya.MAIN_LOOP.traveling.characters.insert(1, self)
    
    soya.MAIN_LOOP.score_label.character = soya.MAIN_LOOP.keys_label.character = self
    
  def have_said___quit_None_blue__(self, discussion):
    if not self.controller.remote: soya.MAIN_LOOP.stop()
cerealizer.register(BlueBalazar)
    
    
class RedBalazar(Balazar):
  ANIMATION_SUFFIX = "_red"
  
  def __init__(self):
    Balazar.__init__(self)
    
    self.set_model(soya.AnimatedModel.get("balazar@rouge"), ["perso"])
    
    self.arrow = Arrow(self, (1.0, 0.2, 0.2, 1.0))
    self.arrow.visible = 0
    
  def control_owned(self):
    Balazar.control_owned(self)
    
    for i in soya.MAIN_LOOP.traveling.characters[:]:
      if isinstance(i, self.__class__): soya.MAIN_LOOP.traveling.characters.remove(i)
    soya.MAIN_LOOP.traveling.characters.insert(0, self)
    
  def have_said___quit_None_red__(self, discussion):
    if not self.doer.remote: tofu.Player.get(self.player_name).restart_world()
cerealizer.register(RedBalazar)

    
import soya.opengl as opengl

class Arrow(soya.PythonCoordSyst):
  def __init__(self, parent = None, color = (1.0, 1.0, 1.0, 1.0)):
    soya.PythonCoordSyst.__init__(self, parent)
    
    self.color = color
    
  def batch(self):
    if self.color[3] < 1.0: return 2, self, None
    else:                   return 1, self, None

  def render(self):
    character = self.parent
    if character.platform and character.next_platform:
      P1.clone(character.next_platform.platform_position)
      P1.convert_to(self)
      
    elif not character.platform:
      if character.next_platform:
        P1.clone(character.next_platform.platform_position)
        P1.convert_to(self)
      else: return
    else: return
    
    self.look_at(self.parent.next_platform.platform_position)
    
    soya.DEFAULT_MATERIAL.activate()
    opengl.glDisable(opengl.GL_TEXTURE_2D)
    opengl.glDisable(opengl.GL_CULL_FACE)
    opengl.glDisable(opengl.GL_LIGHTING)
    opengl.glColor4f(*self.color)
    opengl.glBegin(opengl.GL_LINES)

    dy = 0.0
    for i in range(6):
      f1 = (i + 0.0) / 6.0
      f2 = (i + 1.0) / 6.0

      z1 = P1.z * f1
      z2 = P1.z * f2

      y1 = P1.y * f1 + dy; dy -= 0.6 * (2.0 * f1 - 1.0)
      y2 = P1.y * f2 + dy

      if i == 5:
        opengl.glVertex3f(-0.15, y1, z1)
        opengl.glVertex3f(-0.4, y1, z1)
        opengl.glVertex3f( 0.15, y1, z1)
        opengl.glVertex3f( 0.4, y1, z1)
        
        opengl.glVertex3f(-0.4, y1, z1)
        opengl.glVertex3f(-0.0, y2, z2)
        opengl.glVertex3f( 0.0, y2, z2)
        opengl.glVertex3f( 0.4, y1, z1)
      else:
        opengl.glVertex3f(-0.15, y1, z1)
        opengl.glVertex3f(-0.15, y2, z2)
        opengl.glVertex3f( 0.15, y2, z2)
        opengl.glVertex3f( 0.15, y1, z1)

    opengl.glEnd()
    
    opengl.glEnable(opengl.GL_CULL_FACE)
    opengl.glEnable(opengl.GL_LIGHTING)
cerealizer.register(Arrow)
      

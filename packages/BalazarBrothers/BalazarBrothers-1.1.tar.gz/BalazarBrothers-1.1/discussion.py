# Balazar Brothers
# Copyright (C) 2007 Jean-Baptiste LAMY
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

import soya, soya.tofu as tofu, soya.sdlconst as sdlconst, soya._soya, soya.widget as widget, soya.opengl as opengl
import balazar_brothers, balazar_brothers.globdef as globdef

class Bubble(widget.Label):
  def __init__(self, master = None, pos = 0, text = None, color = soya.BLACK):
    widget.Label.__init__(self, master, text, color = color)
    
    self.position   = soya.Point()
    self.discussion = None
    self.pos        = pos
    
    if   pos == -1: self.resize_style = [ 'parent left'         , 'parent top', ('percent width', 0.33)]
    elif pos ==  0: self.resize_style = [("percent left", 0.335), 'parent top', ('percent width', 0.33)]
    elif pos ==  1: self.resize_style = [("percent left", 0.67 ), 'parent top', ('percent width', 0.33)]
    elif pos ==  2: self.resize_style = [("percent left", 0.2  ), ('percent top', 0.3), ('percent width', 0.6 )]
    elif pos ==  3: self.resize_style = [("percent left", 0.2  ), ('percent width', 0.6 )]
   
  def build_display_list(self):
    opengl.glColor4f(*self._color)
    self._font.draw_area(self._text, self.left + 5, self.top + 3, 0.0, self.width - 10, self.height, self._align)
    
  def set_text(self, text):
    widget.Label.set_text(self, text)
    self.height = self.font.wordwrap(self._text, self.width - 10)[1] + 15.0
  text = property(widget.Label.get_text, set_text)
  
  def render(self):
    if not self.discussion: return
    
    opengl.glPushMatrix()
    opengl.glTranslatef(self.left, self.top, 0.0)
    
    soya.DEFAULT_MATERIAL.activate()
    opengl.glEnable(opengl.GL_BLEND)
    opengl.glColor4f(1.0, 1.0, 1.0, 0.9)
    opengl.glBegin(opengl.GL_POLYGON)

    if self.pos < 2:
      opengl.glVertex2f(0.0, 0.0)
    else:
      opengl.glVertex2f(15.0             ,  0.0)
      opengl.glVertex2f(5.0              ,  5.0)
      opengl.glVertex2f(0.0              , 15.0)
      
    if self.pos == -1:
      opengl.glVertex2f(0.0              , self.height)
    else:
      opengl.glVertex2f(0.0              , self.height - 15.0)
      opengl.glVertex2f(5.0              , self.height -  5.0)
      opengl.glVertex2f(15.0             , self.height)
      
    if self.pos ==  1:
      opengl.glVertex2f(self.width       , self.height)
    else:
      opengl.glVertex2f(self.width - 15.0, self.height)
      opengl.glVertex2f(self.width - 5.0 , self.height -  5.0)
      opengl.glVertex2f(self.width       , self.height - 15.0)
      
    if self.pos < 2:
      opengl.glVertex2f(self.width, 0.0)
    else:
      opengl.glVertex2f(self.width       , 15.0)
      opengl.glVertex2f(self.width - 5.0 ,  5.0)
      opengl.glVertex2f(self.width - 15.0,  0.0)
      
    opengl.glEnd()

    character = getattr(self.discussion, "character", 0) or getattr(self, "character", 0)
    if character:
      opengl.glBegin(opengl.GL_TRIANGLES)
      if self.pos == 3:
        self.position.__init__(character, 0.0, 0.0, 0.0)
        x, y = soya.MAIN_LOOP.camera.coord3d_to_2d(self.position)
        x -= self.left
        y -= self.top
        
        opengl.glVertex2f(min(max(x - 5.0, 15.0), self.width - 25.0), 0.0)
        opengl.glVertex2f(min(max(x + 5.0, 25.0), self.width - 15.0), 0.0)
        opengl.glColor4f(1.0, 1.0, 1.0, 0.1)
        opengl.glVertex2f(x, y)
      else:
        self.position.__init__(character, 0.0, 2.6, 0.0)
        x, y = soya.MAIN_LOOP.camera.coord3d_to_2d(self.position)
        
        opengl.glVertex2f(self.width * 0.55, self.height)
        opengl.glVertex2f(self.width * 0.45, self.height)
        opengl.glColor4f(1.0, 1.0, 1.0, 0.1)
        opengl.glVertex2f(x - self.left, max(y, self.height + 20.0) - self.top)
      opengl.glEnd()
      
    opengl.glDisable(opengl.GL_BLEND)
        
    opengl.glPopMatrix()
    
    widget.Label.render(self)


class Discussion(tofu.Multisided):
  def __init__(self, gettext_key, characters = {}, radius = 5.0):
    self.gettext_key = gettext_key
    self.text        = _(gettext_key)
    self.validable   = 0
    self.characters  = characters
    self.radius      = radius
    
    from balazar_brothers.character import Balazar, RedBalazar
    
    names = gettext_key[:-2].split("_")
    self.character = self._find_character(names[-1])
    if isinstance(self.character, Balazar):
      self.npc = self._find_character(names[-2])
      self.validable = 1
      if isinstance(self.character, RedBalazar): self.text = self.text + u"\n\n" + _("__press_left_shift__" )
      else:                                      self.text = self.text + u"\n\n" + _("__press_right_shift__")
    else:
      self.npc = self.character
      
    if self.validable:
      self.replies = []
      self.character.current_discussion = self
    else:
      self.replies = self.find_replies()
      
  def _find_character(self, name):
    if   name == "None":                return None
    elif name == "npc" :                return self.npc
    elif self.characters.has_key(name): return self.characters[name]
    else:
      for i in soya.MAIN_LOOP.scenes[0].recursive():
        if (getattr(i, "name", "") == name) or (i.__class__.__name__ == name): return i
        
  def can_say(self):
    can_say = getattr((self.npc or self), "can_say_" + self.gettext_key, None)
    if can_say: return can_say()
    return 1
  
  def show(self):
    if not soya.MAIN_LOOP.traveling.characters: return
    
    if   self.character == soya.MAIN_LOOP.traveling.characters[ 0]: self.bubble = soya.MAIN_LOOP.left_bubble
    elif self.character == soya.MAIN_LOOP.traveling.characters[-1]: self.bubble = soya.MAIN_LOOP.right_bubble
    else:                                                           self.bubble = soya.MAIN_LOOP.middle_bubble
    self.bubble.discussion = self
    self.bubble.text       = self.text
    
    soya.MAIN_LOOP.listener.reset()
    
    for reply in self.replies: reply.show()
      
  def hide(self):
    self.bubble.discussion = None
    self.bubble = None
    if self.character and (self.character.current_discussion is self):
      self.character.current_discussion = None
      
  def begin_round(self):
    if self.npc:
      for character in soya.MAIN_LOOP.traveling.characters:
        if character.distance_to(self.npc) > self.radius + 0.1:
          self.bubble.hide()
          
  def find_replies(self):
    if   hasattr(self.character, "have_said_%s" % self.gettext_key): replies = getattr(self.character, "have_said_%s" % self.gettext_key)(self) or []
    elif hasattr(self.npc,       "have_said_%s" % self.gettext_key): replies = getattr(self.npc      , "have_said_%s" % self.gettext_key)(self) or []
    elif hasattr(self,           "have_said_%s" % self.gettext_key): replies = getattr(self          , "have_said_%s" % self.gettext_key)()     or []
    else:                                                            replies = []
    
    nb_ = self.gettext_key.count("_") + 1
    start = self.gettext_key[:-1]
    
    for key in globdef.translator._catalog.keys():
      if key.startswith(start) and (key.count("_") == nb_):
        reply = Discussion(key, self.characters, self.radius)
        if reply.can_say():
          replies.append(reply)
          
    return replies
  
  @tofu.side("single", "client")
  def on_validate(self):
    if self.validable and soya.MAIN_LOOP:
      if soya.MAIN_LOOP.left_bubble  .discussion: soya.MAIN_LOOP.left_bubble  .discussion.hide()
      if soya.MAIN_LOOP.middle_bubble.discussion: soya.MAIN_LOOP.middle_bubble.discussion.hide()
      if soya.MAIN_LOOP.right_bubble .discussion: soya.MAIN_LOOP.right_bubble .discussion.hide()
      
  @tofu.side("single", "server")
  def on_validate(self):
    for reply in self.find_replies():
      self.character.start_discussion(reply.gettext_key)
      
  def can_say___help5_None__      (self): return isinstance(self.characters["owner"], balazar_brothers.character.BlueBalazar)
  def can_say___ransom_None_blue__(self):
    print "can_say___ransom_ok__", self.characters["owner"], self.characters["owner"].score
    return self.characters["owner"].score >= 100
  def can_say___ransom_None_red__ (self):
    print "can_say___ransom_failed__", self.characters["owner"], self.characters["owner"].score
    return self.characters["owner"].score  < 100
  
  def have_said___ransom_None_blue__(self):
    grid = self.characters["owner"].level.get_by_class(balazar_brothers.trap.BigGrid)
    print "have_said___ransom_ok__", grid
    grid.open()
    
    
class ChatLabel(Bubble):
  def __init__(self, master, character, text, time = 250):
    Bubble.__init__(self, master, 3)
    self.character  = character
    self.text       = character.player_name + " : " + text
    self.discussion = 1
    self.time       = time
    
    chat_labels = [child for child in master.children if isinstance(child, ChatLabel)]
    
    total_height = sum([chat_label.height for chat_label in chat_labels])
    if (len(chat_labels) > 1) and (total_height > soya.get_screen_height() / 4.0):
      chat_labels[0].close()
      del chat_labels[0]
      
    total_height = 0
    y = soya.get_screen_height()
    for chat_label in chat_labels:
      total_height += chat_label.height
      chat_label.top = soya.get_screen_height() - total_height
      chat_label._changed = -2

  def render(self):
    Bubble.render(self)
    
    self.time -= 1
    if self.time < 0:
      master = self.master
      self.close()
      
      chat_labels = [child for child in master.children if isinstance(child, ChatLabel)]
      total_height = 0
      y = soya.get_screen_height()
      for chat_label in chat_labels:
        total_height += chat_label.height
        chat_label.top = soya.get_screen_height() - total_height
        chat_label._changed = -2
        
  def close(self):
    self.master.remove(self)
    
    
class ChatEntry(Bubble):
  def __init__(self, master, character, text = _("Chat: ")):
    Bubble.__init__(self, master, 2)
    self.character  = character
    self.text       = text
    self.discussion = 1
    
  def on_key_pressed(self, key_id, mods):
    if   (key_id == sdlconst.K_KP_ENTER or key_id == sdlconst.K_RETURN):
      self.master.remove(self)
      soya.MAIN_LOOP.entry = None
      if self.text.startswith(_("Chat: ")):
        text = self.text[len(_("Chat: ")):].encode("utf-8")
        if text: self.character.send_action("C" + text)
        
    elif (key_id == sdlconst.K_DELETE or key_id == sdlconst.K_BACKSPACE or key_id == sdlconst.K_CLEAR):
      self.text = self.text[:-1]
    elif (key_id == sdlconst.K_KP0) or (key_id == sdlconst.K_0): self.text += '0'
    elif (key_id == sdlconst.K_KP1) or (key_id == sdlconst.K_1): self.text += '1'
    elif (key_id == sdlconst.K_KP2) or (key_id == sdlconst.K_2): self.text += '2'
    elif (key_id == sdlconst.K_KP3) or (key_id == sdlconst.K_3): self.text += '3'
    elif (key_id == sdlconst.K_KP4) or (key_id == sdlconst.K_4): self.text += '4'
    elif (key_id == sdlconst.K_KP5) or (key_id == sdlconst.K_5): self.text += '5'
    elif (key_id == sdlconst.K_KP6) or (key_id == sdlconst.K_6): self.text += '6'
    elif (key_id == sdlconst.K_KP7) or (key_id == sdlconst.K_7): self.text += '7'
    elif (key_id == sdlconst.K_KP8) or (key_id == sdlconst.K_8): self.text += '8'
    elif (key_id == sdlconst.K_KP9) or (key_id == sdlconst.K_9): self.text += '9'
    elif (key_id == sdlconst.K_KP_PERIOD or key_id == sdlconst.K_PERIOD): self.text += '.'
    else:
      if mods & (sdlconst.MOD_SHIFT | sdlconst.MOD_CAPS):
        if   (key_id >= sdlconst.K_a and key_id <= sdlconst.K_z): self.text += unichr(key_id - 32)
        elif (key_id == sdlconst.K_SEMICOLON):                    self.text += '.'
      else:
        if   (key_id >= sdlconst.K_a and key_id <= sdlconst.K_z): self.text += unichr(key_id)
        elif (key_id >= 0 and key_id < 256):                      self.text += unichr(key_id)
    

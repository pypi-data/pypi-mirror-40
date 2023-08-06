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

import os, os.path, random
import cerealizer
import soya, soya.tofu as tofu, soya.sdlconst as sdlconst

import balazar_brothers, balazar_brothers.globdef as globdef

class EventListener(soya.CoordSyst):
  def __init__(self, parent = None):
    soya.CoordSyst.__init__(self, parent)
    
    self.jump1_keys       = set([sdlconst.K_LSHIFT, sdlconst.K_LCTRL, sdlconst.K_SPACE, "0", "6"]) # Strings are for joystick buttons.
    self.jump2_keys       = set([sdlconst.K_RSHIFT, sdlconst.K_RCTRL, sdlconst.K_SPACE, "1", "7"])
    self.chat_keys        = set([sdlconst.K_KP_ENTER, sdlconst.K_RETURN])
    self.quit_keys        = set([sdlconst.K_q, sdlconst.K_ESCAPE, "2"])
    self.screenshot_keys  = set([sdlconst.K_c])
    
    self.camera_distance_speed  = 0.0
    self.camera_angle_speed     = 0.0
    self.nb_camera_keys_pressed = 0.0
    self.reset()
    
  def reset(self):
    self.jump1_key_down = 0
    self.jump2_key_down = 0
    
  def begin_round(self):
    events = soya.process_event()
    
    for event in events:
      if   event[0] == sdlconst.JOYAXISMOTION:
        
        if   event[1] == 0:
          if   event[2] < 0: event_type = sdlconst.KEYDOWN; event_key = sdlconst.K_LEFT
          elif event[2] > 0: event_type = sdlconst.KEYDOWN; event_key = sdlconst.K_RIGHT
          else:              event_type = sdlconst.KEYUP  ; event_key = sdlconst.K_LEFT # XXX or right
        elif event[1] == 1:
          if   event[2] < 0: event_type = sdlconst.KEYDOWN; event_key = sdlconst.K_UP
          elif event[2] > 0: event_type = sdlconst.KEYDOWN; event_key = sdlconst.K_DOWN
          else:              event_type = sdlconst.KEYUP  ; event_key = sdlconst.K_UP # XXX or down
          
      elif event[0] == sdlconst.JOYBUTTONDOWN:
        event_type = sdlconst.KEYDOWN
        event_key  = str(event[1])
        event_mod  = 0
        
      elif event[0] == sdlconst.JOYBUTTONUP:
        event_type = sdlconst.KEYUP
        event_key  = str(event[1])
        event_mod  = 0
        
      else:
        event_type = event[0]
        if len(event) > 1:
          event_key  = event[1]
          if len(event) > 3: event_mod = event[2]
          else:              event_mod = 0
          
      if event_type == sdlconst.KEYDOWN:
        if soya.MAIN_LOOP.entry:
          soya.MAIN_LOOP.entry.on_key_pressed(event_key, event_mod)
        else:
          if   event_key in self.jump1_keys:
            if soya.MAIN_LOOP.traveling.characters[ 0].current_discussion:
              soya.MAIN_LOOP.traveling.characters[ 0].events.append("S")
            else:
              soya.MAIN_LOOP.traveling.characters[ 0].events.append("J")
          if   event_key in self.jump2_keys:
            if soya.MAIN_LOOP.traveling.characters[-1].current_discussion:
              soya.MAIN_LOOP.traveling.characters[-1].events.append("S")
            else:
              soya.MAIN_LOOP.traveling.characters[-1].events.append("J")
              
          elif event_key in self.chat_keys:
            from balazar_brothers.discussion import ChatEntry
            soya.MAIN_LOOP.entry = ChatEntry(soya.MAIN_LOOP.root_widget, soya.MAIN_LOOP.traveling.characters[-1] or soya.MAIN_LOOP.traveling.characters[0])
            
          elif event_key in self.quit_keys:
            #soya.MAIN_LOOP.traveling.characters[0].doer.do_action(QuitMenuAction())
            soya.MAIN_LOOP.stop()
            
          elif event_key in self.screenshot_keys:
            import tempfile
            screenshot_file = tempfile.mktemp(".png")
            soya.screenshot(screenshot_file)
            print "* Balazar Brothers * Screenshot saved as %s" % screenshot_file
            
          elif event_key == sdlconst.K_LEFT:  self.camera_angle_speed    = -0.04; self.nb_camera_keys_pressed += 1.0
          elif event_key == sdlconst.K_RIGHT: self.camera_angle_speed    =  0.04; self.nb_camera_keys_pressed += 1.0
          elif event_key == sdlconst.K_UP:    self.camera_distance_speed = -1.20; self.nb_camera_keys_pressed += 1.0
          elif event_key == sdlconst.K_DOWN:  self.camera_distance_speed =  1.20; self.nb_camera_keys_pressed += 1.0
          
          elif event_key == sdlconst.K_d:
            print soya.MAIN_LOOP.traveling.characters
            print [i.uid for i in soya.MAIN_LOOP.traveling.characters]
            
            import time
            time.sleep(1.0)
          
      elif event_type == sdlconst.KEYUP:
        if not soya.MAIN_LOOP.entry:
          if   event_key in self.jump1_keys: soya.MAIN_LOOP.traveling.characters[ 0].events.append("j")
          if   event_key in self.jump2_keys: soya.MAIN_LOOP.traveling.characters[-1].events.append("j")

          elif event_key == sdlconst.K_LEFT:  self.camera_angle_speed    = 0.0
          elif event_key == sdlconst.K_RIGHT: self.camera_angle_speed    = 0.0
          elif event_key == sdlconst.K_UP:    self.camera_distance_speed = 0.0
          elif event_key == sdlconst.K_DOWN:  self.camera_distance_speed = 0.0
        
    # Camera control
    if self.nb_camera_keys_pressed > 2.0:
      # Reset camera
      self.nb_camera_keys_pressed = -4.0
      soya.MAIN_LOOP.traveling.custom_distance = 0.0
      soya.MAIN_LOOP.traveling.custom_angle    = 0.0
      self.camera_distance_speed = self.camera_angle_speed = 0.0
      
    elif self.nb_camera_keys_pressed < 0.0:
      self.nb_camera_keys_pressed += 0.1
      
    else:
      if self.nb_camera_keys_pressed > 0.1: self.nb_camera_keys_pressed -= 0.1
      soya.MAIN_LOOP.traveling.custom_distance += self.camera_distance_speed
      soya.MAIN_LOOP.traveling.custom_angle    += self.camera_angle_speed



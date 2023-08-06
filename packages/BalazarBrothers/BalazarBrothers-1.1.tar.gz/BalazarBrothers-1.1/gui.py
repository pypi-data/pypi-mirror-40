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

import sys, os, os.path, random, math

import soya.tofu as tofu
import soya, soya.opengl  as soyaopengl
import soya.sdlconst      as soyasdlconst
import soya.widget        as widget
import balazar_brothers
import balazar_brothers.globdef as globdef

COLOR     = (0.0, 0.0, 0.0, 1.0)
HIGHLIGHT = (0.0, 0.0, 1.0, 1.0)
COLOR     = (0.5, 0.5, 1.0, 1.0)
HIGHLIGHT = (1.0, 1.0, 1.0, 1.0)

def filter_string(s):
  return s.replace("\r", "").replace("\n", "")

class Rectangle(soya.widget.Widget):
  def __init__(self, master = None, color = (1.0, 1.0, 1.0, 0.8)):
    soya.widget.Widget.__init__(self, master)
    self.color = color
    self.visible = 1
    
  def render(self):
    if self.visible:
      if self.color[3] < 1.0: soyaopengl.glEnable(soyaopengl.GL_BLEND)
      soyaopengl.glColor4f (*self.color)
      soyaopengl.glBegin   (soyaopengl.GL_QUADS)
      soyaopengl.glVertex2f(self.left, self.top)
      soyaopengl.glVertex2f(self.left, self.top + self.height)
      soyaopengl.glVertex2f(self.left + self.width, self.top + self.height)
      soyaopengl.glVertex2f(self.left + self.width, self.top)
      soyaopengl.glEnd()
      if self.color[3] < 1.0: soyaopengl.glDisable(soyaopengl.GL_BLEND)


class MainMenuMainLoop(soya.MainLoop):
  def __init__ (self, mainmenu):
    soya.MainLoop.__init__ (self)
    self.mainmenu = mainmenu
    self.step     = 0
    
  def begin_round(self):
    soya.MainLoop.begin_round(self)
    if self.step == 0:
      for event in soya.process_event():
        self.mainmenu.set_current_menu(self.mainmenu.game_menu_1)
        self.step = 1
        break
    elif self.mainmenu.current_menu:
      for event in soya.process_event(): self.mainmenu.current_menu.process_event(event)


class MainMenu:
  def __init__(self):
    self.current_menu = None
    self.old_menus = []
    
    self.root = widget.Group()

    self.bg_img = soya.widget.Image(self.root, soya.Material.get('splash'))
    self.bg_img.resize_style  = ('maximize', 'center x', 'center y')
    self.bg_rect = Rectangle(self.root)
    self.bg_rect.resize_style = ('maximize', ('percent width', 0.6), ('margin bottom', 20), ('margin top', 20), ('margin left', 20))
    self.bg_rect.visible = 0
    
    self.scene = soya.World()
    
    self.atm = soya.NoBackgroundAtmosphere()
    self.atm.ambient  = (0.2, 0.2, 0.2, 1.0)
    self.scene.atmosphere = self.atm
    
    CHOICELIST_RESIZE_STYLE = ('maximize', ('percent width', 0.6), ('margin bottom', 20), ('margin top', 20), ('margin left', 20))
    self.game_menu_1 = soya.widget.ChoiceList(self.root, [
      soya.widget.Choice(_('Play'       ), self.show_solo),
      #soya.widget.Choice(_('Play multiplayer game'), self.show_multi),
      soya.widget.Choice(_('Hardware options'     ), self.show_h_option),
      soya.widget.Choice(_('Quit'                 ), self.go_back)
      ], None, COLOR, HIGHLIGHT, cancel = -1)
    self.game_menu_1.resize_style = CHOICELIST_RESIZE_STYLE
    self.game_menu_1.visible = 0
    
    checkbox = [_('off'), _('on')]
    
    self.menu_h_option = soya.widget.ChoiceList(self.root, [
      soya.widget.Choice(_('Resolution'), None, None, ['320x240', '640x480', '800x600', '1024x768', '1152x864', '1280x800', '1280x1024', '1400x1050', '1680x1050']),
      soya.widget.Choice(_('Fullscreen'), None, None, checkbox),
      soya.widget.Choice(_('Graphic quality'), None, None, [_('Low'), _('Medium'), _('High')]),
      soya.widget.Choice(_('Sound volume'), None, None, ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100']),
      soya.widget.ChoiceInput(_('Saved game directory')),
      soya.widget.Choice(_('Back'), self.back_h_option)
      ], None, COLOR, HIGHLIGHT, cancel = -1)
    self.menu_h_option.resize_style = CHOICELIST_RESIZE_STYLE
    self.menu_h_option.visible = 0
    
    self.label = widget.Group(self.root)
    self.label.visible = 0
    self.label.process_event = lambda event: self.menu_label.process_event(event)
    
    self.menu_label = soya.widget.ChoiceList(self.label, [
      soya.widget.Choice( u""     , None, None, [""]),
      soya.widget.Choice(_('Back'), self.go_back),
      ], None, COLOR, HIGHLIGHT, cancel = -1)
    self.menu_label.resize_style = CHOICELIST_RESIZE_STYLE
    
    
    self.solo = widget.Group(self.root)
    self.solo.visible = 0
    self.solo.process_event = lambda event: self.menu_solo.process_event(event)
    
    self.menu_solo = soya.widget.ChoiceList(self.solo, [
      soya.widget.Choice     (_('Start'), self.play_solo),
      soya.widget.ChoiceInput(_('Player name')),
      soya.widget.Choice     (_('Back'), self.go_back),
      ], None, COLOR, HIGHLIGHT, cancel = -1)
    self.menu_solo.resize_style = CHOICELIST_RESIZE_STYLE
    
    
    self.multi = widget.Group(self.root)
    self.multi.visible = 0
    self.multi.process_event = lambda event: self.menu_multi.process_event(event)
    
    self.menu_multi = soya.widget.ChoiceList(self.multi, [
      soya.widget.Choice     (_('Start'), self.play_multi),
      soya.widget.ChoiceInput(_('Player name')),
      soya.widget.ChoiceInput(_('Password')),
      soya.widget.ChoiceInput(_('Remote host or IP')),
      soya.widget.ChoiceInput(_('Connect to port')),
      soya.widget.Choice     (_('Back'), self.go_back),
      ], None, COLOR, HIGHLIGHT, cancel = -1)
    self.menu_multi.resize_style = CHOICELIST_RESIZE_STYLE
    
    #self.set_current_menu(self.game_menu_1)
    
    
  def set_current_menu(self, menu):
    if self.current_menu:
      self.current_menu.visible = 0
      self.old_menus.append(self.current_menu)
    self.current_menu = menu
    self.current_menu.visible = 1
    
  def go_back(self):
    if len(self.old_menus) == 0:
      globdef.generate_config_file()
      soya.MAIN_LOOP.stop()
      import sys
      sys.exit()
    if self.current_menu:
      self.current_menu.visible = 0
    self.current_menu = self.old_menus.pop()
    self.current_menu.visible = 1
    
  def show_h_option(self):
    self.menu_h_option.choices[0].value = str(globdef.SCREEN_WIDTH) + 'x' + str(globdef.SCREEN_HEIGHT)
    self.menu_h_option.choices[1].value = self.menu_h_option.choices[1].range[globdef.FULLSCREEN]
    self.menu_h_option.choices[2].value = self.menu_h_option.choices[2].range[globdef.QUALITY]
    #self.menu_h_option.choices[3].value = self.menu_h_option.choices[3].range[globdef.SOUND]
    self.menu_h_option.choices[3].value = str(int(round(globdef.SOUND_VOLUME * 100)))
    self.menu_h_option.choices[4].value = tofu.SAVED_GAME_DIR
    self.set_current_menu(self.menu_h_option)
    
  def back_h_option(self):
    resa = self.menu_h_option.choices[0].value
    globdef.SCREEN_WIDTH     = int(resa[: resa.find("x")])
    globdef.SCREEN_HEIGHT    = int(resa[resa.find("x") + 1:])
    globdef.FULLSCREEN       = (self.menu_h_option.choices[1].value == _('on'))
    globdef.QUALITY          = self.menu_h_option.choices[2].range.index(self.menu_h_option.choices[2].value)
    globdef.SOUND_VOLUME     = int(self.menu_h_option.choices[3].value) / 100.0
    tofu.SAVED_GAME_DIR  = self.menu_h_option.choices[4].value
    soya.set_quality(globdef.QUALITY)
    soya.set_video(globdef.SCREEN_WIDTH, globdef.SCREEN_HEIGHT, globdef.FULLSCREEN, 1)
    soya.set_sound_volume(globdef.SOUND_VOLUME)
    self.go_back()
    
  def show_solo(self):
    self.menu_solo.choices[1].value = globdef.LOGIN
    self.set_current_menu(self.solo)
    
  def play_solo(self):
    main_loop = soya.MAIN_LOOP
    login = globdef.LOGIN = filter_string(self.menu_solo.choices[1].value)
    tofu.PLAYER_IDS = [tofu.PlayerID(login, "test")]
    tofu.GAME = login
    tofu.set_side("single")
    try:
      r = balazar_brothers.main_loop.MainLoop().main_loop()
    except:
      error, value, traceback = sys.exc_info()
      sys.excepthook(error, value, traceback)
      r = "%s(%s)" % (error, value)
      
    soya.set_root_widget(self.root)
    main_loop.reset()
    soya.MAIN_LOOP = main_loop
    
    if r: self.message("Error: " + str(r))
    
  def show_multi(self):
    self.menu_multi.choices[1].value = globdef.LOGIN
    self.menu_multi.choices[2].value = ""
    self.menu_multi.choices[3].value = tofu.HOST
    self.menu_multi.choices[4].value = str(tofu.PORT)
    self.set_current_menu(self.multi)
    
  def play_multi(self):
    main_loop = soya.MAIN_LOOP
    tofu.PLAYER_IDS = [
      tofu.PlayerID(
      filter_string(self.menu_multi.choices[1].value),
      filter_string(self.menu_multi.choices[2].value),
      )]
    tofu.HOST     = filter_string(self.menu_multi.choices[3].value)
    tofu.PORT     = int          (self.menu_multi.choices[4].value)
    tofu.set_side("client")
    try:
      r = balazar_brothers.main_loop.MainLoop().main_loop()
    except:
      error, value, traceback = sys.exc_info()
      sys.excepthook(error, value, traceback)
      r = u"%s(%s)" % (error, value)
      
    soya.set_root_widget(self.root)
    main_loop.reset()
    soya.MAIN_LOOP = main_loop
    
    if r:
      if r != "Connection was closed cleanly.": # Server close the connection, because the player is dead
        r = str(r)
        if "111" in r: r = r + u"\n\n" + _("__have_you_forget_the_server_?__")
        self.message(u"Error: " + r)
        
  def message(self, text):
    self.menu_label.choices[0].label = text
    self.set_current_menu(self.label)
    


  def run (self):
    soya.set_root_widget(self.root)
    self.main_loop = MainMenuMainLoop(self)
    action = self.main_loop.main_loop()
  










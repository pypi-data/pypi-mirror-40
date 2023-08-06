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

import cerealizer, soya, soya.cerealizer4soya, soya.tofu as tofu, balazar_brothers

import balazar_brothers.globdef as globdef
from balazar_brothers.character import Character, Balazar
from balazar_brothers.platform_  import Platform, BasePlatform, PortailPlatform

def level_display_name(level_name):
  x = level_name.rfind("_")
  return _(level_name[:x]) + " " + level_name[x + 1:]

MUSICS = {
  "tutorial"         : "pompon.ogg",
  "pompon_forest"    : "pompon.ogg",
  "coqueliform_field": "oceane.ogg",
  }

class Level(tofu.Level):
  def __init__(self):
    tofu.Level.__init__(self)
    
    self.center      = soya.Point(self)
    self.static_part = soya.World(self)
    self.platforms   = {}
    
    self.hour       = 8.0
    self.weather    = "sun"
    
  def get_country_name(self): return self.filename[:self.filename.rfind("_")]

  @tofu.side("single", "client")
  def set_active(self, active):
    old_active = self.active
    
    tofu.Level.set_active(self, active)
    
    if active and not old_active:
      soya.MAIN_LOOP.scenes[0].atmosphere.set_time_and_weather(self.hour, self.weather)
      soya.MAIN_LOOP.scenes[0].children.remove(soya.MAIN_LOOP.camera)
      soya.MAIN_LOOP.scenes[0].children.append(soya.MAIN_LOOP.camera)
      
      soya.MAIN_LOOP.level_label.text = level_display_name(self.filename).replace("\n", " ")
      
      music_filename = MUSICS.get(self.get_country_name(), "oceane.ogg")[:-4] + ".wav"
      if (not soya.MAIN_LOOP.music) or (soya.MAIN_LOOP.music.sound.filename != music_filename):
        if soya.MAIN_LOOP.music: soya.MAIN_LOOP.scenes[0].remove(soya.MAIN_LOOP.music)
        soya.MAIN_LOOP.music = soya.SoundPlayer(soya.MAIN_LOOP.scenes[0], soya.Sound.get(music_filename), loop = 1, play_in_3D = 0)
        
  def begin_round(self):
    tofu.Level.begin_round(self)
    
  def advance_time(self, proportion):
    tofu.Level.advance_time(self, proportion)
    
  def add_mobile(self, mobile, _send_later = 0):
    tofu.Level.add_mobile(self, mobile, _send_later)
    
    if isinstance(mobile, BasePlatform):
      mobile.platid = max([0] + [platform.platid for platform in self.mobiles if isinstance(platform, BasePlatform)]) + 1
      self.platforms[mobile.platid] = mobile
      
    if isinstance(mobile, Character):
      if mobile.platform and (not mobile in mobile.platform.characters_on):
        mobile.platform.add_character(mobile, 0)
        
  def remove_mobile(self, mobile):
    if isinstance(mobile, BasePlatform):
      del self.platforms[mobile.platid]
      
    if isinstance(mobile, Character):
      #if mobile.platform and not (isinstance(mobile.platform, Character) and mobile.player_name == mobile.platform.player_name):
      if mobile.platform:
        mobile.platform.remove_character(mobile)
        
        for character_on in mobile.characters_on:
          mobile.remove_character(character_on)
          character_on.set_platform(mobile.platform)
          
    tofu.Level.remove_mobile(self, mobile)
    
  def add_or_add_mobile(self, o):
    if isinstance(o, tofu.Mobile): self.add_mobile(o)
    else: self.add(o)
    
  def del_or_del_mobile(self, i):
    o = self.children[i]
    if isinstance(o, tofu.Mobile): self.remove_mobile(o)
    else: del self[i]
    
  def get_by_class(self, Class):
    for i in self:
      if isinstance(i, Class): return i

  def get_all_by_class(self, Class):
    return [i for i in self if isinstance(i, Class)]
      
  def build_ended(self):
    self.center.set_xyz(0.0, 0.0, 0.0)
    
    nb = 0
    for platform in self.mobiles:
      if isinstance(platform, Platform):
        nb += 1
        self.center.add_xyz(platform.x, platform.y, platform.z)

    if nb:
      self.center.x /= nb
      self.center.y /= nb
      self.center.z /= nb
      
    for i in self.recursive():
      if isinstance(i, soya.Terrain): i.reinit()
  
  def random_terrain(self):
    from balazar_brothers.terrain_gen import random_terrain
    
    for terrain in self.recursive():
      if isinstance(terrain, soya.Terrain): terrain.parent.remove(terrain)
    
    if self.filename.startswith("coqueliform_field"):
      terrain = random_terrain(self)
      terrain.set_xyz(-32.0 * 1.25, -30.0, -32.0 * 1.25)
    elif self.filename.startswith("fountain_river"):
      terrain = random_terrain(self, default_min_y = 0.45, default_max_y = 0.5, nb_hole = 0.5, pic_proba = 0.8, plateau_proba = 0.0, colline_proba = 0.1, cratere1_proba = 0.0, cratere2_proba = 0.0, monticule_proba = 0.0, termitiere_proba = 0.0)
      terrain.set_xyz(-32.0 * 1.25, -30.0, -32.0 * 1.25)
      terrain.multiply_height(30.0 / 50.0)
      self.create_surface()
    elif self.filename.startswith("pompon_forest"):
      terrain = random_terrain(self, default_max_y = 0.25, pic_proba = 0.3, plateau_proba = 0.6, colline_proba = 0.2, cratere1_proba = 0.7, cratere2_proba = 0.7, monticule_proba = 0.8, termitiere_proba = 0.4)
      terrain.set_xyz(-32.0 * 1.25, -30.0, -32.0 * 1.25)
    elif self.filename.startswith("hopeless_castle"):
      terrain = random_terrain(self, default_max_y = 0.27, pic_proba = 0.0, plateau_proba = 0.8, colline_proba = 0.5, cratere1_proba = 0.5, cratere2_proba = 0.5, monticule_proba = 0.2, termitiere_proba = 0.2)
      terrain.set_xyz(-32.0 * 1.25, -30.0, -32.0 * 1.25)
    else:
      terrain = random_terrain(self, default_max_y = 0.27, pic_proba = 0.0, plateau_proba = 0.8, colline_proba = 0.5, cratere1_proba = 0.5, cratere2_proba = 0.5, monticule_proba = 0.0, termitiere_proba = 0.0)
      terrain.set_xyz(-32.0 * 1.25, -30.0, -32.0 * 1.25)
      
    self.set_terrain_material()
    
  def set_terrain_material(self):
    for terrain in self.recursive():
      if isinstance(terrain, soya.Terrain): break
    else: return
    
    if self.filename.startswith("coqueliform_field"):
      terrain.set_material_layer(soya.Material.get("grass"              ), 0.0  * 50.0, 0.24 * 50.0)
      terrain.set_material_layer(soya.Material.get("coqueliformes_champ"), 0.24 * 50.0, 0.54 * 50.0)
      terrain.set_material_layer(soya.Material.get("snow"               ), 0.54 * 50.0, 0.6  * 50.0)
      terrain.set_material_layer(soya.Material.get("ice"                ), 0.6  * 50.0, 1.0  * 50.0)
    elif self.filename.startswith("fountain_river"):
      terrain.set_material_layer(soya.Material.get("nacre"   ), 0.0  * 50.0, 0.3 * 50.0)
      terrain.set_material_layer(soya.Material.get("nacre2"  ), 0.23 * 50.0, 1.0 * 50.0)
      terrain.set_material_layer(soya.Material.get("grass6"  ), 0.3  * 50.0, 1.0 * 50.0)
      terrain.set_material_layer(soya.Material.get("grass"   ), 0.6  * 50.0, 1.0 * 50.0)
    elif self.filename.startswith("pompon_forest"):
      terrain.set_material_layer(soya.Material.get("feuillesmortes2"), 0.0  * 50.0, 0.26 * 50.0)
      terrain.set_material_layer(soya.Material.get("feuillesmortes3"), 0.26 * 50.0, 0.3 * 50.0)
      terrain.set_material_layer(soya.Material.get("grass"          ), 0.3  * 50.0, 0.5 * 50.0)
      terrain.set_material_layer(soya.Material.get("grass3"         ), 0.5  * 50.0, 1.0 * 50.0)
    elif self.filename.startswith("hopeless_castle"):
      terrain.set_material_layer(soya.Material.get("feuillesmortes"), 0.0  * 50.0, 0.26 * 50.0)
      terrain.set_material_layer(soya.Material.get("snow"          ), 0.26 * 50.0, 0.6  * 50.0)
      terrain.set_material_layer(soya.Material.get("ice"           ), 0.6  * 50.0, 1.0  * 50.0)
    else:
      terrain.set_material_layer(soya.Material.get("feuillesmortes"), 0.0   * 50.0, 0.28 * 50.0)
      terrain.set_material_layer(soya.Material.get("grass2"        ), 0.28  * 50.0, 0.4  * 50.0)
      terrain.set_material_layer(soya.Material.get("grass"         ), 0.4   * 50.0, 1.0  * 50.0)
      
  def set_terrain_holes(self):
    for terrain in self.recursive():
      if isinstance(terrain, soya.Terrain): break
    else: return
    
    for x in range(terrain.width):
      for z in range(terrain.depth):
        if terrain.get_height(x, z) == 0.0:
          terrain.set_vertex_option(x, z, 1, 1)
          
  def create_surface(self, y = -20.0, nb_step = 16):
    from balazar_brothers.terrain_gen import TERRAIN_SCALE
    
    for terrain in self.recursive():
      if isinstance(terrain, soya.Terrain): break
    else: return
    
    terrain.set_material_layer(soya.Material.get("nacre"   ), 0.0  * 30.0, 1.0 * 30.0)
    terrain.set_material_layer(soya.Material.get("grass6"  ), 0.30 * 30.0, 1.0 * 30.0)
    terrain.set_material_layer(soya.Material.get("grass"   ), 0.60 * 30.0, 1.0 * 30.0)
    
    directions = [
      soya.Vector(self.static_part, -1.0, 0.0,  0.0),
      soya.Vector(self.static_part,  1.0, 0.0,  0.0),
      soya.Vector(self.static_part,  0.0, 0.0, -1.0),
      soya.Vector(self.static_part,  0.0, 0.0,  1.0),
      ]
    
    surface = soya.World()
    
    insides  = {}
    outsides = {}
    for i in range(nb_step):
      for j in range(nb_step):
        x = (float(i) / nb_step) * 33.0 * TERRAIN_SCALE + terrain.x
        z = (float(j) / nb_step) * 33.0 * TERRAIN_SCALE + terrain.z
        origin = soya.Point(self.static_part, x, y, z)
        nb = 0
        for direction in directions:
          if self.static_part.raypick_b(origin, direction): nb += 1
        if nb >= 4: insides[(i, j)] = 1
        else:       insides[(i, j)] = 0
        
        for direction in directions:
          if self.static_part.raypick_b(origin, direction, cull_face = 0): nb += 1
        if nb >= 4: outsides[(i, j)] = 0
        else:       outsides[(i, j)] = 1
        
    for i in range(nb_step - 1):
      for j in range(nb_step - 1):
        if insides[i, j] or insides[i + 1, j] or insides[i, j + 1] or insides[i + 1, j + 1]:
          if outsides[i, j] or outsides[i + 1, j] or outsides[i, j + 1] or outsides[i + 1, j + 1]:
            continue
          
          x1 = (float(i    ) / nb_step) * 33.0 * TERRAIN_SCALE + terrain.x
          z1 = (float(j    ) / nb_step) * 33.0 * TERRAIN_SCALE + terrain.z
          x2 = (float(i + 1) / nb_step) * 33.0 * TERRAIN_SCALE + terrain.x
          z2 = (float(j + 1) / nb_step) * 33.0 * TERRAIN_SCALE + terrain.z
          
          soya.Face(surface, [
            soya.Vertex(surface, x1, y, z2, tex_x = 0.0, tex_y = 1.0),
            soya.Vertex(surface, x2, y, z2, tex_x = 1.0, tex_y = 1.0),
            soya.Vertex(surface, x2, y, z1, tex_x = 1.0, tex_y = 0.0),
            soya.Vertex(surface, x1, y, z1, tex_x = 0.0, tex_y = 0.0),
            ], soya.Material.get("eau"))
          
    if getattr(self, "surface", None): self.surface.parent.remove(self.surface)
    self.surface = soya.Volume(self.static_part, surface.to_model())
    
  def save(self):
    if tofu.has_side("level_editor"): # Hack !!!
      self.build_ended()
      
    tofu.Level.save(self)
    
  
cerealizer.register(Level, soya.cerealizer4soya.SavedInAPathHandler(Level))



def create_demo_level():
  if Level._alls.has_key("demo_1"): return Level._alls["demo_1"]
  
  print "Create level demo_1..."
  
  level = Level()
  level.filename = "demo_1"
  
  from soya import Point, Vector
  from balazar_brothers.platform import PortailPlatform, StartingPlatform, Coqueliform, RotatingCoqueliform
  from balazar_brothers.terrain_gen import random_terrain
  
  def create(Class, position = None, front = None, **kargs):
    p = Class(**kargs)
    level.add_mobile(p)
    if position: p.move(position)
    if front   : p.look_at(front)
    return p
  
  
  p = create(StartingPlatform, Point(None,  0.0, 0.0,  0.0))
  p = create(Coqueliform     , Point(None,  1.0, 0.0, -4.0))
  
  p = create(Coqueliform     , Point(None, -1.0, 0.0, -8.0))
  #p = create(PortailPlatform     , Point(None, -1.0, 0.0, -8.0), next_level_name = "demo_2"); p.rotate_lateral(20.0)
  
  p = create(RotatingCoqueliform, Point(None, -4.0, 0.0, -10.0))
  p = create(Coqueliform     , Point(None, -6.5, 1.0, -11.0))
  p = create(Coqueliform     , Point(None, -10.0, 2.0, -11.5))
  p = create(Coqueliform     , Point(None, -14.0, 2.5, -11.0))
  p = create(Coqueliform     , Point(None, -17.0, 3.0, -9.5))
  p = create(Coqueliform     , Point(None, -18.0, 3.0, -7.0))
  p = create(Coqueliform     , Point(None, -18.5, 3.2, -4.0))
  p = create(Coqueliform     , Point(None, -18.0, 3.5, -1.0))
  p = create(Coqueliform     , Point(None, -17.0, 3.5,  1.0))
  p = create(Coqueliform     , Point(None, -14.5, 3.7,  2.0))
  p = create(Coqueliform     , Point(None, -12.0, 0.0,  3.0))
  p = create(Coqueliform     , Point(None, -8.5, 0.0,  3.5))
  p = create(Coqueliform     , Point(None, -4.5, 0.0,  2.5))
  p = create(Coqueliform     , Point(None, -2.0, 0.0,  1.5))

  level.weather = "sun"
  level.hour    = 8.0
  
  terrain = random_terrain(level)
  terrain.x = -50.0
  terrain.z = -50.0
  
  #terrain.set_material_layer(soya.Material.get("grass2"), 0.0  * 50.0, 0.24 * 50.0)
  terrain.set_material_layer(soya.Material.get("grass"), 0.0  * 50.0, 0.24 * 50.0)
  terrain.set_material_layer(soya.Material.get("coqueliformes_champ" ), 0.24 * 50.0, 0.54 * 50.0)
  terrain.set_material_layer(soya.Material.get("snow"  ), 0.54 * 50.0, 0.6  * 50.0)
  terrain.set_material_layer(soya.Material.get("ice"   ), 0.6  * 50.0, 1.0  * 50.0)
  
  
  level.build_ended()
  return level



def create_demo_level2():
  if Level._alls.has_key("demo_2"): return Level._alls["demo_2"]
  
  print "Create level demo_2..."
  
  level = Level()
  level.filename = "demo_2"
  
  from soya import Point, Vector
  from balazar_brothers.platform import PortailPlatform, StartingPlatform, Coqueliform, RotatingCoqueliform
  from balazar_brothers.bonus    import SmallChest, BigChest
  from balazar_brothers.terrain_gen import random_terrain
  
  def create(Class, position = None, front = None, **kargs):
    p = Class(**kargs)
    level.add_mobile(p)
    if position: p.move(position)
    if front   : p.look_at(front)
    return p
  
  p = create(PortailPlatform , Point(None,  0.0, -5.0,  0.0), next_level_name = "demo_1")
  p = create(Coqueliform     , Point(None,  1.0, -5.0, -4.0))
  p = create(Coqueliform     , Point(None, -1.0, -5.0, -8.0))
  p = create(RotatingCoqueliform, Point(None, -4.0, -5.0, -10.0))
  
  p = create(BigChest, Point(None,  -1.0, -4.0, -8.0))
  
  level.weather = "sun"
  level.hour    = 17.0
  
  terrain = random_terrain(level)
  terrain.x = -50.0
  terrain.z = -50.0
  
  #terrain.set_material_layer(soya.Material.get("grass2"), 0.0  * 50.0, 0.24 * 50.0)
  terrain.set_material_layer(soya.Material.get("grass"), 0.0  * 50.0, 0.24 * 50.0)
  terrain.set_material_layer(soya.Material.get("coqueliformes_champ" ), 0.24 * 50.0, 0.54 * 50.0)
  terrain.set_material_layer(soya.Material.get("snow"  ), 0.54 * 50.0, 0.6  * 50.0)
  terrain.set_material_layer(soya.Material.get("ice"   ), 0.6  * 50.0, 1.0  * 50.0)
  
  level.build_ended()
  return level

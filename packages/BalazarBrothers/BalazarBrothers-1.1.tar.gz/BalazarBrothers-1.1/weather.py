# Balazar Brothers
# Copyright (C) 2002-2007 Jean-Baptiste LAMY
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

import bisect, random
import cerealizer, soya, soya.opengl as soyaopengl, soya.widget as widget
import soya.spc_material
import balazar_brothers

class SunSprite(soya.Sprite):
  def __init__(self, parent = None):
    soya.Sprite.__init__(self, parent, soya.Material.get("sun"))
    self.color = (1.0, 0.7, 0.5, 1.0)
    self.width = self.height = 20.0
cerealizer.register(SunSprite)

class StarSprite(soya.Sprite):
  def __init__(self, parent = None):
    soya.Sprite.__init__(self, parent, soya.Material.get("star"))
cerealizer.register(StarSprite)
  


#cloud = soya.spc_material.MovingMaterial(soya.Image.get("cloud2.png"), 0.0001, 0.0002)
#cloud.filename = "cloud2"
#cloud.save()

class WeatherAtmosphere(soya.SkyAtmosphere):
  def __init__(self, parent = None):
    soya.SkyAtmosphere.__init__(self)
    self.fog         = 1
    self.fog_type    = 0
    self.skyplane    = 1
    self.cloud       = soya.Material.get("cloud2")
    self.cloud_scale = 0.2
    
    self.time             = 0.0 # In hour
    self.weather          = "sun"
    
    if parent:
      self.sun = soya.Light(parent)
      self.sun.directional  = 1
      self.sun.cast_shadow  = 1
      self.sun.shadow_color = (0.0, 0.0, 0.0, 0.5)
      
      self.astral_world = soya.World(parent)
      self.astral_world.atmosphere = soya.SkyAtmosphere()
      self.astral_world.atmosphere.ambient = (1.0, 1.0, 1.0, 1.0)
      
      a = 90.0
      self.sun.rotate_vertical(a)
      self.astral_world.rotate_vertical(a)
      
      self.sun_sprite = SunSprite(self.astral_world)
      self.sun_sprite.z = 90.0
      
      for i in range(50):
        star = StarSprite(self.astral_world)
        star.color = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), 1.0)
        star.size = star.width = star.height = random.uniform(0.5, 5.0)
        
        star.x = random.uniform(-90.0,  90.0)
        star.y = random.uniform(-90.0,  90.0)
        star.z = random.uniform(-90.0,  90.0)
        l = self.astral_world.distance_to(star) / 99.0
        star.x /= l
        star.y /= l
        star.z /= l
        
  def set_time_and_weather(self, time, weather = "sun"):
    if   self.weather == "rain":
      if soya.MAIN_LOOP: soya.root_widget.remove(RAIN) # 0 is camera
    elif self.weather == "snow":
      if soya.MAIN_LOOP: soya.root_widget.remove(SNOW) # 0 is camera
      
    dtime = time - self.time
    self.time    = time
    self.weather = weather
    
    if   weather == "rain":
      self.astral_world.visible = 0
      if soya.MAIN_LOOP: soya.root_widget.insert(1, RAIN) # 0 is camera
    elif weather == "snow":
      self.astral_world.visible = 1
      if soya.MAIN_LOOP: soya.root_widget.insert(1, SNOW) # 0 is camera
    else:
      self.astral_world.visible = 1
      
    a = dtime / 24.0 * 360.0
    self.sun.rotate_vertical(a)
    #self.astral_world.rotate_vertical(0)
    
    data = DAY_NIGHT_DATA[self.weather]
    right = bisect.bisect(data, (self.time,))
    
    d1 = data[right - 1]
    d2 = data[right]
    
    if d1[0] < d2[0]: f2 = (self.time - d1[0]) / (d2[0] - d1[0])
    else:             f2 = (24.0 + self.time - d1[0]) / (24.0 + d2[0] - d1[0])
    f1 = 1.0 - f2
    
    self.fog_start   = f1 * d1[1] + f2 * d2[1]
    self.fog_end     = (f1 * d1[2] + f2 * d2[2])
    self.fog_color   = self.bg_color = (f1 * d1[ 3] + f2 * d2[ 3], f1 * d1[ 4] + f2 * d2[ 4], f1 * d1[ 5] + f2 * d2[ 5], 1.0)
    self.sky_color   =                 (f1 * d1[ 6] + f2 * d2[ 6], f1 * d1[ 7] + f2 * d2[ 7], f1 * d1[ 8] + f2 * d2[ 8], 1.0)
    self.ambient     =                 (f1 * d1[ 9] + f2 * d2[ 9], f1 * d1[10] + f2 * d2[10], f1 * d1[11] + f2 * d2[11], 1.0)
    self.sun.diffuse =                 (f1 * d1[12] + f2 * d2[12], f1 * d1[13] + f2 * d2[13], f1 * d1[14] + f2 * d2[14], 1.0)
    
      
  def begin_round(self): pass
  
  def advance_time(self, proportion):
    if soya.MAIN_LOOP:
      self.astral_world.move(soya.MAIN_LOOP.camera)
      
  def destroy(self):
    if soya.MAIN_LOOP:
      if RAIN.master: RAIN.master.remove(RAIN)
      if SNOW.master: SNOW.master.remove(SNOW)
cerealizer.register(WeatherAtmosphere)
      
      
class Rain(widget.Widget):
  def __init__(self, parent = None):
    self.w = 640
    self.h = 480
    self.next_thunder = 10
    self.particles = [[random.uniform(0.0, self.w), random.uniform(-20.0, self.h), random.uniform(15.0, 50.0), random.uniform(0.5, 1.0)] for i in range(30)]
    
    widget.Widget.__init__(self, parent)
    
  def __getstate__(self): return None
  def __setstate__(self, state): pass
    
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    w = soya.get_screen_width()
    h = soya.get_screen_height()
    fw = float(w) / self.w
    fh = float(h) / self.h
    self.w = w
    self.h = h
    
    for p in self.particles:
      p[0] *= fw
      p[1] *= fh
      p[2] *= fh
      
  def render(self):
    f = soya.MAIN_LOOP.scenes[0].transform_vector(1.0, 0.0, 0.0, soya.MAIN_LOOP.camera)[0] / 2.0
    
    soya.DEFAULT_MATERIAL.activate()
    soyaopengl.glLineWidth(2.0)
    soyaopengl.glBegin(soyaopengl.GL_TRIANGLES)
    for p in self.particles:
      if p[1] > 0.6 * self.h + p[2] * 2.5: p[1] = 0.0
      if   p[0] > self.w: p[0] -= self.w
      elif p[0] < 0.0:    p[0] += self.w
      
      soyaopengl.glColor4f(p[3], 0.8, 1.0, 1.0)
      soyaopengl.glVertex2f(p[0], p[1])
      p[0] += p[2] *  f
      p[1] += p[2]
      soyaopengl.glVertex2f(p[0], p[1])
      soyaopengl.glVertex2f(p[0] + 3, p[1])
      p[0] -= p[2] * 0.5 * f
      p[1] -= p[2] * 0.5
      
    soyaopengl.glEnd()
    
    self.next_thunder -= 1
    if   self.next_thunder == 0:
      weather_atmosphere = soya.MAIN_LOOP.scenes[0].atmosphere
      weather_atmosphere.old_data = weather_atmosphere.fog_color, weather_atmosphere.bg_color, weather_atmosphere.sky_color, weather_atmosphere.fog_start
      weather_atmosphere.fog_color = (1.0, 1.0, 1.0, 1.0)
      weather_atmosphere.bg_color  = weather_atmosphere.sky_color = (1.0, 1.0, 1.0, 1.0)
      weather_atmosphere.fog_start = -20.0
      
    elif self.next_thunder <= -10:
      weather_atmosphere = soya.MAIN_LOOP.scenes[0].atmosphere
      if hasattr(weather_atmosphere, "old_data"):
        weather_atmosphere.fog_color, weather_atmosphere.bg_color, weather_atmosphere.sky_color, weather_atmosphere.fog_start = weather_atmosphere.old_data
      self.next_thunder = random.randint(50, 200)
      
    
    
class Snow(widget.Widget):
  def __init__(self, parent = None):
    widget.Widget.__init__(self, parent)
    self.w = 640
    self.h = 480
    
    self.particles = [[random.uniform(0.0, self.w), 0.0, random.uniform(20.0, 50.0), random.uniform(0.5, 1.0)] for i in range(15)]
    self.old_cam_x = 0.0
    self.old_cam_y = 0.0
    
    self.material = soya.Material.get("star")
    
  def __getstate__(self): return None
  def __setstate__(self, state): pass
  
  def resize(self, parent_left, parent_top, parent_width, parent_height):
    w = soya.get_screen_width()
    h = soya.get_screen_height()
    fw = float(w) / self.w
    fh = float(h) / self.h
    self.w = w
    self.h = h
    
    for p in self.particles:
      p[0] *= fw
      p[1] *= fh
      
    self.v1 = soya.Vector(soya.MAIN_LOOP.scenes[0], 0.0, 0.0, -1.0)
    self.v2 = soya.Vector(soya.MAIN_LOOP.camera, 0.0, 0.0, -1.0)
    
  def render(self):
    if not hasattr(self, "v1"): return
    
    a = self.v1.angle_to(self.v2)
    if self.v1.cross_product(self.v2).y < 0.0: delta_x = (self.old_cam_x - a) * self.w * 0.5
    else:                                      delta_x = (a - self.old_cam_x) * self.w * 0.5
    self.old_cam_x = a
    
    delta_y = (soya.MAIN_LOOP.camera.y - self.old_cam_y) * self.h * 0.1
    self.old_cam_y = soya.MAIN_LOOP.camera.y
    
    self.material.activate()
    soyaopengl.glEnable(soyaopengl.GL_BLEND)
    soyaopengl.glPointSize(20.0)
    soyaopengl.glBegin(soyaopengl.GL_QUADS)
    for p in self.particles:
      if   p[1] > self.h - 35: p[1] -= self.h
      elif p[1] < - 35: p[1] += self.h
      if   p[0] < 0.0: p[0] += self.w
      elif p[0] > self.w: p[0] -= self.w
      
      soyaopengl.glColor4f(0.5, 0.3, 1.0, 1.0)
      soyaopengl.glTexCoord2f(0.0, 0.0); soyaopengl.glVertex2f(p[0], p[1])
      soyaopengl.glTexCoord2f(1.0, 0.0); soyaopengl.glVertex2f(p[0], p[1] + p[2])
      soyaopengl.glTexCoord2f(1.0, 1.0); soyaopengl.glVertex2f(p[0] + p[2], p[1] + p[2])
      soyaopengl.glTexCoord2f(0.0, 1.0); soyaopengl.glVertex2f(p[0] + p[2], p[1])
      p[0] += delta_x / p[2]
      p[1] += p[2] * (0.1 + 0.02 * delta_y)
      
    soyaopengl.glEnd()
    soya.DEFAULT_MATERIAL.activate()
    
      
SNOW = Snow()
RAIN = Rain()


DAY_NIGHT_DATA = {
  "sun" : [
  (4.0, # Time
   0.0, 70.0, # Fog distance
   0.0, 0.0, 0.0, # Fog color
   0.0, 0.3, 1.0, # Sky color
   0.15, 0.15, 0.3, # Ambient
   0.3, 0.3, 0.5, # Sun diffuse color
   ),
  (8.0, # Time
   20.0, 80.0, # Fog distance
   0.4, 0.45, 0.7, # Fog color
   1.5, 1.0, 0.8, # Sky color
   0.3, 0.3, 0.4, # Ambient
   1.0, 0.8, 0.4, # Sun diffuse color
   ),
  (12.0, # Time
   50.0, 100.0, # Fog distance
   0.2, 0.5, 0.7, # Fog color
   2.0, 2.0, 2.0, # Sky color
   0.4, 0.4, 0.4, # Ambient
   0.9, 0.9, 0.7, # Sun diffuse color
   ),
  (16.0, # Time
   40.0, 95.0, # Fog distance
   0.45, 0.6, 1.0, # Fog color
   0.0, 0.0, 1.0, # Sky color
   0.3, 0.3, 0.4, # Ambient
   0.7, 0.7, 0.5, # Sun diffuse color
   ),
   (19.0, # Time
   30.0, 80.0, # Fog distance
   0.3, 0.0, 0.6, # Fog color
   1.5, 1.2, 0.2, # Sky color
   0.2, 0.2, 0.6, # Ambient
   0.7, 0.7, 0.5, # Sun diffuse color
   ),
   (24.0, # Time -- This one is MANDATORY !!!
   5.0, 70.0, # Fog distance
   0.0, 0.0, 0.0, # Fog color
   0.2, 0.0, 1.0, # Sky color
   0.15, 0.15, 0.4, # Ambient
   0.3, 0.3, 0.5, # Sun diffuse color
   ),
 ],
  "rain" : [
  (4.0, # Time
   0.0, 65.0, # Fog distance
   0.0, 0.0, 0.0, # Fog color
   0.2, 0.3, 0.5, # Sky color
   0.15, 0.15, 0.2, # Ambient
   0.2, 0.2, 0.3, # Sun diffuse color
   ),
  (8.0, # Time
   5.0, 70.0, # Fog distance
   0.4, 0.45, 0.5, # Fog color
   0.2, 0.2, 0.3, # Sky color
   0.3, 0.3, 0.3, # Ambient
   0.6, 0.4, 0.3, # Sun diffuse color
   ),
  (12.0, # Time
   25.0, 95.0, # Fog distance
   0.4, 0.5, 0.6, # Fog color
   0.3, 0.3, 0.3, # Sky color
   0.3, 0.3, 0.3, # Ambient
   0.5, 0.5, 0.5, # Sun diffuse color
   ),
  (16.0, # Time
   25.0, 90.0, # Fog distance
   0.4, 0.4, 0.6, # Fog color
   0.2, 0.2, 0.4, # Sky color
   0.3, 0.3, 0.3, # Ambient
   0.4, 0.4, 0.4, # Sun diffuse color
   ),
   (19.0, # Time
   15.0, 80.0, # Fog distance
   0.4, 0.3, 0.5, # Fog color
   0.4, 0.3, 0.2, # Sky color
   0.2, 0.2, 0.3, # Ambient
   0.3, 0.3, 0.2, # Sun diffuse color
   ),
   (24.0, # Time -- This one is MANDATORY !!!
   0.0, 65.0, # Fog distance
   0.0, 0.0, 0.0, # Fog color
   0.2, 0.2, 0.8, # Sky color
   0.15, 0.15, 0.3, # Ambient
   0.2, 0.2, 0.3, # Sun diffuse color
   ),
  ],
  "snow" : [
  (4.0, # Time
   0.0, 70.0, # Fog distance
   0.0, 0.0, 0.0, # Fog color
   0.6, 0.0, 0.4, # Sky color
   0.15, 0.15, 0.3, # Ambient
   0.3, 0.2, 0.3, # Sun diffuse color
   ),
  (8.0, # Time
   0.0, 80.0, # Fog distance
   0.6, 0.5, 0.7, # Fog color
   1.5, 1.0, 0.8, # Sky color
   0.3, 0.3, 0.4, # Ambient
   0.5, 0.4, 0.3, # Sun diffuse color
   ),
  (12.0, # Time
   5.0, 100.0, # Fog distance
   0.5, 0.7, 0.7, # Fog color
   2.0, 2.0, 2.0, # Sky color
   0.4, 0.4, 0.4, # Ambient
   0.6, 0.6, 0.4, # Sun diffuse color
   ),
  (16.0, # Time
   3.0, 95.0, # Fog distance
   0.5, 0.8, 0.8, # Fog color
   0.0, 0.0, 1.0, # Sky color
   0.3, 0.3, 0.4, # Ambient
   0.4, 0.4, 0.2, # Sun diffuse color
   ),
   (19.0, # Time
   0.0, 80.0, # Fog distance
   0.3, 0.2, 0.6, # Fog color
   1.5, 1.2, 0.7, # Sky color
   0.2, 0.2, 0.6, # Ambient
   0.4, 0.4, 0.2, # Sun diffuse color
   ),
   (24.0, # Time -- This one is MANDATORY !!!
   0.0, 70.0, # Fog distance
   0.0, 0.0, 0.0, # Fog color
   0.4, 0.0, 0.3, # Sky color
   0.15, 0.15, 0.4, # Ambient
   0.3, 0.2, 0.3, # Sun diffuse color
   ),
  ],
  }




# -*- coding: latin-1 -*-
# Balazar Brothers
# Copyright (C) 2003-2007 Jean-Baptiste LAMY
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

import random, math
import soya

import balazar_brothers


TERRAIN_SIZE  = 33
TERRAIN_SCALE = 2.5
TERRAIN_DIM   = TERRAIN_SCALE * TERRAIN_SIZE

    
def random_terrain(level,
                default_min_y = 0.18, default_max_y = 0.23,
                nb_max = 0.0015, nb_hole = 0.0,
                pic_proba = 0.1, plateau_proba = 0.25, colline_proba = 0.25, cratere1_proba = 0.1, cratere2_proba = 0.1, monticule_proba = 0.1, termitiere_proba = 0.1, 
                ):
  
  terrain = soya.Terrain(None, TERRAIN_SIZE)
  terrain.texture_factor = 0.25
  
  proba = pic_proba + plateau_proba + colline_proba + cratere1_proba + cratere2_proba + monticule_proba + termitiere_proba
  pic_proba        += 0
  plateau_proba    += pic_proba
  colline_proba    += plateau_proba
  cratere1_proba   += colline_proba
  cratere2_proba   += cratere1_proba
  monticule_proba  += cratere2_proba
  termitiere_proba += monticule_proba
  
  # Default height
  for i in range(TERRAIN_SIZE):
    for j in range(TERRAIN_SIZE):
      terrain.set_height(i, j, random.uniform(default_min_y, default_max_y))
      
  for n in range(int(random.uniform(0.001, nb_max) * TERRAIN_SIZE * TERRAIN_SIZE)):
    t = random.random() * proba
    x = random.randrange(TERRAIN_SIZE)
    y = random.randrange(TERRAIN_SIZE)
    if   t < pic_proba:
      r = random.randrange(5, 20)
      h = random.uniform(0.5, 2.5)
      
      for i in range(max(0, x - r), min(TERRAIN_SIZE - 1, x + r)):
        for j in range(max(0, y - r), min(TERRAIN_SIZE - 1, y + r)):
          d = (r - math.sqrt((i - x) * (i - x) + (j - y) * (j - y))) / float(r)
          if d > 0.0:
            d = d * d
            terrain.set_height(i, j, min(1.0, d * h + terrain.get_height(i, j)))
            
    elif t < plateau_proba:
      r1 = random.randrange(10, 20)
      r2 = random.randrange(r1 + 5, 40)
      h  = random.uniform(0.05, 0.3)
      
      for i in range(max(0, x - r2), min(TERRAIN_SIZE - 1, x + r2)):
        for j in range(max(0, y - r2), min(TERRAIN_SIZE - 1, y + r2)):
          d = (r2 - math.sqrt((i - x) * (i - x) + (j - y) * (j - y))) / float(r2 - r1)
          if d > 1.0: d = 1.0
          if d > 0.0:
            d = 0.5 - (math.cos(d * math.pi) / 2.0)
            terrain.set_height(i, j, min(1.0, d * h + terrain.get_height(i, j)))
            
    elif t < colline_proba:
      r = random.randrange(5, 35)
      h = random.uniform(0.1, 0.4)
      
      for i in range(max(0, x - r), min(TERRAIN_SIZE - 1, x + r)):
        for j in range(max(0, y - r), min(TERRAIN_SIZE - 1, y + r)):
          d = (r - math.sqrt((i - x) * (i - x) + (j - y) * (j - y))) / float(r)
          if d > 0.0:
            d = 0.5 - (math.cos(d * math.pi) / 2.0)
            terrain.set_height(i, j, min(1.0, d * h + terrain.get_height(i, j)))
            
    elif t < cratere1_proba:
      r = random.randrange(15, 20)
      h = random.uniform(0.1, 0.1)
      
      for i in range(max(0, x - r), min(TERRAIN_SIZE - 1, x + r)):
        for j in range(max(0, y - r), min(TERRAIN_SIZE - 1, y + r)):
          d = (r - math.sqrt((i - x) * (i - x) + (j - y) * (j - y))) / float(r)
          if d > 0.0:
            d = (math.sin(d * math.pi) / 2.0) + 0.5
            terrain.set_height(i, j, min(1.0, d * h + terrain.get_height(i, j)))
            
    elif t < cratere2_proba:
      r = random.randrange(15, 20)
      h = random.uniform(0.1, 0.1)
      
      for i in range(max(0, x - r), min(TERRAIN_SIZE - 1, x + r)):
        for j in range(max(0, y - r), min(TERRAIN_SIZE - 1, y + r)):
          d = (r - math.sqrt((i - x) * (i - x) + (j - y) * (j - y))) / float(r)
          if d > 0.0:
            d = (math.cos(d * math.pi) / 2.0) + 0.5
            terrain.set_height(i, j, min(1.0, d * h + terrain.get_height(i, j)))
            
    elif t < monticule_proba:
      r = random.randrange(5, 20)
      h = random.uniform(0.5, 1.0)
      
      for i in range(max(0, x - r), min(TERRAIN_SIZE - 1, x + r)):
        for j in range(max(0, y - r), min(TERRAIN_SIZE - 1, y + r)):
          d = (r - math.sqrt((i - x) * (i - x) + (j - y) * (j - y))) / float(r)
          if d > 0.0:
            d = math.sqrt(d)
            terrain.set_height(i, j, min(1.0, d * h + terrain.get_height(i, j)))
            
    else:
      # Termitière conique XXX une texture spéciale ?
      r = random.randrange(5, 15)
      h = random.uniform(0.1, 0.5)
      
      for i in range(max(0, x - r), min(TERRAIN_SIZE - 1, x + r)):
        for j in range(max(0, y - r), min(TERRAIN_SIZE - 1, y + r)):
          d = (r - math.sqrt((i - x) * (i - x) + (j - y) * (j - y))) / float(r)
          if d > 0.0:
            terrain.set_height(i, j, min(1.0, d * h + terrain.get_height(i, j)))
            
            
  smooth_terrain       (level, terrain)
  random_terrain_border(level, terrain)
  
  XYR = []
  for n in range(int(random.uniform(0.001, nb_hole) * TERRAIN_SIZE * TERRAIN_SIZE)):
    x = random.randrange(TERRAIN_SIZE)
    y = random.randrange(TERRAIN_SIZE)
    r = random.randrange(5, 20)
    
    ok = 1
    for i in range(max(0, x - r), min(TERRAIN_SIZE - 1, x + r)):
      for j in range(max(0, y - r), min(TERRAIN_SIZE - 1, y + r)):
        d = (r - math.sqrt((i - x) * (i - x) + (j - y) * (j - y))) / float(r)
        if d > 0.0:
          if terrain.get_height(i, j) < 0.4: ok = 0
    if ok == 0: continue
    
    XYR.append((x, y, r))
    
  for x, y, r in XYR:
    h = random.uniform(0.1, 0.4)
    
    for i in range(max(0, x - r), min(TERRAIN_SIZE - 1, x + r)):
      for j in range(max(0, y - r), min(TERRAIN_SIZE - 1, y + r)):
        d = (r - math.sqrt((i - x) * (i - x) + (j - y) * (j - y))) / float(r)
        if d > 0.0:
          d = 0.5 - (math.cos(d * math.pi) / 2.0)
          terrain.set_height(i, j, max(0.0, -d * h + terrain.get_height(i, j)))
          
          
          
  end_terrain          (level, terrain)
  terrain.y = -30.0
  return terrain
  
def smooth_terrain(level, terrain, nb = 2):
  for k in range(nb):
    smoothed = [0.0] * (TERRAIN_SIZE * TERRAIN_SIZE)
    for i in range(1, TERRAIN_SIZE - 1):
      for j in range(1, TERRAIN_SIZE - 1):
        smoothed[i + TERRAIN_SIZE * j] = (terrain.get_height(i, j) + terrain.get_height(i - 1, j) + terrain.get_height(i, j - 1) + terrain.get_height(i + 1, j) + terrain.get_height(i, j + 1)) / 5.0
    for i in range(1, TERRAIN_SIZE - 1):
      for j in range(1, TERRAIN_SIZE - 1):
        terrain.set_height(i, j, smoothed[i + TERRAIN_SIZE * j])
        
def random_terrain_border(level, terrain):
  out_of_map_vertex_options = (1, 1)
  
  fall_length  = 2
  afall_length = 0
  for i in range(TERRAIN_SIZE):
    for j in range(fall_length):
      terrain.set_vertex_option(i, j, *out_of_map_vertex_options)
      #terrain.set_vertex_color(i, j, (0.0, 0.0, 0.0, 0.0))
      terrain.set_height(i, j, 0.0)
    terrain.set_height(i, j + 1, 0.92 * terrain.get_height(i, j + 1))
    if i % 2:
      fall_length = max(1, fall_length + afall_length)
      if (fall_length == 1) and (afall_length == -1): afall_length = 0
      else: afall_length = max(-1, min(1, afall_length + random.randint(-1, 1)))
      
  fall_length  = 2
  afall_length = 0
  for i in range(TERRAIN_SIZE):
    for j in range(TERRAIN_SIZE - 1, TERRAIN_SIZE - fall_length - 1, -1):
      terrain.set_vertex_option(i, j, *out_of_map_vertex_options)
      #terrain.set_vertex_color(i, j, (0.0, 0.0, 0.0, 0.0))
      terrain.set_height(i, j, 0.0)
    terrain.set_height(i, j - 1, 0.92 * terrain.get_height(i, j - 1))
    if i % 2:
      fall_length = max(1, fall_length + afall_length)
      if (fall_length == 1) and (afall_length == -1): afall_length = 0
      else: afall_length = max(-1, min(1, afall_length + random.randint(-1, 1)))

  fall_length  = 2
  afall_length = 0
  for j in range(TERRAIN_SIZE):
    for i in range(fall_length):
      terrain.set_vertex_option(i, j, *out_of_map_vertex_options)
      #terrain.set_vertex_color(i, j, (0.0, 0.0, 0.0, 0.0))
      terrain.set_height(i, j, 0.0)
    terrain.set_height(i + 1, j, 0.92 * terrain.get_height(i + 1, j))
    if j % 2:
      fall_length = max(1, fall_length + afall_length)
      if (fall_length == 1) and (afall_length == -1): afall_length = 0
      else: afall_length = max(-1, min(1, afall_length + random.randint(-1, 1)))
      
  fall_length  = 2
  afall_length = 0
  for j in range(TERRAIN_SIZE):
    for i in range(TERRAIN_SIZE - 1, TERRAIN_SIZE - fall_length - 1, -1):
      terrain.set_vertex_option(i, j, *out_of_map_vertex_options)
      #terrain.set_vertex_color(i, j, (0.0, 0.0, 0.0, 0.0))
      terrain.set_height(i, j, 0.0)
    terrain.set_height(i - 1, j, 0.92 * terrain.get_height(i - 1, j))
    if j % 2:
      fall_length = max(1, fall_length + afall_length)
      if (fall_length == 1) and (afall_length == -1): afall_length = 0
      else: afall_length = max(-1, min(1, afall_length + random.randint(-1, 1)))


def end_terrain(level, terrain, height = 50.0):
  terrain.multiply_height(height)
  terrain.scale_factor = TERRAIN_SCALE
  terrain.map_size = 8
  terrain.split_factor = 4.0
  
  level.static_part.add(terrain)


def add_flower(level, terrain, nb = 40):
  grass2 = soya.Material.get("grass3")
  for i in range(nb):
    x = random.randrange(TERRAIN_SIZE)
    y = random.randrange(TERRAIN_SIZE)
    r = random.randint(1, 3)
    
    for i in range(max(0, x - r), min(TERRAIN_SIZE - 1, x + r)):
      for j in range(max(0, y - r), min(TERRAIN_SIZE - 1, y + r)):
        d = (r - math.sqrt((i - x) * (i - x) + (j - y) * (j - y))) / float(r)
        if (d >= 0.0) and terrain.get_height(i, j) < 30:
          terrain.set_material(i, j, grass2)
  

  



    

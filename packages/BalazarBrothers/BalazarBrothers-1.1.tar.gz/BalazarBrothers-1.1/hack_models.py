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

import soya, balazar_brothers, balazar_brothers.globdef

world = soya.World.get("fontaine_eau")
for face in world:
  for vertex in face:
    face.lit = 0
    print vertex % world
    if vertex.z < -7.0:
      print "."
      vertex.diffuse = (1.0, 1.0, 1.0, 0.0)
    else:
      vertex.diffuse = (1.0, 1.0, 1.0, 1.0)
      
world.save()

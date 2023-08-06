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

import soya, balazar_brothers, balazar_brothers.level, balazar_brothers.bonus, balazar_brothers.globdef

KEYS   = {}
CHESTS = {}

for filename in balazar_brothers.level.Level.availables():
  if "_" in filename:
    worldname = "_".join(filename.split("_")[:-1])
    level = balazar_brothers.level.Level.get(filename)
    for i in level.recursive():
      if   isinstance(i, balazar_brothers.bonus.Key       ): KEYS  [worldname] = KEYS  .get(worldname, 0) + 1
      elif isinstance(i, balazar_brothers.bonus.SmallChest): CHESTS[worldname] = CHESTS.get(worldname, 0) + 1
      elif isinstance(i, balazar_brothers.bonus.BigChest  ): CHESTS[worldname] = CHESTS.get(worldname, 0) + 5
      
worldnames = set()
worldnames.update(KEYS.keys())
worldnames.update(CHESTS.keys())

for worldname in worldnames:
  print worldname, ":", KEYS.get(worldname, 0), "keys", CHESTS.get(worldname, 9), "chests"
print "Total :", sum(CHESTS.values()), "chests"

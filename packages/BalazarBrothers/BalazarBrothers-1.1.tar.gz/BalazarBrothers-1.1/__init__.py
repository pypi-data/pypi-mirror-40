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

# Import all modules, in order to register all classes in Cerealizer
import cerealizer, soya.tofu as tofu, soya, soya.cerealizer4soya

soya.set_file_format(cerealizer, [cerealizer])


import balazar_brothers.globdef, balazar_brothers.character, balazar_brothers.controller, balazar_brothers.level, balazar_brothers.weather, balazar_brothers.bonus, balazar_brothers.platform_, balazar_brothers.main_loop, balazar_brothers.player, balazar_brothers.trap
cerealizer.freeze_configuration()


platform = balazar_brothers.platform_

#
# Copyright 2018 coord.e
#
# This file is part of flom-py.
#
# flom-py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# flom-py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with flom-py.  If not, see <http://www.gnu.org/licenses/>.
#

cmake_minimum_required(VERSION 3.7)

pybind11_add_module(flom MODULE binding.cpp interpolate.cpp enums.cpp motion.cpp effector.cpp ranges.cpp frame.cpp errors.cpp)
target_link_libraries(flom PRIVATE -lflom)
enable_clang_format(flom)

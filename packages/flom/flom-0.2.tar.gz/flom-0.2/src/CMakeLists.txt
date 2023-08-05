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
cmake_policy(SET CMP0048 NEW)

project(flom-py VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(PYBIND11_CPP_STANDARD -std=c++17)

if(NOT CONFIG)
  set(CONFIG Release)
endif()

message(STATUS "Build in ${CONFIG} mode")

if(CONFIG STREQUAL "Debug")
  add_compile_options(-O0 -g3)
elseif(CONFIG STREQUAL "Release")
  add_compile_options(-O3)
endif()

add_subdirectory(third_party/pybind11)
# pybind11 headers produce so many errors with strict compiler options
include_directories(SYSTEM ${PYBIND11_INCLUDE_DIR})

include(cmake/clang-format.cmake)

add_subdirectory(binding)

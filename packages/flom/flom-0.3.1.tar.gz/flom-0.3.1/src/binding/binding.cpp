//
// Copyright 2018 coord.e
//
// This file is part of flom-py.
//
// flom-py is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// flom-py is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with flom-py.  If not, see <http://www.gnu.org/licenses/>.
//

#include <pybind11/pybind11.h>

#include "declarations.hpp"

namespace py = pybind11;

PYBIND11_MODULE(flom, m) {
  m.doc() = "flom: Motion exchange format";

  flom_py::define_errors(m);

  flom_py::define_interpolate(m);
  flom_py::define_enums(m);

  flom_py::define_motion(m);
  flom_py::define_ranges(m);

  flom_py::define_frame(m);

  flom_py::define_effector(m);
}

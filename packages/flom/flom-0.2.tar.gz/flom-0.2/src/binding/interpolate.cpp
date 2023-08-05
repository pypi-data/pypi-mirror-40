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

#include <flom/interpolation.hpp>

#include <pybind11/pybind11.h>

#include "declarations.hpp"

namespace flom_py {

namespace py = pybind11;

void define_interpolate(py::module &m) {
  m.def(
      "interpolate",
      py::overload_cast<double, flom::Location const &, flom::Location const &>(
          &flom::interpolate));
  m.def(
      "interpolate",
      py::overload_cast<double, flom::Rotation const &, flom::Rotation const &>(
          &flom::interpolate));
  m.def(
      "interpolate",
      py::overload_cast<double, flom::Effector const &, flom::Effector const &>(
          &flom::interpolate));
  m.def("interpolate",
        py::overload_cast<double, flom::Frame const &, flom::Frame const &>(
            &flom::interpolate));
  m.def("interpolate",
        py::overload_cast<double, double, double>(&flom::interpolate));
}

} // namespace flom_py

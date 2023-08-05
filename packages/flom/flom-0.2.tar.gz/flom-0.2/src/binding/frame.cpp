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

#include <flom/range.hpp>

#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "declarations.hpp"

namespace flom_py {

namespace py = pybind11;

void define_frame(py::module &m) {
  py::class_<flom::Frame>(m, "Frame")
      .def(py::init<>())
      .def_readwrite("positions", &flom::Frame::positions)
      .def_readwrite("effectors", &flom::Frame::effectors)
      .def("joint_names", &flom::Frame::joint_names)
      .def("effector_names", &flom::Frame::effector_names)
      .def(py::self == py::self)
      .def(py::self != py::self)
      .def(py::self += py::self)
      .def(py::self + py::self)
      .def(py::self -= py::self)
      .def(py::self - py::self)
      .def(py::self *= double())
      .def(py::self * double())
      .def(py::self *= float())
      .def(py::self * float());
}

} // namespace flom_py

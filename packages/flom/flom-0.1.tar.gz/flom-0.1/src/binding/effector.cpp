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

#include <flom/effector.hpp>

#include <pybind11/numpy.h>
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <boost/qvm/quat_access.hpp>
#include <boost/qvm/vec_access.hpp>

#include "declarations.hpp"

namespace flom_py {

namespace py = pybind11;

void define_effector(py::module &m) {
  py::class_<flom::Effector>(m, "Effector")
      .def(py::init<>())
      .def_readwrite("location", &flom::Effector::location)
      .def_readwrite("rotation", &flom::Effector::rotation)
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

  py::class_<flom::Location>(m, "Location")
      .def_readwrite("weight", &flom::Location::weight)
      .def_property("vec",
                    [](flom::Location const &l) {
                      py::array_t<double> ret(3);
                      auto *data = ret.mutable_data();
                      data[0] = boost::qvm::X(l.vec);
                      data[1] = boost::qvm::Y(l.vec);
                      data[2] = boost::qvm::Z(l.vec);
                      return ret;
                    },
                    [](flom::Location &l, py::array_t<double> const &ary) {
                      auto *data = ary.data();
                      boost::qvm::X(l.vec) = data[0];
                      boost::qvm::Y(l.vec) = data[1];
                      boost::qvm::Z(l.vec) = data[2];
                    })
      .def(py::self == py::self);

  py::class_<flom::Rotation>(m, "Rotation")
      .def_readwrite("weight", &flom::Rotation::weight)
      .def_property("quat",
                    [](flom::Rotation const &l) {
                      py::array_t<double> ret(4);
                      auto *data = ret.mutable_data();
                      data[0] = boost::qvm::S(l.quat);
                      data[1] = boost::qvm::X(l.quat);
                      data[2] = boost::qvm::Y(l.quat);
                      data[3] = boost::qvm::Z(l.quat);
                      return ret;
                    },
                    [](flom::Rotation &l, py::array_t<double> const &ary) {
                      auto *data = ary.data();
                      boost::qvm::S(l.quat) = data[0];
                      boost::qvm::X(l.quat) = data[1];
                      boost::qvm::Y(l.quat) = data[2];
                      boost::qvm::Z(l.quat) = data[3];
                    })
      .def(py::self == py::self);
}

} // namespace flom_py

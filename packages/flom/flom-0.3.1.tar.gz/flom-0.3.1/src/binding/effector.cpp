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
  py::class_<flom::EffectorDifference>(m, "EffectorDifference")
      .def(py::init<const flom::Effector &, const flom::Effector &>())
      .def_property_readonly(
          "location",
          [](const flom::EffectorDifference &eff) { return eff.location(); })
      .def_property_readonly(
          "rotation",
          [](const flom::EffectorDifference &eff) { return eff.rotation(); })
      .def("is_compatible", &flom::EffectorDifference::is_compatible)
      .def(py::self == py::self)
      .def(py::self != py::self)
      .def(py::self + py::self)
      .def(py::self += py::self)
      .def(py::self * std::size_t())
      .def(py::self *= std::size_t());

  py::class_<flom::Effector>(m, "Effector")
      .def(py::init<>())
      .def(py::init<const std::optional<flom::Location> &,
                    const std::optional<flom::Rotation> &>())
      .def_property("location",
                    [](const flom::Effector &eff) { return eff.location(); },
                    &flom::Effector::set_location)
      .def_property("rotation",
                    [](const flom::Effector &eff) { return eff.rotation(); },
                    &flom::Effector::set_rotation)
      .def("clear_location", &flom::Effector::clear_location)
      .def("clear_rotation", &flom::Effector::clear_rotation)
      .def("new_compatible_effector", &flom::Effector::new_compatible_effector)
      .def("is_compatible", py::overload_cast<const flom::Effector &>(
                                &flom::Effector::is_compatible, py::const_))
      .def("is_compatible", py::overload_cast<const flom::EffectorDifference &>(
                                &flom::Effector::is_compatible, py::const_))
      .def(py::self == py::self)
      .def(py::self != py::self)
      .def(py::self - py::self)
      .def("__add__",
           [](const flom::Effector &e, const flom::EffectorDifference &diff) {
             return e + diff;
           })
      .def("__iadd__",
           [](flom::Effector &e, const flom::EffectorDifference &diff) {
             return e += diff;
           });

  py::class_<flom::Location>(m, "Location")
      .def(py::init<>())
      .def(py::init([](const py::array_t<double> &ary) {
        auto *data = ary.data();
        flom::Location::value_type vec;
        boost::qvm::X(vec) = data[0];
        boost::qvm::Y(vec) = data[1];
        boost::qvm::Z(vec) = data[2];
        return flom::Location{vec};
      }))
      .def_property("vector",
                    [](flom::Location const &l) {
                      py::array_t<double> ret(3);
                      auto *data = ret.mutable_data();
                      auto const &vec = l.vector();
                      data[0] = boost::qvm::X(vec);
                      data[1] = boost::qvm::Y(vec);
                      data[2] = boost::qvm::Z(vec);
                      return ret;
                    },
                    [](flom::Location &l, py::array_t<double> const &ary) {
                      auto *data = ary.data();
                      flom::Location::value_type vec;
                      boost::qvm::X(vec) = data[0];
                      boost::qvm::Y(vec) = data[1];
                      boost::qvm::Z(vec) = data[2];
                      l.set_vector(vec);
                    })
      .def(py::self == py::self)
      .def(py::self != py::self)
      .def(py::self + py::self)
      .def(py::self += py::self)
      .def(py::self - py::self)
      .def(py::self -= py::self)
      .def(py::self * std::size_t())
      .def(py::self *= std::size_t());

  py::class_<flom::Rotation>(m, "Rotation")
      .def(py::init<>())
      .def(py::init([](const py::array_t<double> &ary) {
        auto *data = ary.data();
        flom::Rotation::value_type quat;
        boost::qvm::S(quat) = data[0];
        boost::qvm::X(quat) = data[1];
        boost::qvm::Y(quat) = data[2];
        boost::qvm::Z(quat) = data[3];
        return flom::Rotation{quat};
      }))
      .def_property("quaternion",
                    [](flom::Rotation const &l) {
                      py::array_t<double> ret(4);
                      auto *data = ret.mutable_data();
                      auto const &quat = l.quaternion();
                      data[0] = boost::qvm::S(quat);
                      data[1] = boost::qvm::X(quat);
                      data[2] = boost::qvm::Y(quat);
                      data[3] = boost::qvm::Z(quat);
                      return ret;
                    },
                    [](flom::Rotation &l, py::array_t<double> const &ary) {
                      auto *data = ary.data();
                      flom::Rotation::value_type quat;
                      boost::qvm::S(quat) = data[0];
                      boost::qvm::X(quat) = data[1];
                      boost::qvm::Y(quat) = data[2];
                      boost::qvm::Z(quat) = data[3];
                      l.set_quaternion(quat);
                    })
      .def(py::self == py::self)
      .def(py::self != py::self)
      .def(py::self + py::self)
      .def(py::self += py::self)
      .def(py::self - py::self)
      .def(py::self -= py::self)
      .def(py::self * std::size_t())
      .def(py::self *= std::size_t());
}

} // namespace flom_py

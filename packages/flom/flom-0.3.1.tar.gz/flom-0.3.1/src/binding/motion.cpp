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

#include <flom/motion.hpp>
#include <flom/range.hpp>

#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "declarations.hpp"

namespace flom_py {

namespace py = pybind11;

void define_motion(py::module &m) {
  py::class_<flom::EffectorType>(m, "EffectorType")
      .def(py::init<std::optional<flom::CoordinateSystem>,
                    std::optional<flom::CoordinateSystem>>())
      .def("clear_location", &flom::EffectorType::clear_location)
      .def("clear_rotation", &flom::EffectorType::clear_rotation)
      .def("new_effector", &flom::EffectorType::new_effector)
      .def("is_compatible", &flom::EffectorType::is_compatible)
      .def_property("location", &flom::EffectorType::location,
                    &flom::EffectorType::set_location)
      .def_property("rotation", &flom::EffectorType::rotation,
                    &flom::EffectorType::set_rotation)
      .def(py::self == py::self)
      .def(py::self != py::self);

  py::class_<flom::EffectorWeight>(m, "EffectorWeight")
      .def(py::init<double, double>())
      .def_property("location", &flom::EffectorWeight::location,
                    &flom::EffectorWeight::set_location)
      .def_property("rotation", &flom::EffectorWeight::rotation,
                    &flom::EffectorWeight::set_rotation)
      .def(py::self == py::self)
      .def(py::self != py::self);

  m.def("load", [](std::string const &filename) {
    std::ifstream f(filename, std::ios::binary);
    return flom::Motion::load(f);
  });
  m.def("load_json", [](std::string const &filename) {
    std::ifstream f(filename);
    return flom::Motion::load_json(f);
  });
  m.def("load_json_string", &flom::Motion::load_json_string);

  py::class_<flom::Motion>(m, "Motion")
      .def(py::init<std::unordered_set<std::string>,
                    std::unordered_map<std::string, flom::EffectorType>,
                    std::string>(),
           py::arg("joint_names"), py::arg("effector_types"), py::arg("model"))
      .def("dump",
           [](flom::Motion const &motion, std::string const &filename) {
             std::ofstream f(filename, std::ios::binary);
             motion.dump(f);
           })
      .def("dump_json",
           [](flom::Motion const &motion, std::string const &filename) {
             std::ofstream f(filename);
             motion.dump_json(f);
           })
      .def("dump_json_string", &flom::Motion::dump_json_string)
      .def("frame_at",
           [](const flom::Motion &m, double t) {
             // TODO: Return directly as value
             return std::make_unique<flom::Frame>(m.frame_at(t));
           })
      .def("frames", &flom::Motion::frames)
      .def("loop", &flom::Motion::loop)
      .def("set_loop", &flom::Motion::set_loop)
      .def("model_id", &flom::Motion::model_id)
      .def("set_model_id", &flom::Motion::set_model_id)
      .def("effector_type", &flom::Motion::effector_type)
      .def("is_in_range_at", &flom::Motion::is_in_range_at)
      .def("length", &flom::Motion::length)
      .def("joint_names", &flom::Motion::joint_names)
      .def("effector_names", &flom::Motion::effector_names)
      .def("new_keyframe",
           [](const flom::Motion &m) {
             // TODO: Return directly as value
             return std::make_unique<flom::Frame>(m.new_keyframe());
           })
      .def("insert_keyframe", &flom::Motion::insert_keyframe, py::arg("t"),
           py::arg("frame"))
      .def("delete_keyframe", &flom::Motion::delete_keyframe, py::arg("t"),
           py::arg("loose") = true)
      .def("keyframes", &flom::Motion::keyframes)
      .def("clear_keyframes", &flom::Motion::clear_keyframes)
      .def("is_valid_frame", &flom::Motion::is_valid_frame)
      .def("is_valid", &flom::Motion::is_valid)
      .def("effector_weight", &flom::Motion::effector_weight)
      .def("set_effector_weight", &flom::Motion::set_effector_weight)
      .def(py::self == py::self)
      .def(py::self != py::self);
}

} // namespace flom_py

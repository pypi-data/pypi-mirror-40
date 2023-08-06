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

#include <pybind11/pybind11.h>

#include "declarations.hpp"

namespace flom_py {

namespace py = pybind11;

void define_ranges(py::module &m) {
  py::class_<flom::KeyRange<std::string>>(m, "KeyRange")
      .def("__iter__", [](flom::KeyRange<std::string> &range) {
        return py::make_iterator(range.begin(), range.end());
      });

  py::class_<flom::FrameRange>(m, "FrameRange")
      .def("__iter__", [](flom::FrameRange &range) {
        return py::make_iterator(range.begin(), range.end());
      });

  py::class_<flom::KeyframeRange>(m, "KeyframeRange")
      .def("__iter__", [](flom::KeyframeRange &range) {
        return py::make_iterator(range.begin(), range.end());
      });

  py::class_<flom::CheckedFrameRef>(m, "CheckedFrameRef")
      .def("get",
           [](const flom::CheckedFrameRef &f) {
             // TODO: Return directly as value
             return std::make_unique<flom::Frame>(f);
           })
      .def("set",
           [](flom::CheckedFrameRef &ref, const flom::Frame &f) { ref = f; });
}

} // namespace flom_py

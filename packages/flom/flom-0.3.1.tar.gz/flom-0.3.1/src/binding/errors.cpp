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

#include <flom/errors.hpp>

#include <pybind11/pybind11.h>

#include "declarations.hpp"

namespace flom_py {

namespace py = pybind11;
namespace errs = flom::errors;

void define_errors(py::module &m) {
  py::register_exception<errs::InvalidTimeError>(m, "InvalidTimeError");
  py::register_exception<errs::OutOfFramesError>(m, "OutOfFramesError");
  py::register_exception<errs::KeyframeNotFoundError>(m,
                                                      "KeyframeNotFoundError");
  py::register_exception<errs::ParseError>(m, "ParseError");
  py::register_exception<errs::SerializationError>(m, "SerializationError");
  py::register_exception<errs::JSONLoadError>(m, "JSONLoadError");
  py::register_exception<errs::JSONDumpError>(m, "JSONDumpError");
  py::register_exception<errs::InvalidFrameError>(m, "InvalidFrameError");
  py::register_exception<errs::InitKeyframeError>(m, "InitKeyframeError");
  py::register_exception<errs::InitKeyframeError>(m, "InvaildWeightError");
}

} // namespace flom_py

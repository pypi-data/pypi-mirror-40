#ifndef FLOM_PY_DECLARATIONS_HPP
#define FLOM_PY_DECLARATIONS_HPP

#include <pybind11/pybind11.h>

namespace flom_py {

void define_errors(pybind11::module&);
void define_interpolate(pybind11::module&);
void define_enums(pybind11::module&);
void define_motion(pybind11::module&);
void define_effector(pybind11::module&);
void define_ranges(pybind11::module&);
void define_frame(pybind11::module&);

}

#endif

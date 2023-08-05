#include <Python.h>

#include "c11hash.h"

static PyObject *c11_getpowhash(PyObject *self, PyObject *args)
{
    char *output;
    PyObject *value;
#if PY_MAJOR_VERSION >= 3
    PyBytesObject *input;
#else
    PyStringObject *input;
#endif
    if (!PyArg_ParseTuple(args, "S", &input))
        return NULL;
    Py_INCREF(input);
    output = PyMem_Malloc(32);

#if PY_MAJOR_VERSION >= 3
    c11_hash((char *)PyBytes_AsString((PyObject*) input), output);
#else
    c11_hash((char *)PyString_AsString((PyObject*) input), output);
#endif
    Py_DECREF(input);
#if PY_MAJOR_VERSION >= 3
    value = Py_BuildValue("y#", output, 32);
#else
    value = Py_BuildValue("s#", output, 32);
#endif
    PyMem_Free(output);
    return value;
}

static PyMethodDef C11Methods[] = {
    { "getPoWHash", c11_getpowhash, METH_VARARGS, "Returns the proof of work hash using c11 hash" },
    { NULL, NULL, 0, NULL }
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef C11Module = {
    PyModuleDef_HEAD_INIT,
    "c11_hash",
    "...",
    -1,
    C11Methods
};

PyMODINIT_FUNC PyInit_c11_hash(void) {
    return PyModule_Create(&C11Module);
}

#else

PyMODINIT_FUNC initc11_hash(void) {
    (void) Py_InitModule("c11_hash", C11Methods);
}
#endif

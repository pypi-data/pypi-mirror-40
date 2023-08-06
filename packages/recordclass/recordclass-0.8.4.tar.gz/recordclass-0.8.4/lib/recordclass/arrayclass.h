#define C_DIV(a,b) ((a)/(b))

#define arrayclass_items(op) ((PyObject**)((char*)(op) + sizeof(PyObject)))
#define arrayclass_dictptr(op, tp) ((PyObject**)((char*)op + tp->tp_dictoffset))
#define arrayclass_weaklistptr(op, tp) ((PyObject**)((char*)op + tp->tp_weaklistoffset))

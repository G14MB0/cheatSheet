#include <Python.h>

//######################################################
//##      this are  methods                            ##
//######################################################
static PyObject* hello_world(PyObject* self) {
    return PyUnicode_FromString("Hello, World!");
}

static PyObject* goodbye_world(PyObject* self) {
    return PyUnicode_FromString("Goodbye, World!");
}


// Funzione di confronto per qsort
static int compare_doubles(const void* a, const void* b) {
    double arg1 = *(const double*)a;
    double arg2 = *(const double*)b;

    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}


static PyObject* sort_float_list(PyObject* self, PyObject* args) {

    PyObject* input_list;

    //questa parte si occupa della validazione
    //la stringa "0!" è usata per indicare come deve essere args
    //in questo caso deve essere oggetto di un tipo specificato, es: "O!" &PyList_Type
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &input_list)) {
        return NULL;
    }


    //Py_ssize_t: È un tipo definito nella Python/C API. 
    //È simile a size_t che si trova comunemente in C, ma è progettato per gestire anche valori negativi. 
    //Viene spesso utilizzato per rappresentare la dimensione di oggetti o l'indice in sequenze in Python/C API.
    Py_ssize_t size = PyList_Size(input_list);

    //invece che definire un array di dimenzione nota (i.e. double array[10])
    //si definisce un puntatore array a double di dimensione non nota
    //col quale si alloca poi una memoria dinamica (malloc) della dimensione size calcolata prima
    double* array = malloc(size * sizeof(double));

    //semplice controllo se la fuzione malloc è andata a buon fine.
    //in caso contrario ritorna un eccezione di "no memory"
    if (!array) {
        return PyErr_NoMemory();
    }


    //scorri tutti gli elementi della lista (come puntatore) e convertili in double se sono float
    //altrimenti libera la memoria e ritorna un eccezione
    for (Py_ssize_t i = 0; i < size; i++) {
        PyObject* item = PyList_GetItem(input_list, i);
        if (!PyFloat_Check(item)) {
            free(array);
            PyErr_SetString(PyExc_TypeError, "List contains non-float value");
            return NULL;
        }
        array[i] = PyFloat_AsDouble(item);
    }

    // Ordiniamo l'array
    qsort(array, size, sizeof(double), (int (*)(const void*, const void*))compare_doubles);


    //crea una nuova lista e popolala con gli elementi presenti nella lista originale ordinata
    //questi elementi vengono prima confertiti in float (poichè precedentemente convertiti in double da float)
    //PyList_SetItem "consuma" una referenza all'oggetto passato,
    // il che significa che non è necessario decrementare i
    PyObject* sorted_list = PyList_New(size);
    for (Py_ssize_t i = 0; i < size; i++) {
        PyObject* num = PyFloat_FromDouble(array[i]);
        PyList_SetItem(sorted_list, i, num);
    }

    //libera la memoria array ma non sorted_list in quanto va ritornata a python
    free(array);
    return sorted_list;
}


//######################################################
//##      This is the declaration array               ##
//######################################################
static PyMethodDef HelloMethods[] = {
    {"hello_world",  hello_world, METH_NOARGS, "Print 'Hello, World!'"},
    {"goodbye_world",  goodbye_world, METH_NOARGS, "Print 'Goodbye, World!'"},
    {"sort_float_list",  sort_float_list, METH_VARARGS, "sort a list of float"}, //da notare METH_VARARGS in caso di argomenti
    {NULL, NULL, 0, NULL}
};

//######################################################
//##  this are the module parameter used during comp  ##
//######################################################
static struct PyModuleDef hellomodule = {
    PyModuleDef_HEAD_INIT,
    "hello",      // nome del modulo
    NULL,         // documentazione del modulo (può essere NULL)
    -1,           // dimensione del modulo (per la creazione di moduli multi-threaded)
    HelloMethods
};


//######################################################
//##     this is the equivalent of __init__(self)     ##
//######################################################
PyMODINIT_FUNC PyInit_hello(void) {
    return PyModule_Create(&hellomodule);
}

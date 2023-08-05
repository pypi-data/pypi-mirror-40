//
// Created by lpe234 on 2018/12/27.
//
// doc: https://docs.python.org/3/extending/extending.html

#include <Python.h>


/**
 * reverse
 * 实际执行函数
 *
 * @param str
 * @param size
 */
void reverse(char *str, int size) {
    for (int i = 0, j = size-1; i < j ; ++i, --j) {
        char tmp = str[i];
        str[i] = str[j];
        str[j] = tmp;
    }
}

/**
 * 对函数进行封装
 *
 * @param self
 * @param args
 * @return
 */
PyObject *
strings_reverse(PyObject *self, PyObject *args) {
    char *str;

    // 参数解析
    if (!PyArg_ParseTuple(args, "s", &str)) {
        return NULL;
    }

    // 调用 reverse
    reverse(str, (int) strlen(str));

    return Py_BuildValue("s", str);
}

/**
 * 定义模块方法表
 *
 */
static PyMethodDef StringsMethods[] = {
        {"reverse", strings_reverse, METH_VARARGS, "Reverse str."},
        {NULL, NULL, 0, NULL}
};

/**
 * 定义模块
 *
 */
static struct PyModuleDef stringsmodule = {
        PyModuleDef_HEAD_INIT,
        "strings",
        "reverse str, \"abc\" => \"cba\"",
        -1,
        StringsMethods
};

/**
 * 模块初始化
 *
 * @return
 */
PyMODINIT_FUNC
PyInit_strings(void) {
    return PyModule_Create(&stringsmodule);
}

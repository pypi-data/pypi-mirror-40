#include <Python.h>
#define _WIN32_DCOM
#define _WIN32_FUSION 0x0100
#include <atlbase.h>
#include <atlstr.h>
#define _ATL_CSTRING_EXPLICIT_CONSTRUCTORS      // some CString constructors will be explicit
#include <iostream>

#ifdef STDERR_LOGGING

template<class T>
void info(const T& msg) {
    std::cerr << "[+] " << msg << std::endl;
}

template<class T>
void warn(const T& msg) {
    std::cerr << "[!] " << msg << std::endl;
}

template<class T>
void error(const T& ) {
    std::cerr << "[-] " << msg << std::endl;
}

#else

template<class T>
void info(const T& ) {}

template<class T>
void warn(const T& ) {}

template<class T>
void error(const T& ) {}

#endif

#define ENOERROR 0
#define EINVPARAM -1
#define ECOMINIT -2
#define ECREATECTX -3
#define EACTIVATE -4
#define ESTORE -5


const char s_uninitID = 0;
struct ctxHolder {
    ctxHolder() : _id(s_uninitID), _hCtx(INVALID_HANDLE_VALUE), _cookie((ULONG_PTR)0) {}
    char _id;
    HANDLE _hCtx;
    ULONG_PTR _cookie;
};

const int MAX_CTX = 32;
static ctxHolder s_contexts[MAX_CTX];
static bool s_comInitialized = false;

HRESULT InitializeCom() {
    if (!s_comInitialized) {
        info("Initializing COM...");
        HRESULT hr = CoInitializeEx(0, COINIT_MULTITHREADED);
        if (hr == S_OK) {
            info("Running COM in multithreaded mode");
            s_comInitialized = true;
        } else if (hr == RPC_E_CHANGED_MODE) {
            info("Running COM in singlethreaded mode");
			info("Switching to multithreaded mode");
			CoUninitialize();
			InitializeCom();
            s_comInitialized = true;
            return S_OK;
        }
        return hr;
    }
    return S_OK;
}

int CreateActivationContext(const char* manifest, ACTCTX& actCtx, HANDLE& hCtx) {
    memset((void*)&actCtx, 0, sizeof(ACTCTX));
    actCtx.cbSize = sizeof(ACTCTX);
    actCtx.lpSource = manifest;

    hCtx = ::CreateActCtx(&actCtx);
    if (hCtx == INVALID_HANDLE_VALUE) {
        error("Failed to activate context!");
        return ECREATECTX;
    }
    return ENOERROR;
}

int ActivateActivationContext(HANDLE hCtx, ULONG_PTR& cookie) {
    if (::ActivateActCtx(hCtx, &cookie)) {
        return ENOERROR;
    }
    else {
        return EACTIVATE;
    }
}

int StoreContext(HANDLE hCtx, ULONG_PTR cookie) {
    char i = 1;
    for (; i <= MAX_CTX; ++i) {
        ctxHolder& tempCtx = s_contexts[i - 1];
        if (tempCtx._id == s_uninitID) {
            tempCtx._id = i;
            tempCtx._hCtx = hCtx;
            tempCtx._cookie = cookie;
            return i;
        }
    }
    // All available slots are already busy
    return ESTORE;
}


static PyObject* activate(PyObject* self, PyObject* args)
{
    int res = ENOERROR;
    char* manifest;
    if (!PyArg_ParseTuple(args, "s", &manifest)) {
        return Py_BuildValue("i", EINVPARAM);
    }
    res = static_cast<int>(InitializeCom());
    if (res == ENOERROR) {
        ACTCTX actCtx;
        HANDLE hCtx = INVALID_HANDLE_VALUE;
        res = CreateActivationContext(manifest, actCtx, hCtx);
        if (res == ENOERROR) {
            ULONG_PTR cookie;
            res = ActivateActivationContext(hCtx, cookie);
            if (res == ENOERROR) {
                ULONG_PTR cookie;
                res = StoreContext(hCtx, cookie);
            }
        }
    }

    return Py_BuildValue("i", res);
}

static PyObject* deactivate(PyObject* self, PyObject* args)
{
    int res = 0;
    int ctxId = 0;
    if (!PyArg_ParseTuple(args, "i", &ctxId)) {
      res = -1;
    } else {
        if (ctxId >= 0 && ctxId <= MAX_CTX) {
            ctxHolder& ctx = s_contexts[ctxId - 1];
            ::DeactivateActCtx(0, ctx._cookie);
            ctx._id = s_uninitID;
            ctx._hCtx = INVALID_HANDLE_VALUE;
            ctx._cookie = (ULONG_PTR)0;
        } else {
            res = -1;
        }
    }
    return Py_BuildValue("i", res);
}

static char actontext_docs[] =
    "actontext: Allows to use side-by-side manifests to refer inproc COM server DLL without registering it in Windows registry\n";

static PyMethodDef actontext_funcs[] = {
    {"activate", (PyCFunction)activate,
     METH_VARARGS,
     "Activate context for the manifest. Given side-by-side manifest path it loads activation context of manifested in-proc server to allow using of COM objects declared in typelibrary without any additional setup. It returns a context ID or negative error code otherwise"},
     {"deactivate", (PyCFunction)deactivate,
     METH_VARARGS,
     "Deactivate context with given id"},
    {NULL, NULL, 0, NULL}
};

static const char* s_docstring = "" \
"This module provides functions to load COM DLL on Windows machine, to avoid registering it in Windows registry.\n" 
"You can find more about how it can be done in articles on web:\n"
"- \"Registration-Free Activation of COM Components: A Walkthrough\" (https://docs.microsoft.com/en-us/previous-versions/dotnet/articles/ms973913(v=msdn.10));\n"
"- \"\" (https://weblog.west-wind.com/posts/2011/Oct/09/An-easy-way-to-create-Side-by-Side-registrationless-COM-Manifests-with-Visual-Studio);\n"
"- etc. just Google it\n\n" 
"The main use case for module could be lightweight testing of COM objects, created from built in-proc COM servers\n"
""
;

static struct PyModuleDef actontext = {
   PyModuleDef_HEAD_INIT,
   "actontext_internal",   
   s_docstring, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   actontext_funcs
};

PyMODINIT_FUNC
PyInit_actontext_internal(void)
{
    return PyModule_Create(&actontext);
}

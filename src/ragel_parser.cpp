#include <stdio.h>
#include <helper_string.h>
#include <python2.7/Python.h>

int main(int argc, char **argv) {
    char *strRegex = NULL;

    if (argc > 1) {
        if (checkCmdLineFlag(argc, (const char **) argv, "r")) {
            getCmdLineArgumentString(argc, (const char **)argv, "r", (char **) &strRegex);
        }
    }

    if (strRegex == NULL) {
        printf("Regex not provided... Aborting\n");
        return 1;   
    }

    FILE* file;
    int nPyArgC = 5;
    char *arrPyArgV[5];

    arrPyArgV[0] = "../exec/parse.py";
    arrPyArgV[1] = strRegex;
    arrPyArgV[2] = "../bin/nwa.rl";
    arrPyArgV[3] = "\"../bin/nwa.cpp\"";
    arrPyArgV[4] = "../include/nwa.h";

    Py_SetProgramName(arrPyArgV[0]);
    Py_Initialize();
    PySys_SetArgv(nPyArgC, arrPyArgV);
    file = fopen(arrPyArgV[0],"r");
    PyRun_SimpleFile(file, arrPyArgV[0]);
    Py_Finalize();

    return 0;
}
#include "nwa.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <stdlib.h>
#include <time.h>
#include "helper.h"

#define SUCCESS 0
#define FAILURE 1

int test(vector<long> vecTraceEvents) {
    Automaton *a = new NWParserAutomaton();

    int dimCount = a->dimCount;
    int callCount = a->callCount;

    int permCount = 1;

    // Initialize state storage
    vector<int> symbols(permCount);
    fill(symbols.begin(), symbols.end(), a->getStartState());

    // Initialize call count storage
    vector<vector<int> > callCounts(permCount, vector<int>(callCount, 0));

    int iLoc;
    struct timespec start, stop;
    vector<int> word;
    clock_gettime(CLOCK_REALTIME, &start);

    for (int cnt = 0; cnt < vecTraceEvents.size(); ++cnt) {
        iLoc = vecTraceEvents[cnt];
        int succ = 0;
        int reset = 0;

        // Magic happens here
        a->compute(&(symbols[0]), &(callCounts[0]), succ, reset, iLoc);
        if (succ > 0) {
            word.push_back(iLoc);
            for (int i = 0; i < word.size(); ++i) {
                printf("%d ", word[i]);
            }
            printf("\n");
            word.clear();
        } else if (reset > 0) {
            word.clear();
        } else {
            word.push_back(iLoc);
        }
    }

    clock_gettime( CLOCK_REALTIME, &stop);
    double accum;
    accum = ( stop.tv_sec - start.tv_sec ) + (double)(( stop.tv_nsec - start.tv_nsec ) / BILLION);
    printf("\nTime: %f\n", accum);

    return SUCCESS;
}

int main(int argc, char **argv) {
    char *strRegex = NULL;
    char *strTraceFileName = NULL;
    char *strTrace = NULL;

    if (argc > 1) {
        if (checkCmdLineFlag(argc, (const char **) argv, "f")) {
            getCmdLineArgumentString(argc, (const char **)argv, "f", (char **) &strTraceFileName);
        }

        if (checkCmdLineFlag(argc, (const char **) argv, "e")) {
            getCmdLineArgumentString(argc, (const char **)argv, "e", (char **) &strTrace);
        }
    }

    if (strTraceFileName == NULL && strTrace == NULL) {
        printf("Missing sequence string or sequence file.\n");
        return FAILURE;
    }

    if (strTraceFileName != NULL && strTrace != NULL) {
        printf("Provided sequence string and sequence file. Please provide one.\n");
        return FAILURE;
    }

    vector<long> vecTraceEvents;
    if (strTrace != NULL) {
        stringstream stream(strTrace);
        int n;
        while(stream >> n){
            vecTraceEvents.push_back(n);
        }
    }

    if (strTraceFileName != NULL) {
        ifstream fin(strTraceFileName);
        if (!fin) {
            printf("No valid input file... Aborting\n");
            return FAILURE;
        }

        string item;
        // File format: trace time, trace event\n
        for (string line; getline(fin, line);) {
            istringstream in(line);
            while (getline(in, item, '\n')) {
                stringstream ss(item);
                double i;
                ss >> i;
                vecTraceEvents.push_back(i); 
            }
        }
    }

    return test(vecTraceEvents);
}
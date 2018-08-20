#ifndef NWA_H
#define NWA_H

#include <stdio.h>
#include <vector>
#include <string>
// #include <memory>
#include <cmath>
#include <map>

#include "automaton.h"

using namespace std;

// Macros for compute
#define STATE(x)  currentState = x;

#define RT   for (int i = 0; i < currentCount.size(); i++) {    \
currentCount[i] = 0;                                            \
}                                                               \

#define IN(x) currentCount[x] += 1;

#define DE(x) currentCount[x] -= 1;                             \
if (x == 0 && currentCount[x] == 0) {                           \
success = true;                                                 \
STATE(foo_start);                                               \
RT                                                              \
return;                                                         \
}                                                               \

#define CHK(x) if(currentCount[x] != 0) {                       \
failure = true;                                                 \
STATE(foo_start);                                               \
RT                                                              \
return;                                                         \
}                                                               \

class NWA : public Automaton {
        int callCount;

        vector<int> currentCount;
        bool success;
        bool failure;

    public:
        NWA();

        void compute(const int nextSymbol);
        int getStartState();
        bool isFailure();
        bool isSuccess();
};

#endif

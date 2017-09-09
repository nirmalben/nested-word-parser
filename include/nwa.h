#ifndef AUTOMATON_H
#define AUTOMATON_H

#include <vector>
#include <string>
#include <memory>
#include <stdio.h>
#include <cmath>

using namespace std;

// Macros for compute
#define STATE(x)  *currentState = x;
#define AERROR     stop("Unsupported symbol");

#define RT   for (int i = 0; i < (*currentCount).size(); i++) { \
(*currentCount)[i] = 0;                                   \
}                                                               \

#define PRINTSUCC std::cerr<<"Incr Succ"<<std::endl;

#define IN(x) (*currentCount)[x] += 1;

#define DE(x) (*currentCount)[x] -= 1;                          \
if(x == 0 && (*currentCount)[x] == 0) {\
(succ)++;                                                      \
STATE(foo_start);                                               \
RT                                                              \
return;                                                         \
}                                                               \

#define CHK(x) if((*currentCount)[x] != 0) {                   \
(reset)++;                                                        \
STATE(foo_start);                                                  \
RT                                                                 \
  return;                                                          \
}                                                                  \

// Automaton Super Class
class Automaton {
    public:
        int dimCount;
        int startState;
        int callCount;
        
        Automaton(){}
        
        virtual int getStartState() = 0;
        virtual void compute(int *currentState, vector<int> *currentCount, int &succ, int &reset, const int nextSymbol) = 0;
        virtual ~Automaton(){}
};

// NW Parser Automaton
class NWParserAutomaton: public Automaton {
    public:
        NWParserAutomaton();
        
        void compute(int *currentState, vector<int> *currentCount, int &succ, int &reset, const int nextSymbol);
        int  getStartState();

        virtual ~NWParserAutomaton(){}
};

#endif

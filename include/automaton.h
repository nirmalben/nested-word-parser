#ifndef AUTOMATON_H
#define AUTOMATON_H

class Automaton {
    public:
        int dimCount;
        int startState;
        int currentState;

        Automaton() {}

        virtual int getStartState() = 0;
        virtual void compute(const int nextSymbol) = 0;
        virtual ~Automaton() {}
};

#endif

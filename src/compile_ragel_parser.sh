#!/bin/bash

g++ ragel_parser.cpp -I/opt/include/python2.7 -I../include/ -fno-strict-aliasing -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -L/opt/lib/python2.7/config -lpthread -ldl -lutil -lm -lpython2.7 -Xlinker -export-dynamic -o ragel_parser
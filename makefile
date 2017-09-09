CC = g++

INC := -I./include -g -O3

LIB := -lrt

CFLAGS  = -std=c++0x $(INC) $(LIB)

SOURCE = test

TARGET = test

all: $(TARGET)

$(TARGET): 
	$(CC) $(CFLAGS) -o bin/$(TARGET) src/$(SOURCE).cpp bin/nwa.cpp

clean:
	$(RM) $(TARGET)

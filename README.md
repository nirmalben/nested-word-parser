# nested-word-parser
Tool to parse <a href="https://en.wikipedia.org/wiki/Nested_word" target="_blank">Nested Words</a> in a string. The <a href="https://en.wikipedia.org/wiki/Nested_word#Nested_word_automaton" target="_blank">Nested Word Automaton</a> used for parsing is built using the <a href="http://www.colm.net/open-source/ragel/">Ragel State Machine Compiler</a>. The code demonstrates a way to build the NWA using the Ragel library.
<br>
### Prerequisites
  * Python 3 (Tested on Python 3.4.3)
  * gcc
  * g++
  * <a href="http://www.colm.net/open-source/ragel/">Ragel State Machine Compiler</a>
  * <a href="http://www.swig.org/download.html">SWIG</a>

### Usage
```
$ python3 ./nested_word_parser.py -r <Nested Word Automaton regex> -f <Filename to parse> -i <Absolute location of the Python 3 executable>
```
<br>

**Examples** <br>
* By default, the values of the arguments are as follows:
  ```
  $ python3 ./nested_word_parser.py -r "<0.1.2>" -f "./data/t1.csv" -i "/usr/include/python3.4m"
  0
  0
  1
  2
  0
  Failure
  0
  0
  1
  2
  2
  Success
  ```
* The below line produces the same output as above:
  ```
  $ python3 ./nested_word_parser.py
  ```

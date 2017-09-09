# nested-word-parser
Tool to parse Nested Words in a string. More details on Nested Word can be found <a href="https://en.wikipedia.org/wiki/Nested_word" target="_blank">here</a>. The <a href="https://en.wikipedia.org/wiki/Nested_word#Nested_word_automaton" target="_blank">Nested Word Automaton</a> used for parsing is build using the <a href="http://www.colm.net/open-source/ragel/">Ragel State Machine Compiler</a>.
<br>
### Prerequisites
  * <a href="https://gcc.gnu.org/install/binaries.html">GCC</a>
  * <a href="https://www.python.org/downloads/">Python 2.7</a>
  * <a href="http://www.colm.net/open-source/ragel/">Ragel State Machine Compiler</a>

### Usage 
**Using the shell script** <br>
`./get_nested_words.sh -f <A sequence of numbers file name> -e <A sequence of numbers in double quotes(\"\")> -r <The nested word expression> `
<br><br>
**Note**: Provide either the file containing the sequence or the string containing the sequence 
<br><br>
**Examples** <br>
`./get_nested_words.sh -r \"<0.<1.2>.3>\" -e \"0 1 2 3\"` <br>
`./get_nested_words.sh -r \"<0.<1.2>.3>\" -f \"./data/t2.csv\"`
<br><br>
**Alternative to using the shell script** <br>
The shell script basically runs the following commands<br>
```
$ cd src/
$ ./ragel_parser -r="<The nested word expression>"
$ cd ..
$ make
$ ./bin/main -e="<A sequence of numbers in double quotes>"
```
The last command can be replaced with the following line
```
$ ./bin/main -f="<A sequence of numbers file name>"
```
**Examples** <br>
```
$ cd src/
$ ./ragel_parser -r="<0.<1.2>.3>"
$ cd ..
$ make
$ ./bin/main -e="0 1 2 3"
$ ./bin/main -f="./data/t2.csv"
```

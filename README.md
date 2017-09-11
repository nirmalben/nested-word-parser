# nested-word-parser
Tool to parse <a href="https://en.wikipedia.org/wiki/Nested_word" target="_blank">Nested Words</a> in a string. The <a href="https://en.wikipedia.org/wiki/Nested_word#Nested_word_automaton" target="_blank">Nested Word Automaton</a> used for parsing is built using the <a href="http://www.colm.net/open-source/ragel/">Ragel State Machine Compiler</a>.
<br>
### Prerequisites
  * <a href="https://gcc.gnu.org/install/binaries.html">GCC</a>
  * <a href="https://www.python.org/downloads/">Python 2.7.x</a>
  * <a href="http://www.colm.net/open-source/ragel/">Ragel State Machine Compiler</a>

### Usage 
* **Using the shell script** <br>
     ```
     $ ./get_nested_words.sh -r <The nested word expression> -f <A sequence of numbers file name> -e <A sequence of numbers in double quotes(\"\")> 
     ```
     **Note**: Provide either the file containing the sequence using `-f` or the string containing the sequence using `-e`
     <br><br>
     **Examples** <br>
    ```
    $ ./get_nested_words.sh -r \"<0.<1.2>.3>\" -e \"0 1 2 3\"
    $ ./get_nested_words.sh -r \"<0.<1.2>.3>\" -f \"./data/t1.csv\"
    ```
    <br>
* **Alternative to using the shell script** <br>
    The shell script basically runs the following commands<br>
    ```
    $ cd src/
    $ ./ragel_parser -r="<The nested word expression>"
    $ cd ..
    $ make
    $ ./bin/test -e="<A sequence of numbers>"
    ```
    The last command above can be replaced with the following command if the sequence is stored in a file:
    ```
    $ ./bin/test -f="<A sequence of numbers file name>"
    ```
    **Examples** <br>
    ```
    $ cd src/
    $ ./ragel_parser -r="<0.<1.2>.3>"
    $ cd ..
    $ make
    $ ./bin/test -e="0 1 2 3"
    $ ./bin/test -f="./data/t1.csv"
    ```

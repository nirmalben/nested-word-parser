# ./get_nested_words.sh -r "<0.<1.2>.3>" -e "0 1 2 3"
# ./get_nested_words.sh -r "<0.<1.2>.3>" -f "./data/t2.csv"

#!/bin/bash
usage() { echo -e "\nUsage: \n $0 -f <A sequence of numbers file name> -e <A sequence of numbers in double quotes(\"\")> -r <The nested word expression> \n Provide either the file containing the sequence or the string containing the sequence\n 
 Examples: \n  ./get_nested_words.sh -r \"<0.<1.2>.3>\" -e \"0 1 2 3\"
  ./get_nested_words.sh -r \"<0.<1.2>.3>\" -f \"./data/t2.csv\""; exit 1; }

while getopts ":f:e:r:" o; do
    case "${o}" in
        f)
            f=${OPTARG}
            ;;
        e)
            e=${OPTARG}
            ;;
        r)	
            r=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done

if [ -z "${f}" ] && [ -z "${e}" ]
then
	echo "ERROR: A sequence of numbers file name or string containing the sequence are not given"
    usage
fi

if [ ! -z "${f}" ] && [ ! -z "${e}" ]
then
    echo "ERROR: A sequence of numbers file name and string containing the sequence are given"
    usage
fi

cd src/
./ragel_parser -r=$r
cd ..
set -e
make -s -f makefile

if [ -z "${f}" ]
then
	./bin/main -e="$e"
fi

if [ -z "${e}" ]
then
	./bin/main -f=$f
fi
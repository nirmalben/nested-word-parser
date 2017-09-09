import ragel_parser
import os
import sys

ragel_parser.write_to_file(sys.argv[1], sys.argv[2], sys.argv[4])
cmdString = "ragel -G1 " + sys.argv[2].decode('string_escape') + " -o " + sys.argv[3].decode('string_escape')
os.system(cmdString)

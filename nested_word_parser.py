#!/usr/bin/python3
import sys
import os
import ragel_generator as rg
import argparse
import importlib
import shutil

python_include = ""

def generate_state_machine(nwa_file_name, bin_dir, include_dir):
    rl_file = bin_dir + nwa_file_name + ".rl"
    cpp_file = bin_dir + nwa_file_name + ".cpp"
    header_file = include_dir + nwa_file_name + ".h"

    rg.global_symbols_counter = 0
    rg.global_call_counter = 0
    rg.global_calls_list = []

    rg.write_to_file(regex, rl_file, header_file)
    ragelCmdString = "ragel -G1 " + rl_file + " -o " + cpp_file
    os.system(ragelCmdString)

def generate_swig_interface(nwa_file_name, bin_dir, include_dir, python_include):
    interface_file = open(bin_dir + nwa_file_name + ".i", "w+")
    interface_file.write("%module " + nwa_file_name + "_module\n")
    interface_file.write("%{\n")
    interface_file.write("#include \"" + include_dir + "automaton.h\"\n")
    interface_file.write("#include \"" + include_dir + nwa_file_name + ".h\"\n")
    interface_file.write("%}\n\n")
    interface_file.write("%include \"" + include_dir + "automaton.h\"\n")
    interface_file.write("%include \"" + include_dir + nwa_file_name + ".h\"\n")
    interface_file.close()

    os.chdir(bin_dir)
    os.system("g++ -fpic -c " + nwa_file_name  + ".cpp -o " + nwa_file_name  + ".o -std=c++0x")
    os.system("swig -c++ -python " + nwa_file_name + ".i")
    os.system("g++ -fpic -c "+ nwa_file_name +"_wrap.cxx " + include_dir + nwa_file_name + ".h -I" + python_include)
    os.system("gcc -shared " + nwa_file_name  + ".o " + nwa_file_name + "_wrap.o -o _" + nwa_file_name + "_module.so -lstdc++")

def run(regex, filename):
    current_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + '/'
    bin_dir = script_dir + 'bin/'
    include_dir = script_dir + 'include/'

    if os.path.exists(bin_dir):
        shutil.rmtree(bin_dir)
    os.makedirs(bin_dir)

    nwa_file_name = "nwa"
    generate_state_machine(nwa_file_name, bin_dir, include_dir)
    start_symbol = rg.start_symbol

    generate_swig_interface(nwa_file_name, bin_dir, include_dir, python_include)
    os.chdir(script_dir)

    sys.path.append(bin_dir)
    m = importlib.import_module("_" + nwa_file_name + "_module")

    nwa_class_name = "NWA"
    o = getattr(m, "new_" + nwa_class_name)()
    compute = getattr(m, nwa_class_name + "_compute")
    isSuccess = getattr(m, nwa_class_name + "_isSuccess")
    isFailure = getattr(m, nwa_class_name + "_isFailure")
    destroy = getattr(m, "delete_" + nwa_class_name)

    with open(filename, "r") as seqs_file:
        seqs_lines = seqs_file.readlines()
    seqs_string = [x.strip() for x in seqs_lines]

    seqs = list(map(int, seqs_string))

    for i in range(len(seqs)):
        s = seqs[i]
        compute(o, s)
        print(s)

        success = isSuccess(o)
        failure = isFailure(o)

        if success:
            print("Success")
        elif failure:
            print("Failure")
            if s == start_symbol:
                compute(o, s)
                print(s)

        if i == len(seqs) - 1 and not (success or failure):
            print("Failure")

    destroy(o)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Timed Regular Expression Monitor")
    parser.add_argument('-f', "--filename", default="./data/t1.csv", help='File to parse.')
    parser.add_argument('-r', "--regex", default="<0.1.2>", help='Nested Word Automaton regex.')
    parser.add_argument('-i', "--include", default="/usr/include/python3.4m", help='Absolute location of the Python 3 executable.')

    arguments = parser.parse_args()

    regex = ""
    filename = ""

    if arguments.regex:
        regex = arguments.regex

    if arguments.filename:
        filename = arguments.filename

    if arguments.include:
        python_include = arguments.include

    run(regex, filename)

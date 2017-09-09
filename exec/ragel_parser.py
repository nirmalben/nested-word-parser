import os
import shutil

global_alphabet_counter = 0 # counter for the number of alphabets
global_call_counter = 0 # counter for the number of calls
global_calls_list = []


def parser(input):

    expressions = ["("]
    i = 0
    check_input(input)
    isCall = False

    while i < len(input):
        current_char = input[i]
        if current_char == '<':
            isCall = True
            exp, i, counter, isCall = create_new_expression(input, i + 1, global_call_counter, "", isCall)
            expressions.append(exp)
        else:
            expressions.append(current_char)
        i += 1

    expressions.append(") $~NEXT $lerr(R);")

    return "".join(expressions)


def create_new_expression(input, i, counter, new_exp, isCall):
    global global_call_counter
    global global_calls_list

    new_exp += "("
    interval_str=""
    while i < len(input):
        current_char = input[i]
        if current_char == '<':
            i += 1
            isCall = True
            new_exp, i, counter, isCall = create_new_expression(input, i, counter+1, new_exp, isCall)
        elif current_char == '>':
            new_exp += '+'
            new_exp = embed_actions(new_exp, counter)
            global_call_counter += 1
            return (new_exp, i, counter-1, isCall)
        else:
            new_exp += current_char
            if isCall:
                global_calls_list.append(current_char)
                new_exp += '+'
                isCall = False
        i += 1

    return (new_exp, i, counter, isCall)


def check_input(input):
    global global_alphabet_counter

    opening_count = 0
    closing_count = 0
    alphabets = {}
    intervalMode = False
    dot_count = 0

    for char in input:
        if char == '<':
            opening_count += 1
        if char == '>':
            closing_count += 1
        if char == '.':
            dot_count += 1
        if char.isalpha():
            raise ValueError("The alphabet must be integers only")
        if char.isdigit() and (not intervalMode):
            if int(char) not in alphabets.keys():
                alphabets[int(char)] = 1
       
    alphabets_list = sorted(alphabets.keys())
    global_alphabet_counter = len(alphabets_list)

    if not alphabets_list:
        raise ValueError("The timed regular expression must include at least one alphabet")

    if alphabets_list[0] is not 0:
        raise ValueError("The alphabet must start with 0 and increment by 1.")

    for i in range(1, global_alphabet_counter):
        if alphabets_list[i] - alphabets_list[i-1] > 1:
            raise ValueError("The alphabet must start with 0 and increment by 1.")
    
    if not (dot_count == global_alphabet_counter - 1):
        raise ValueError("Missing '.'")

    if not (opening_count == closing_count):
        raise ValueError("Each '<' must have a matching '>'")

    return


def embed_actions(exp, counter):
    return exp + ") %~DE" + str(counter) + " %CHK" + str(counter) + ""


def create_actions(file, counter):
    for x in range(counter):
        create_action_in(file, x)
        create_action_de(file, x)
        create_action_chk(file, x)

    return

def create_action_in(file, counter):
    file.write("    action IN" + str(counter) + " { IN(" + str(counter) + ") }\n" )
    return

def create_action_de(file, counter):
    file.write("    action DE" + str(counter) + " { DE(" + str(counter) + ") }\n" )
    return

def create_action_chk(file, counter):
    file.write("    action CHK" + str(counter) + " { CHK(" + str(counter) + ") }\n" )
    return

def write_to_file(input, temprl, headerLoc):
    dir = os.getcwd() + "/../bin/"
    if os.path.exists(dir):
       shutil.rmtree(dir) 
    os.makedirs(dir)
    f = open(temprl, "w+")
    ragel_expression = parser(input)
    f.write ("// Generated code\n")
    f.write("#include \"" + str(headerLoc) + "\"\n\n")

    f.write("void NWParserAutomaton::compute(int *currentState, vector<int> *currentCount, int &succ, int &reset, const int nextSymbol) {\n")

    f.write("const int calls[] = {")
    i = 0
    while i < len(global_calls_list):
        f.write(global_calls_list[i])
        if (i != len(global_calls_list) - 1):
            f.write(", ")
        i += 1
    f.write("};\n")

    f.write("%%{\n")


    f.write("    machine foo;\n\n")
    f.write("    action R { reset++; STATE(foo_start); RT return; }\n")

    # add call to IN(x) into NEXT as there is no facility to access the call states specifically
    f.write("    action NEXT { for(int i = 0; i < " + str(global_call_counter) + "; ++i) { if (fc == calls[i]) { IN(i); break; } } STATE(ftargs); return; }\n\n")

    create_actions(f, global_call_counter)

    f.write("\n    getkey nextSymbol;\n")
    f.write("    variable p dummy;\n")
    f.write("    write data;\n\n")
    f.write("}%%\n\n")

    f.write("int cs = *currentState, dummy = 0, eof = -1;\n\n")
    f.write("")
    f.write("%%{\n")
    f.write("    main := " + ragel_expression + "\n")
    f.write("    write init nocs;\n")
    f.write("    write exec noend;\n")
    f.write("}%%\n\n")

    f.write("return; \n\n}\n\n")

    f.write("int NWParserAutomaton::getStartState() {\n")
    f.write("startState = %%{")
    f.write("    write start;")
    f.write("}%%;\n")
    f.write("return startState;\n")
    f.write("}\n\n")

    f.write("NWParserAutomaton::NWParserAutomaton() {\n")
    f.write("   dimCount = " + str(global_alphabet_counter) + ";\n")
    f.write("   callCount = " + str(global_call_counter) + ";\n")
    f.write("}\n")

    return

#!/usr/bin/env python3
import json
import os
import subprocess
import random
import time
import string
MAX_LEN = 1000
MAX_LOOPS = 100000
MAX_TRIES = 1000

import consts_t as K
L_INS = len(K.INSTRUCTIONS)

lua_p = 'compiled.luap'

def generate_random_instruction(): # 4-byte instruction
    for i in range(4): yield random.randint(0, 255)

def create_body(instr_count):
    for k in range(instr_count): yield from generate_random_instruction()


def create_lua_binary_random(instr_count):
    instruction_seq = [j for i in range(instr_count) for j in generate_random_instruction()]
    binary_form = (bytes(K.PREFIX) +
                  (instr_count + 1 + 3).to_bytes(4, byteorder='little') +
                  bytes(instruction_seq + K.PRINT + K.RETURN_INSTRUCTION + K.POSTFIX))
    with open(lua_p, 'bw') as binary_file:
        binary_file.write(binary_form)
    return instruction_seq


def create_lua_binary(instruction_seq):
    instr_count = int(len(instruction_seq) / 4)
    binary_form = (bytes(K.PREFIX) +
                  (instr_count + 1 + 3).to_bytes(4, byteorder='little') +
                  bytes(instruction_seq + K.PRINT + K.RETURN_INSTRUCTION + K.POSTFIX))
    with open(lua_p, 'bw') as binary_file:
        binary_file.write(binary_form)
    return instruction_seq

def execute_binary(instruction_seq):
    try:
        result = subprocess.run(['lua', lua_p], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1)
    except subprocess.TimeoutExpired:
        return 'tmeout'
    stderr = result.stderr.decode("utf-8")
    stdout = result.stdout.decode("utf-8")
    if stdout.strip()[-3:] == 'end':
        return 'incomplete'
    elif stderr.strip() == '':
        return 'complete'
    else:
        return stderr

def validate_lua(input_str, log_level):
    """ return:
        rv: "complete", "incomplete" or "wrong",
        n: the index of the character -1 if not applicable
        c: the character where error happened  "" if not applicable
    """
    try:
        instruction_seq = input_str
        create_lua_binary(instruction_seq)
        output = execute_binary(input_str)
        print(repr(output))
        if output == "complete":
            return "complete",-1,""
        elif output == "incomplete":
            return "incomplete", -1, ""
        else:
            return "wrong", len(input_str), "input_str[-1]"
    except Exception as e:
        msg = str(e)
        print("Can't parse: " + msg)
        n = len(msg)
        return "wrong", n, ""

def get_next_char(log_level, pool):
    if L_INS - len(pool) > MAX_TRIES:
        return None
    print(len(pool), end=' ')
    input_char = pool.pop()
    return input_char

import random

def generate(log_level):
    """
    Feed it one character at a time, and see if the parser rejects it.
    If it does not, then append one more character and continue.
    If it rejects, replace with another character in the set.
    :returns completed string
    """
    prev_str = []
    i = 0
    pool = list(K.INSTRUCTIONS)
    random.shuffle(pool)
    inputs = []
    while i < MAX_LOOPS:
        print('>>', len(inputs))
        i += 1
        char = get_next_char(log_level, pool)
        if not char: break
        curr_str = prev_str + char
        rv, n, c = validate_lua(curr_str, log_level)

        if log_level:
            print("%s n=%d, c=%s. Input string is %s" % (rv,n,c,curr_str))
        if rv == "complete":
            break
        elif rv == "incomplete": # go ahead...
            print('.', end='')
            inputs.append(list(curr_str))
            if len(curr_str) >= MAX_LEN:
                break
            if random.randint(0,1000) == 0:
                # with a 1/1000 probabilyt we mark complete.
                break
            pool = list(K.INSTRUCTIONS)
            random.shuffle(pool)
            prev_str = curr_str
            continue
        elif rv == "wrong": # try again with a new random character do not save current character
            continue
        else:
            print("ERROR What is this I dont know !!!")
            break
    return inputs
import time
def create_valid_strings(n, log_level):
    os.remove("my_valid_inputs.txt") if os.path.exists('my_valid_inputs.txt') else None
    tic = time.time()
    i = 0
    with open("my_valid_inputs.txt", "w+") as myfile:
        while True: # while
            i += 1
            created_strings = generate(log_level)
            toc = time.time()
            for created_string in created_strings:
                var = (f"Time used until input was generated: {toc - tic:f}\n" + repr(created_string) + "\n\n")
                myfile.write(var)
                myfile.flush()

import sys
if __name__ == '__main__':
    #import pudb
    #pudb.set_trace()
    create_valid_strings(10, 0)

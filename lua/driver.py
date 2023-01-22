#!/usr/bin/env python3
import consts as K
import subprocess
import random
import time
import os

MAX_LEN = 1000
MAX_LOOPS = 100000
MAX_TRIES = 10000

L_INS = len(K.INSTRUCTIONS)

lua_p = 'compiled.luap'


def generate_random_instruction():  # 4-byte instruction
    for i in range(4): yield random.randint(0, 255)


def create_body(instr_count):
    for k in range(instr_count): yield from generate_random_instruction()


def create_lua_binary(instruction_seq):
    instr_count = int(len(instruction_seq) / 4)
    binary_form = (bytes(K.PREFIX) +
                   (instr_count + 1 + 3).to_bytes(4, byteorder='little') +
                   bytes(instruction_seq + K.PRINT + K.RETURN_INSTRUCTION + K.POSTFIX))
    with open(lua_p, 'bw') as binary_file:
        binary_file.write(binary_form)
    return instruction_seq


def execute_binary():
    try:
        result = subprocess.run(['lua', lua_p], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1)
    except subprocess.TimeoutExpired:
        return 'tmeout'
    stderr = result.stderr.decode("utf-8")
    if stderr[-3:] == 'end':
        return 'incomplete'
    elif stderr == '':
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
        output = execute_binary()
        print(repr(output))
        if output == "complete":
            return "complete", -1, ""
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


def generate(log_level, misbehaving_ins):
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
    while i < MAX_LOOPS:
        i += 1
        char = get_next_char(log_level, pool)
        if not char:
            misbehaving_ins.append(prev_str)
            return prev_str
        curr_str = prev_str + char
        rv, n, c = validate_lua(curr_str, log_level)

        if log_level:
            print("%s n=%d, c=%s. Input string is %s" % (rv, n, c, curr_str))
        if rv == "complete":
            if random.randrange(5) == 0:
                return curr_str
            else:
                pool = list(K.INSTRUCTIONS)
                random.shuffle(pool)
                prev_str = curr_str
                continue
        elif rv == "incomplete":  # go ahead...
            print('.', end='')
            if len(curr_str) >= MAX_LEN:
                return curr_str
            pool = list(K.INSTRUCTIONS)
            random.shuffle(pool)
            prev_str = curr_str
            continue
        elif rv == "wrong":  # try again with a new random character do not save current character
            continue
        else:
            print("ERROR What is this I dont know !!!")
            break
    return None


def create_valid_strings(n, log_level):
    os.remove("valid_inputs.txt") if os.path.exists('valid_inputs.txt') else None
    os.remove("misbehaving_instructions.txt") if os.path.exists('misbehaving_instructions.txt') else None
    tic = time.time()
    i = 0
    while True:  # while
        i += 1
        misbehaving_ins = []
        created_string = generate(log_level, misbehaving_ins)
        toc = time.time()
        if created_string is not None:
            with open("valid_inputs.txt", "a") as myfile, open("misbehaving_instructions.txt", "a") as file:
                var = f"Time used until input was generated: {toc - tic:f}\n" + repr(created_string) + "\n\n"
                myfile.write(var)
                [file.write(str(char) + "\n") for char in misbehaving_ins]


create_valid_strings(10, 0)

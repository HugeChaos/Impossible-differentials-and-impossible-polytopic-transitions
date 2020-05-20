#!/usr/bin/python
# -*- coding: UTF-8 -*-


import copy
import os
import subprocess


sbox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

perm = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, \
        4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, \
        8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, \
        12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]


def __xor_operate_1(var1, var2, var3):
    return "ASSERT(BVXOR({}, {}) = {});\n".format(var1, var2, var3)


def xor_operate(var1, var2, var3):
    xor_statement = ""
    for var_index in range(0, len(var1)):
        xor_statement += __xor_operate_1(var1[var_index], var2[var_index], var3[var_index])
    return xor_statement


def __sbox_operate1(v1, v2):
    var1 = "{}@{}@{}@{}".format(v1[3], v1[2], v1[1], v1[0])
    var2 = "{}@{}@{}@{}".format(v2[3], v2[2], v2[1], v2[0])
    statement1 = "0bin1100"
    for i in range(1, 16):
        iv = "0bin"
        for j in range(0, 4):
            iv += "{}".format((i >> (3 - j)) & 0x1)
        siv = "0bin"
        for j in range(0, 4):
            siv += "{}".format((sbox[i] >> (3 - j)) & 0x1)
        statement1 = "(IF {} = {} THEN {} ELSE {} ENDIF)".format(var1, iv, siv, statement1)
    statement = "ASSERT({} = {});\n".format(var2, statement1)
    return statement


def sbox_operate(var1, var2):
    s_box_size = 4
    s_box_statement = ""
    for s_box_index in range(0, 16):
        begin_index = s_box_index * s_box_size
        end_index = begin_index + s_box_size
        s_box_statement += __sbox_operate1(var1[begin_index:end_index], var2[begin_index:end_index])
    return s_box_statement


def var_value_assign(var, values):
    statement = ""
    for i in range(0, len(var)):
        statement += "ASSERT({} = 0bin{});\n".format(var[i], values[i])
    return statement


def var_equal(var1, var2):
    statement = ""
    for i in range(0, len(var1)):
        statement += "ASSERT({} = {});\n".format(var1[i], var2[i])
    return statement


def perm_wire(var1):
    var = ["" for i in range(0, len(var1))]
    for i in range(0, len(var1)):
        var[i] = var1[perm[i]]
    return var


def perm_wire_value(var1):
    var = [0 for i in range(0, len(var1))]
    for i in range(0, len(var1)):
        var[perm[i]] = var1[i]
    return var


def header(var1):
    temp1 = ""
    for var in var1:
        temp = var[0]
        for i in range(1, len(var)):
            temp += ", {}".format(var[i])
        temp += " : BITVECTOR(1);\n"
        temp1 += temp
    return temp1


def trailer(v1, va2):
    return "QUERY(FALSE);\nCOUNTEREXAMPLE;"


def state_var_dec(var, round_index, var_size, mul):
    var0 = [["p{}_{}_{}_{}".format(j, var, round_index, i) for i in range(0, var_size)] for j in range(0, mul)]
    return var0


def diff_var_dec(var, round_index, var_size):
    return ["d_{}_{}_{}".format(var, round_index, i) for i in range(0, var_size)]


def key_var_dec(var, round_index, var_size):
    return ["k_{}_{}_{}".format(var, round_index, i) for i in range(0, var_size)]


def solver(solve_file):
    stp_parameters = ["stp", "--minisat", "--CVC", solve_file]
    res = subprocess.check_output(stp_parameters)
    res = res.replace("\r", "")[0:-1]
    print(res)
    if res == "Valid.":
        return True
    else:
        return False


def solver1(solve_file):
    stp_parameters = ["stp", "--minisat", "--CVC", solve_file]
    res = subprocess.check_output(stp_parameters)
    res = res.replace("\r", "")[0:-1]
    print(res)
    if res == "Valid.":
        return True, res
    else:
        return False, res


def values_propagate_phrase0(cd, round_inf):

    statement = ""
    all_var = list()
    key_var = list()
    x = state_var_dec("x", round_inf[0], cd["cipher_size"], cd["mul"])
    begin_values = copy.deepcopy(x)
    for rou in range(round_inf[0], round_inf[1]):
        all_var += copy.deepcopy(x)

        y = state_var_dec("y", rou, cd["cipher_size"], cd["mul"])
        all_var += copy.deepcopy(y)

        rk = copy.deepcopy(key_var_dec("k", rou, 64))
        all_var.append(copy.deepcopy(rk))
        key_var.append(copy.deepcopy(rk))

        for i in range(0, cd["mul"]):
            statement += xor_operate(x[i], copy.deepcopy(rk), y[i])

        x1 = state_var_dec("x", rou + 1, cd["cipher_size"], cd["mul"])

        for i in range(0, cd["mul"]):
            statement += sbox_operate(y[i], copy.deepcopy(perm_wire(x1[i])))
        x = copy.deepcopy(x1)
    all_var += copy.deepcopy(x)

    y = state_var_dec("y", round_inf[1], cd["cipher_size"], cd["mul"])
    all_var += copy.deepcopy(y)

    rk = copy.deepcopy(key_var_dec("k", round_inf[1], 64))
    all_var.append(copy.deepcopy(rk))
    key_var.append(copy.deepcopy(rk))

    for i in range(0, cd["mul"]):
        statement += xor_operate(x[i], copy.deepcopy(rk), y[i])

    end_values = copy.deepcopy(y)
    return begin_values, end_values, all_var, key_var, statement


def get_key_schedule_constant(num):
    li = []
    for i in range(0, 5):
        li.append((num >> i) & 0x1)
    return li


def key_schedule(key_var):
    statement = ""
    for rou in range(0, len(key_var) - 1):
        constant_list = get_key_schedule_constant(rou + 1)
        shift_key = ["" for ii in range(0, 80)]
        for ii in range(0, 80):
            shift_key[ii] = key_var[rou][(ii + 19) % 80]
        i_count = 0
        for i in range(0, 76):
            if i in [15, 16, 17, 18, 19]:
                statement += "ASSERT(BVXOR({}, {}) = 0bin{});\n".format(shift_key[i], key_var[rou + 1][i], constant_list[i_count])
                i_count += 1
            else:
                statement += "ASSERT({} = {});\n".format(key_var[rou + 1][i], shift_key[i])
        statement += __sbox_operate1(copy.deepcopy(shift_key[76:80]), copy.deepcopy(key_var[rou + 1][76:80]))
    return statement


def __mb_mode1(cd, mode):
    statement = ""

    begin_values, end_values, all_var, key_var, statement1 = values_propagate_phrase0(cd, [mode[1][0], mode[1][1]])

    statement += header(all_var)
    for i in range(1, cd["mul"]):
        statement += xor_operate(begin_values[0], begin_values[i], ["0bin{}".format(cd["b{}".format(i)][j]) for j in range(0, len(cd["b{}".format(i)]))])

    statement += statement1

    for i in range(1, cd["mul"]):
        statement += xor_operate(end_values[0], end_values[i], ["0bin{}".format(cd["e{}".format(i)][j]) for j in range(0, len(cd["e{}".format(i)]))])

    statement += trailer([], [])

    f = open(cd["solve_file1"], "a")
    f.write(statement)
    f.close()


def model_build(cd, mode):
    if os.path.exists(cd["solve_file1"]):
        os.remove(cd["solve_file1"])
    if mode[0] == 1:
        __mb_mode1(cd, mode)

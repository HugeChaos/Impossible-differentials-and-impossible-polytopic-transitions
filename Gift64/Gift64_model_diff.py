#!/usr/bin/python
# -*- coding: UTF-8 -*-


import copy
import os
import subprocess


sbox_ddt = [[-1, -1, -1, 1, 0, 0, -1, 0], \
            [1, -1, 1, 0, -1, 1, -1, 0], \
            [1, 1, 1, 0, -1, -1, 1, -1], \
            [0, 1, 1, 0, -1, -1, -1, 1], \
            [1, 1, -1, -1, 0, 1, 1, -1], \
            [0, 1, -1, -1, 0, 1, -1, 1], \
            [1, -1, -1, -1, 0, -1, -1, 0], \
            [-1, 0, 0, 0, 1, -1, 1, -1], \
            [0, 1, 0, 1, -1, 0, 1, 1], \
            [0, 0, 0, -1, 1, 1, 1, 1], \
            [0, -1, 0, -1, 1, 0, -1, -1], \
            [0, 1, 1, 1, 0, 0, 1, -1], \
            [1, 0, 0, 0, 1, 1, 1, -1], \
            [0, 1, -1, 0, 1, 0, 1, 1], \
            [1, 0, 0, 0, 1, -1, 1, 1], \
            [-1, -1, 1, 1, 0, 0, 0, -1], \
            [1, 1, 0, 0, 1, 0, -1, -1], \
            [0, -1, 0, 0, 1, -1, -1, 1], \
            [1, 0, 0, 1, -1, 0, -1, -1], \
            [0, 1, 0, 0, 1, 1, -1, 1], \
            [1, -1, -1, 1, 0, 0, 1, 0], \
            [1, -1, 1, 1, 0, 0, 0, 1], \
            [0, 1, 1, 1, 0, 0, -1, 1], \
            [-1, -1, 0, -1, -1, 0, 1, 1], \
            [-1, 1, 0, 0, 1, 0, 1, 1], \
            [-1, 1, 0, -1, -1, 0, -1, -1], \
            [0, 1, -1, 1, 0, 0, -1, -1], \
            [0, -1, 0, 0, 1, 1, 1, 1], \
            [-1, 0, 1, 0, -1, 1, 1, -1], \
            [-1, 0, -1, -1, 0, -1, 1, -1], \
            [1, -1, 1, -1, 0, 1, 0, -1], \
            [1, -1, -1, 0, -1, -1, 0, -1], \
            [-1, 0, 1, -1, -1, -1, -1, 1], \
            [-1, 0, -1, -1, -1, 1, -1, 1]]

perm = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3, \
        4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7, \
        8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11, \
        12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]


def __xor_operate_1(var1, var2, var3):
    return "ASSERT(BVXOR({}, {}) = {});\n".format(var1, var2, var3)


def xor_operate(var1, var2, var3):
    xor_statement = ""
    for var_index in range(0, len(var1)):
        xor_statement += __xor_operate_1(var1[var_index], var2[var_index], var3[var_index])
    return xor_statement


def __sbox_operate1(var1, var2):
    s_box_size = len(var1)
    s_box_statement = ""
    for row in sbox_ddt:
        temp = ""
        for u in range(0, s_box_size):
            if row[u] == 1:
                temp += "{}|".format(var1[s_box_size - 1 - u])
            elif row[u] == -1:
                temp += "(~{})|".format(var1[s_box_size - 1 - u])
        for v in range(0, s_box_size):
            if row[v + s_box_size] == 1:
                temp += "{}|".format(var2[s_box_size - 1 - v])
            elif row[v + s_box_size] == -1:
                temp += "(~{})|".format(var2[s_box_size - 1 - v])
        temp = temp[0:-1]
        s_box_statement += "ASSERT(({}) = 0bin1);\n".format(temp)
    return s_box_statement


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


def state_var_dec(var, round_index, var_size):
    var0 = ["p0_{}_{}_{}".format(var, round_index, i) for i in range(0, var_size)]
    var1 = ["p1_{}_{}_{}".format(var, round_index, i) for i in range(0, var_size)]
    return var0, var1


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
    all_var = []
    x = diff_var_dec("x", round_inf[0], cd["cipher_size"])
    begin_values = copy.deepcopy(x)
    for rou in range(round_inf[0], round_inf[1]):
        all_var.append(copy.deepcopy(x))
        x1 = diff_var_dec("x", rou + 1, cd["cipher_size"])
        z0 = perm_wire(x1)
        statement += sbox_operate(x, z0)
        x = copy.deepcopy(x1)
    all_var.append(copy.deepcopy(x))
    end_values = copy.deepcopy(x)
    return begin_values, end_values, all_var, statement


def __mb_mode1(cd, mode):
    statement = ""

    begin_values, end_values, all_var, statement1 = values_propagate_phrase0(cd, [mode[1][0], mode[1][1]])

    statement += header(all_var)

    statement += var_value_assign(begin_values, cd["b1"])

    statement += statement1

    statement += var_value_assign(end_values, cd["e1"])

    statement += trailer([], [])

    f = open(cd["solve_file1"], "a")
    f.write(statement)
    f.close()


def model_build(cd, mode):
    if os.path.exists(cd["solve_file1"]):
        os.remove(cd["solve_file1"])
    if mode[0] == 1:
        __mb_mode1(cd, mode)

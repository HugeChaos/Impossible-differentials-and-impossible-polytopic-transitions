#!/usr/bin/python
# -*- coding: UTF-8 -*-


import copy
import os
import subprocess


sbox = [0x1, 0xa, 0x4, 0xc, 0x6, 0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe]

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


def __sbox_operate1(v1, v2):
    var1 = "{}@{}@{}@{}".format(v1[3], v1[2], v1[1], v1[0])
    var2 = "{}@{}@{}@{}".format(v2[3], v2[2], v2[1], v2[0])
    statement1 = "0bin0001"
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
    var = ["" for i in range(0, len(var1))]
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
    var = [["p{}_{}_{}_{}".format(j, var, round_index, i) for i in range(0, var_size)] for j in range(0, mul)]
    return var


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

    rc = [0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F, 0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E]
    round_rc = []
    for i in range(0, 16):
        sub_rc = [0 for k in range(0, 6)]
        for j in range(0, 6):
            sub_rc[j] = (rc[i] >> j) & 0x1
        sub_rc.append(1)
        round_rc.append(sub_rc)
    i_position = [3, 7, 11, 15, 19, 23, 63]

    mk = key_var_dec("k", 0, 128)
    split_key = [["" for j in range(0, 16)] for i in range(0, 8)]
    split_key_t = [["" for j in range(0, 16)] for i in range(0, 8)]

    round_key = []
    for i in range(0, 8):
        split_key[i] = copy.deepcopy(mk[(16*i):(16*i + 16)])
    for rou in range(0, round_inf[1] + 1):
        round_key.append(copy.deepcopy(split_key[0] + split_key[1]))
        for j in range(0, 16):
            split_key_t[7][j] = split_key[1][(j+2) % 16]
            split_key_t[6][j] = split_key[0][(j + 12) % 16]
            split_key_t[5][j] = split_key[7][j]
            split_key_t[4][j] = split_key[6][j]
            split_key_t[3][j] = split_key[5][j]
            split_key_t[2][j] = split_key[4][j]
            split_key_t[1][j] = split_key[3][j]
            split_key_t[0][j] = split_key[2][j]
        split_key = copy.deepcopy(split_key_t)

    statement = ""
    all_var = [copy.deepcopy(mk)]

    x = state_var_dec("x", round_inf[0], cd["cipher_size"], cd["mul"])
    begin_values = copy.deepcopy(x)
    for rou in range(round_inf[0], round_inf[1]):
        all_var += copy.deepcopy(x)
        k = copy.deepcopy(round_key[rou])

        y = state_var_dec("y", rou, cd["cipher_size"], cd["mul"])
        all_var += copy.deepcopy(y)
        for m in range(0, cd["mul"]):

            key_count = 0
            i_position_count = 0
            for i in range(0, cd["cipher_size"]):
                if (i % 4 == 0) or (i % 4 == 1):

                    statement += "ASSERT(BVXOR({}, {}) = {});\n".format(x[m][i], k[key_count], y[m][i])
                    key_count += 1
                elif i in i_position:
                    statement += "ASSERT(BVXOR({}, {}) = 0bin{});\n".format(x[m][i], y[m][i], round_rc[rou][i_position_count])
                    i_position_count += 1
                else:
                    statement += "ASSERT({} = {});\n".format(x[m][i], y[m][i])

        x1 = state_var_dec("x", rou + 1, cd["cipher_size"], cd["mul"])
        for m in range(0, cd["mul"]):
            zm = perm_wire(x1[m])
            statement += sbox_operate(y[m], zm)
        x = copy.deepcopy(x1)
    all_var += copy.deepcopy(x)
    k = round_key[round_inf[1]]

    y = state_var_dec("y", round_inf[1], cd["cipher_size"], cd["mul"])
    all_var += copy.deepcopy(y)

    for m in range(0, cd["mul"]):
        key_count = 0
        i_position_count = 0
        for i in range(0, cd["cipher_size"]):
            if (i % 4 == 0) or (i % 4 == 1):
                statement += "ASSERT(BVXOR({}, {}) = {});\n".format(x[m][i], k[key_count], y[m][i])
                key_count += 1
            elif i in i_position:
                statement += "ASSERT(BVXOR({}, {}) = 0bin{});\n".format(x[m][i], y[m][i], round_rc[round_inf[1]][i_position_count])
                i_position_count += 1
            else:
                statement += "ASSERT({} = {});\n".format(x[m][i], y[m][i])

    end_values = copy.deepcopy(y)
    return begin_values, end_values, all_var, statement


def __mb_mode1(cd, mode):
    statement = ""

    begin_values, end_values, all_var, statement1 = values_propagate_phrase0(cd, [mode[1][0], mode[1][1]])

    statement += header(all_var)

    for i in range(1, cd["mul"]):
        statement += xor_operate(begin_values[0], begin_values[i], ["0bin{}".format(cd["b{}".format(i)][j]) for j in range(0, len(cd["b{}".format(i)]))])

    statement += statement1

    for i in range(1, cd["mul"]):
        statement += xor_operate(end_values[0], end_values[i], ["0bin{}".format(cd["e{}".format(i)][j]) for j in range(0, len(cd["b{}".format(i)]))])

    statement += trailer([], [])

    f = open(cd["solve_file"], "a")
    f.write(statement)
    f.close()


def model_build(cd, mode):
    if os.path.exists(cd["solve_file"]):
        os.remove(cd["solve_file"])
    if mode[0] == 1:
        __mb_mode1(cd, mode)


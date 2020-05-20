#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import os
import subprocess

alpha0 = [[0, 0, 1, 0],
          [0, 1, 0, 0],
          [0, 0, 1, 1],
          [1, 1, 1, 1]]

alpha1 = [[0, 1, 1, 0],
          [1, 0, 1, 0],
          [1, 0, 0, 0],
          [1, 0, 0, 0]]

alpha2 = [[1, 0, 0, 0],
          [0, 1, 0, 1],
          [1, 0, 1, 0],
          [0, 0, 1, 1]]

alpha3 = [[0, 0, 0, 0],
          [1, 0, 0, 0],
          [1, 1, 0, 1],
          [0, 0, 1, 1]]

alpha4 = [[0, 0, 0, 1],
          [0, 0, 1, 1],
          [0, 0, 0, 1],
          [1, 0, 0, 1]]

alpha5 = [[1, 0, 0, 0],
          [1, 0, 1, 0],
          [0, 0, 1, 0],
          [1, 1, 1, 0]]

alpha6 = [[0, 0, 0, 0],
          [0, 0, 1, 1],
          [0, 1, 1, 1],
          [0, 0, 0, 0]]

alpha7 = [[0, 1, 1, 1],
          [0, 0, 1, 1],
          [0, 1, 0, 0],
          [0, 1, 0, 0]]

alpha8 = [[1, 0, 1, 0],
          [0, 1, 0, 0],
          [0, 0, 0, 0],
          [1, 0, 0, 1]]


def squ_xor(x, y, z):
    statement = ""
    for i in range(0, 4):
        for j in range(0, 4):
            statement += "ASSERT(BVXOR({}, {})= {});\n".format(x[i][j], y[i][j], z[i][j])
    return statement


def squ_xor_constant(x, y, values):
    statement = ""
    for i in range(0, 4):
        for j in range(0, 4):
            bin_value = "0bin"
            for ii in range(0, 4):
                bin_value += "{}".format((values[i][j] >> ii) & 0x1)
            statement += "ASSERT(BVXOR({}, {})= {});\n".format(x[i][j], y[i][j], bin_value)
    return statement


def mix_column(x, y):
    statement = ""
    for c in range(0, 4):
        statement += "ASSERT(BVXOR({}, BVXOR({}, {})) = {});\n".format(x[1][c], x[2][c], x[3][c], y[0][c])
        statement += "ASSERT(BVXOR({}, BVXOR({}, {})) = {});\n".format(x[0][c], x[2][c], x[3][c], y[1][c])
        statement += "ASSERT(BVXOR({}, BVXOR({}, {})) = {});\n".format(x[0][c], x[1][c], x[3][c], y[2][c])
        statement += "ASSERT(BVXOR({}, BVXOR({}, {})) = {});\n".format(x[0][c], x[1][c], x[2][c], y[3][c])
    return statement


def shuffle_cell(x):
    sc = [0, 10, 5, 15, 14, 4, 11, 1, 9, 3, 12, 6, 7, 13, 2, 8]
    y = [["" for jj in range(0, 4)] for ii in range(0, 4)]
    for i in range(0, 16):
        y[sc[i] % 4][sc[i] // 4] = x[i % 4][i // 4]
    return y


def __sbox_operate1(v1, v2):
    sbox = [0xc, 0xa, 0xd, 3, 0xe, 0xb, 0xf, 7, 8, 9, 1, 5, 0, 2, 4, 6]
    statement1 = "0bin1100"
    for i in range(1, 16):
        iv = "0bin"
        for j in range(0, 4):
            iv += "{}".format((i >> (3 - j)) & 0x1)
        siv = "0bin"
        for j in range(0, 4):
            siv += "{}".format((sbox[i] >> (3 - j)) & 0x1)
        statement1 = "(IF {} = {} THEN {} ELSE {} ENDIF)".format(v1, iv, siv, statement1)
    statement = "ASSERT({} = {});\n".format(v2, statement1)
    return statement


def sbox_operate(var1, var2):
    statement = ""
    for i in range(0, 4):
        for j in range(0, 4):
            statement += __sbox_operate1(var1[i][j], var2[i][j])
    return statement


def var_value_assign(var, values):
    statement = ""
    for i in range(0, 4):
        for j in range(0, 4):
            bin_value = "0bin"
            for ii in range(0, 4):
                bin_value += (values[i][j] >> ii) & 0x1
            statement += "ASSERT({} = {});\n".format(var[i][j], bin_value)
    return statement


def var_equal(var1, var2):
    statement = ""
    for i in range(0, 4):
        for j in range(0, 4):
            statement += "ASSERT({} = {});\n".format(var1[i][j], var2[i][j])
    return statement


def header(var1):
    temp1 = ""
    for var in var1:
        temp = var[0][0]
        for i in range(0, 4):
            for j in range(0, 4):
                if (i == 0) and (j == 0):
                    continue
                temp += ", {}".format(var[i][j])
        temp += " : BITVECTOR(4);\n"
        temp1 += temp
    return temp1


def trailer(v1, va2):
    return "QUERY(FALSE);\nCOUNTEREXAMPLE;"


def state_var_dec(var, round_index, mul):
    var0 = [[["p{}_{}_{}_{}_{}".format(m, var, round_index, i, j) for i in range(0, 4)] for j in range(0, 4)] for m in range(0, mul)]
    return var0


def key_var_dec(var, round_index):
    return [["k_{}_{}_{}_{}".format(var, round_index, i, j) for j in range(0, 4)] for i in range(0, 4)]


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

    alpha = [alpha0, alpha1, alpha2, alpha3, alpha4, alpha5, alpha6, alpha7, alpha8]

    k0 = key_var_dec("k0", 0)
    k1 = key_var_dec("k1", 0)
    all_var.append(k0)
    all_var.append(k1)

    x = state_var_dec("x", round_inf[0], cd["mul"])
    begin_values = copy.deepcopy(x)

    for rou in range(round_inf[0], round_inf[1]):
        all_var += copy.deepcopy(x)
        y = state_var_dec("y", rou, cd["mul"])
        all_var += copy.deepcopy(y)
        if rou == 0:
            for m in range(0, cd["mul"]):
                for i in range(0, 4):
                    for j in range(0, 4):
                        statement += "ASSERT(BVXOR({}, BVXOR({}, {}))= {});\n".format(x[m][i][j], k0[i][j], k1[i][j], y[m][i][j])
        elif rou % 2 == 1:
            for m in range(0, cd["mul"]):
                for i in range(0, 4):
                    for j in range(0, 4):
                        statement += "ASSERT(BVXOR({}, BVXOR({}, 0bin000{}))= {});\n".format(x[m][i][j], k0[i][j],
                                                                                              alpha[rou - 1][i][j], y[m][i][j])
        else:
            for m in range(0, cd["mul"]):
                for i in range(0, 4):
                    for j in range(0, 4):
                        statement += "ASSERT(BVXOR({}, BVXOR({}, 0bin000{}))= {});\n".format(x[m][i][j], k1[i][j],
                                                                                              alpha[rou - 1][i][j], y[m][i][j])
        z = state_var_dec("z", rou, cd["mul"])
        all_var += copy.deepcopy(z)

        for m in range(0, cd["mul"]):

            statement += sbox_operate(y[m], shuffle_cell(z[m]))

        x1 = state_var_dec("x", rou + 1, cd["mul"])

        for m in range(0, cd["mul"]):
            statement += mix_column(z[m], x1[m])

        x = copy.deepcopy(x1)
    all_var += copy.deepcopy(x)
    y = state_var_dec("y", round_inf[1], cd["mul"])
    all_var += copy.deepcopy(y)
    if round_inf[1] == 0:
        for m in range(0, cd["mul"]):
            for i in range(0, 4):
                for j in range(0, 4):
                    statement += "ASSERT(BVXOR({}, BVXOR({}, {}))= {});\n".format(x[m][i][j], k0[i][j], k1[i][j], y[m][i][j])
    elif round_inf[1] % 2 == 1:
        for m in range(0, cd["mul"]):
            for i in range(0, 4):
                for j in range(0, 4):
                    statement += "ASSERT(BVXOR({}, BVXOR({}, 0bin000{}))= {});\n".format(x[m][i][j], k0[i][j],
                                                                                          alpha[round_inf[1] - 1][i][j], y[m][i][j])
    else:
        for m in range(0, cd["mul"]):
            for i in range(0, 4):
                for j in range(0, 4):
                    statement += "ASSERT(BVXOR({}, BVXOR({}, 0bin000{}))= {});\n".format(x[m][i][j], k1[i][j],
                                                                                          alpha[round_inf[1] - 1][i][j], y[m][i][j])

    end_values = copy.deepcopy(y)
    return begin_values, end_values, all_var, statement


def __mb_mode1(cd, mode):
    statement = ""

    begin_values, end_values, all_var, statement1 = values_propagate_phrase0(cd, [mode[1][0], mode[1][1]])
    statement += header(all_var)

    for i in range(1, cd["mul"]):
        statement += squ_xor_constant(begin_values[0], begin_values[i], cd["b{}".format(i)])

    statement += statement1

    for i in range(1, cd["mul"]):
        statement += squ_xor_constant(end_values[0], end_values[i], cd["e{}".format(i)])

    statement += trailer([], [])

    f = open(cd["solve_file"], "a")
    f.write(statement)
    f.close()


def model_build(cd, mode):
    if os.path.exists(cd["solve_file"]):
        os.remove(cd["solve_file"])
    if mode[0] == 1:
        __mb_mode1(cd, mode)






















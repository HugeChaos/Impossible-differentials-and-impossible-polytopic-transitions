#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "HugeChaos"


import model_build.primitives_rules_sat as mp
import copy, os


def values_propagate_phrase0(cd, round_inf):
    statement = ""
    all_var = []

    x = mp.list2square2(mp.var_dec("state", "x", round_inf[0] + 1, cd["cipher_size"]), cd["sp"])
    all_var += copy.deepcopy(x)
    begin_values = copy.deepcopy(x)

    k = mp.list2square(mp.var_dec("key", "k", round_inf[0] + 1, cd["cipher_size"]), cd["sp"])
    all_var.append(copy.deepcopy(k))
    y = mp.list2square2(mp.var_dec("state", "y", round_inf[0] + 1, cd["cipher_size"]), cd["sp"])
    all_var += copy.deepcopy(y)
    statement += mp.s_operate_all("xor", [x[0], k, y[0]])
    statement += mp.s_operate_all("xor", [x[1], k, y[1]])
    z = mp.list2square2(mp.var_dec("state", "z", round_inf[0] + 1, cd["cipher_size"]), cd["sp"])
    all_var += copy.deepcopy(z)
    w0 = mp.s_operate_all("shift_row", [z[0], cd["constant"]])
    w1 = mp.s_operate_all("shift_row", [z[1], cd["constant"]])

    statement += mp.s_operate_all("s_box", [y[0], w0, cd["sbox_logic"]])
    statement += mp.s_operate_all("s_box", [y[1], w1, cd["sbox_logic"]])

    x = mp.list2square2(mp.var_dec("state", "x", round_inf[0] + 2, cd["cipher_size"]), cd["sp"])

    statement += mp.s_operate_all("mc", [z[0], x[0], cd["mix_column"]])
    statement += mp.s_operate_all("mc", [z[1], x[1], cd["mix_column"]])

    for rou in range(round_inf[0] + 2, round_inf[1] - 2):
        all_var += copy.deepcopy(x)

        k = mp.list2square(mp.var_dec("key", "k", rou, cd["cipher_size"]), cd["sp"])

        all_var.append(copy.deepcopy(k))

        y = mp.list2square2(mp.var_dec("state", "y", rou, cd["cipher_size"]), cd["sp"])

        all_var += copy.deepcopy(y)

        statement += mp.s_operate_all("xor", [x[0], k, y[0]])
        statement += mp.s_operate_all("xor", [x[1], k, y[1]])

        z = mp.list2square2(mp.var_dec("state", "z", rou, cd["cipher_size"]), cd["sp"])
        all_var += copy.deepcopy(z)

        w0 = mp.s_operate_all("shift_row", [z[0], cd["constant"]])
        w1 = mp.s_operate_all("shift_row", [z[1], cd["constant"]])

        statement += mp.s_operate_all("s_box", [y[0], w0, cd["sbox_logic"]])
        statement += mp.s_operate_all("s_box", [y[1], w1, cd["sbox_logic"]])

        x1 = mp.list2square2(mp.var_dec("state", "x", rou + 1, cd["cipher_size"]), cd["sp"])

        statement0 = mp.s_operate_all("mc", [z[0], x1[0], cd["mix_column"]])
        statement1 = mp.s_operate_all("mc", [z[1], x1[1], cd["mix_column"]])

        statement += statement0
        statement += statement1

        x = copy.deepcopy(x1)
    all_var += copy.deepcopy(x)

    k = mp.list2square(mp.var_dec("key", "k", round_inf[1] - 2, cd["cipher_size"]), cd["sp"])
    all_var.append(copy.deepcopy(k))

    y = mp.list2square2(mp.var_dec("state", "y", round_inf[1] - 2, cd["cipher_size"]), cd["sp"])
    all_var += copy.deepcopy(y)

    statement += mp.s_operate_all("xor", [x[0], k, y[0]])
    statement += mp.s_operate_all("xor", [x[1], k, y[1]])

    end_values = copy.deepcopy(y)

    return begin_values, end_values, all_var, statement


def __sbox_operate1(var1, var2, s_box_logic_express):
    s_box_size = len(var1)
    s_box_statement = ""
    for row in s_box_logic_express:
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


def word_xor(var1, var2, var3):
    statement = ""
    for i in range(0, 8):
        statement += "ASSERT(BVXOR({}, {}) = {});\n".format(var1[i], var2[i], var3[i])
    return statement


def word_value(var1, var2, var3):
    statement = ""
    for i in range(0, 8):
        statement += "ASSERT(BVXOR({}, {}) = 0bin{});\n".format(var1[i], var2[i], var3[i])
    return statement


def key_r(cd):
    statement = ""
    k1 = mp.list2square(mp.var_dec("key", "k", 1, cd["cipher_size"]), cd["sp"])
    k2 = mp.list2square(mp.var_dec("key", "k", 2, cd["cipher_size"]), cd["sp"])
    kt1 = [["t1_{}_{}".format(i, j) for j in range(0, 8)] for i in range(0, 5)]

    statement += __sbox_operate1(k1[1][3], kt1[0], cd["sbox_logic"])
    statement += __sbox_operate1(k1[2][3], kt1[2], cd["sbox_logic"])
    statement += __sbox_operate1(k1[3][3], kt1[3], cd["sbox_logic"])
    statement += __sbox_operate1(k1[0][3], kt1[4], cd["sbox_logic"])
    statement += word_value(kt1[0], kt1[1], [0, 1, 0, 0, 0, 0, 0, 0])
    statement += word_xor(k1[0][0], kt1[1], k2[0][0])
    statement += word_xor(k1[1][0], kt1[2], k2[1][0])
    statement += word_xor(k1[2][0], kt1[3], k2[2][0])
    statement += word_xor(k1[3][0], kt1[4], k2[3][0])

    statement += word_xor(k1[0][1], k2[0][0], k2[0][1])
    statement += word_xor(k1[1][1], k2[1][0], k2[1][1])
    statement += word_xor(k1[2][1], k2[2][0], k2[2][1])
    statement += word_xor(k1[3][1], k2[3][0], k2[3][1])

    statement += word_xor(k1[0][2], k2[0][1], k2[0][2])
    statement += word_xor(k1[1][2], k2[1][1], k2[1][2])
    statement += word_xor(k1[2][2], k2[2][1], k2[2][2])
    statement += word_xor(k1[3][2], k2[3][1], k2[3][2])

    statement += word_xor(k1[0][3], k2[0][2], k2[0][3])
    statement += word_xor(k1[1][3], k2[1][2], k2[1][3])
    statement += word_xor(k1[2][3], k2[2][2], k2[2][3])
    statement += word_xor(k1[3][3], k2[3][2], k2[3][3])

    k3 = mp.list2square(mp.var_dec("key", "k", 3, cd["cipher_size"]), cd["sp"])
    kt = [["t2_{}_{}".format(i, j) for j in range(0, 8)] for i in range(0, 5)]
    statement += __sbox_operate1(k2[1][3], kt[0], cd["sbox_logic"])
    statement += __sbox_operate1(k2[2][3], kt[2], cd["sbox_logic"])
    statement += __sbox_operate1(k2[3][3], kt[3], cd["sbox_logic"])
    statement += __sbox_operate1(k2[0][3], kt[4], cd["sbox_logic"])
    statement += word_value(kt[0], kt[1], [0, 0, 1, 0, 0, 0, 0, 0])
    statement += word_xor(k2[0][0], kt[1], k3[0][0])
    statement += word_xor(k2[1][0], kt[2], k3[1][0])
    statement += word_xor(k2[2][0], kt[3], k3[2][0])
    statement += word_xor(k2[3][0], kt[4], k3[3][0])

    statement += word_xor(k2[0][1], k3[0][0], k3[0][1])
    statement += word_xor(k2[1][1], k3[1][0], k3[1][1])
    statement += word_xor(k2[2][1], k3[2][0], k3[2][1])
    statement += word_xor(k2[3][1], k3[3][0], k3[3][1])

    statement += word_xor(k2[0][2], k3[0][1], k3[0][2])
    statement += word_xor(k2[1][2], k3[1][1], k3[1][2])
    statement += word_xor(k2[2][2], k3[2][1], k3[2][2])
    statement += word_xor(k2[3][2], k3[3][1], k3[3][2])

    statement += word_xor(k2[0][3], k3[0][2], k3[0][3])
    statement += word_xor(k2[1][3], k3[1][2], k3[1][3])
    statement += word_xor(k2[2][3], k3[2][2], k3[2][3])
    statement += word_xor(k2[3][3], k3[3][2], k3[3][3])

    var = ", ".join(kt[0] + kt[1] + kt[2] + kt[3] + kt[4])
    var += " : BITVECTOR(1);\n"

    var1 = ", ".join(kt1[0] + kt1[1] + kt1[2] + kt1[3] + kt1[4])
    var1 += " : BITVECTOR(1);\n"

    return statement, var, var1


def __mb_mode1(cd, mode):
    statement = ""

    begin_values, end_values, all_var, statement1 = values_propagate_phrase0(cd, [mode[1][0], mode[1][1]])
    statement2, var1, var2 = key_r(cd)

    dx0 = mp.list2square(mp.s_var_dec("diff", "x", mode[1][0], cd["cipher_size"]), cd["sp"])
    dxn = mp.list2square(mp.s_var_dec("diff", "x", mode[1][1], cd["cipher_size"]), cd["sp"])

    all_var.append(dx0)
    all_var.append(dxn)

    statement += mp.s_operate_all("header", all_var)
    statement += var1
    statement += var2

    statement += statement2

    dx = mp.list2square(mp.s_var_dec("diff", "x", mode[1][0], cd["cipher_size"]), cd["sp"])

    statement += mp.s_operate_all("xor", [begin_values[0], begin_values[1], dx])

    statement += mp.s_operate_all("var_value_assign", [dx, cd["b1"]])

    statement += statement1

    dx = mp.list2square(mp.s_var_dec("diff", "x", mode[1][1], cd["cipher_size"]), cd["sp"])

    statement += mp.s_operate_all("xor", [end_values[0], end_values[1], dx])

    statement += mp.s_operate_all("var_value_assign", [dx, cd["e1"]])

    statement += mp.s_operate_all("trailer", [[], []])

    f = open(cd["solve_file"], "a")
    f.write(statement)
    f.close()


def model_build(cd, mode):
    if os.path.exists(cd["solve_file"]):
        os.remove(cd["solve_file"])
    if mode[0] == 1:
        __mb_mode1(cd, mode)

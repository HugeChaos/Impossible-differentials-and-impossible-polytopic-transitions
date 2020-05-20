#!/usr/bin/python
# -*- coding: UTF-8 -*-


import copy
import os
import subprocess


sbox = [0, 1, 3, 6, 7, 4, 5, 2]


rc = [[1, 0, 0, 0, 0, 0], \
      [1, 1, 0, 0, 0, 0], \
      [1, 1, 1, 0, 0, 0], \
      [1, 1, 1, 1, 0, 0], \
      [1, 1, 1, 1, 1, 0], \
      [0, 1, 1, 1, 1, 1], \
      [1, 0, 1, 1, 1, 1], \
      [1, 1, 0, 1, 1, 1], \
      [1, 1, 1, 0, 1, 1], \
      [1, 1, 1, 1, 0, 1], \
      [0, 1, 1, 1, 1, 0], \
      [0, 0, 1, 1, 1, 1], \
      [1, 0, 0, 1, 1, 1], \
      [1, 1, 0, 0, 1, 1], \
      [1, 1, 1, 0, 0, 1], \
      [0, 1, 1, 1, 0, 0], \
      [1, 0, 1, 1, 1, 0], \
      [0, 1, 0, 1, 1, 1], \
      [1, 0, 1, 0, 1, 1]]


def __xor_operate_1(var1, var2, var3):
    return "ASSERT(BVXOR({}, {}) = {});\n".format(var1, var2, var3)


def xor_operate(var1, var2, var3):
    xor_statement = ""
    for var_index in range(0, len(var1)):
        xor_statement += __xor_operate_1(var1[var_index], var2[var_index], var3[var_index])
    return xor_statement


def __sbox_operate1(v1, v2):
    var1 = "{}@{}@{}".format(v1[2], v1[1], v1[0])
    var2 = "{}@{}@{}".format(v2[2], v2[1], v2[0])
    statement1 = "0bin000"
    for i in range(1, 8):
        iv = "0bin"
        for j in range(0, 3):
            iv += "{}".format((i >> (2 - j)) & 0x1)
        siv = "0bin"
        for j in range(0, 3):
            siv += "{}".format((sbox[i] >> (2 - j)) & 0x1)
        statement1 = "(IF {} = {} THEN {} ELSE {} ENDIF)".format(var1, iv, siv, statement1)
    statement = "ASSERT({} = {});\n".format(var2, statement1)
    return statement


def kp1(v1, v2, k):
    var00 = "{}@{}@{}".format(v1[2], v1[1], v1[0])
    var01 = "{}@{}@{}".format(v1[1], v1[2], v1[0])
    var10 = "{}@{}@{}".format(v1[2], v1[0], v1[1])
    var11 = "{}@{}@{}".format(v1[0], v1[1], v1[2])
    var2 = "{}@{}@{}".format(v2[2], v2[1], v2[0])
    key = "{}@{}".format(k[1], k[0])
    statement1 = var00
    statement1 = "(IF {} = 0bin01 THEN {} ELSE {} ENDIF)".format(key, var01, statement1)
    statement1 = "(IF {} = 0bin10 THEN {} ELSE {} ENDIF)".format(key, var10, statement1)
    statement1 = "(IF {} = 0bin11 THEN {} ELSE {} ENDIF)".format(key, var11, statement1)
    statement = "ASSERT({} = {});\n".format(var2, statement1)
    return statement


def kp(v1, v2, v3):
    s_box_size = 3
    key_size1 = 2
    statement = ""
    for s_box_index in range(0, 16):
        begin_index = s_box_index * s_box_size
        end_index = begin_index + s_box_size
        begin_index1 = key_size1 * s_box_index
        end_index1 = begin_index1 + key_size1
        statement += kp1(v1[begin_index:end_index], v2[begin_index:end_index], v3[begin_index1:end_index1])
    return statement


def sbox_operate(var1, var2):
    s_box_size = 3
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
        if i <= (len(var) - 2):
            var[i] = var1[(3 * i) % (len(var) - 1)]
        else:
            var[i] = var1[i]
    return var


def perm_wire_value(val):
    var = [0 for i in range(0, len(val))]
    for i in range(0, len(val)):
        if i <= (len(var) - 2):
            var[i] = val[(3 * i) % (len(var) - 1)]
        else:
            var[i] = val[i]
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
    var2 = ["p2_{}_{}_{}".format(var, round_index, i) for i in range(0, var_size)]
    var3 = ["p3_{}_{}_{}".format(var, round_index, i) for i in range(0, var_size)]
    return var0, var1, var2, var3


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

    k0 = key_var_dec("k", 0, cd["cipher_size"])
    k1 = key_var_dec("k", 1, 32)

    all_var.append(k0)
    all_var.append(k1)

    x = state_var_dec("x", round_inf[0], cd["cipher_size"])
    begin_values = copy.deepcopy(x)
    for rou in range(round_inf[0], round_inf[1]):
        all_var += copy.deepcopy(x)
        y = state_var_dec("y", rou, cd["cipher_size"])
        all_var += copy.deepcopy(y)
        u0 = perm_wire(y[0])
        u1 = perm_wire(y[1])
        u2 = perm_wire(y[2])
        u3 = perm_wire(y[3])

        statement += xor_operate(x[0], k0, u0)
        statement += xor_operate(x[1], k0, u1)
        statement += xor_operate(x[2], k0, u2)
        statement += xor_operate(x[3], k0, u3)

        z = state_var_dec("z", rou, cd["cipher_size"])
        all_var += copy.deepcopy(z)

        for i in range(0, cd["cipher_size"]):
            if i < 6:
                statement += "ASSERT(BVXOR({}, {}) = 0bin{});\n".format(y[0][i], z[0][i], rc[rou][i])
                statement += "ASSERT(BVXOR({}, {}) = 0bin{});\n".format(y[1][i], z[1][i], rc[rou][i])
                statement += "ASSERT(BVXOR({}, {}) = 0bin{});\n".format(y[2][i], z[2][i], rc[rou][i])
                statement += "ASSERT(BVXOR({}, {}) = 0bin{});\n".format(y[3][i], z[3][i], rc[rou][i])
            else:
                statement += "ASSERT({} = {});\n".format(y[0][i], z[0][i])
                statement += "ASSERT({} = {});\n".format(y[1][i], z[1][i])
                statement += "ASSERT({} = {});\n".format(y[2][i], z[2][i])
                statement += "ASSERT({} = {});\n".format(y[3][i], z[3][i])
        w = state_var_dec("w", rou, cd["cipher_size"])
        all_var += copy.deepcopy(w)

        statement += kp(z[0], w[0], k1)
        statement += kp(z[1], w[1], k1)
        statement += kp(z[2], w[2], k1)
        statement += kp(z[3], w[3], k1)

        x1 = state_var_dec("x", rou + 1, cd["cipher_size"])
        statement += sbox_operate(w[0], x1[0])
        statement += sbox_operate(w[1], x1[1])
        statement += sbox_operate(w[2], x1[2])
        statement += sbox_operate(w[3], x1[3])

        x = copy.deepcopy(x1)
    all_var += copy.deepcopy(x)
    y = state_var_dec("y", round_inf[1], cd["cipher_size"])
    all_var += copy.deepcopy(y)

    statement += xor_operate(x[0], k0, y[0])
    statement += xor_operate(x[1], k0, y[1])
    statement += xor_operate(x[2], k0, y[2])
    statement += xor_operate(x[3], k0, y[3])

    end_values = copy.deepcopy(y)
    return begin_values, end_values, all_var, statement


def __mb_mode0(cd, mode):
    statement = ""

    begin_values, end_values, all_var, statement1 = values_propagate_phrase0(cd, [mode[1][0], mode[1][1]])

    statement += header(all_var)

    statement += var_value_assign(begin_values[0], cd["b0"])
    statement += var_value_assign(begin_values[1], cd["b1"])

    statement += statement1

    statement += var_value_assign(end_values[0], cd["e0"])
    statement += var_value_assign(end_values[1], cd["e1"])

    statement += trailer([], [])

    f = open(cd["solve_file"], "a")
    f.write(statement)
    f.close()


def __mb_mode1(cd, mode):
    statement = ""

    begin_values, end_values, all_var, statement1 = values_propagate_phrase0(cd, [mode[1][0], mode[1][1]])

    statement += header(all_var)

    statement += xor_operate(begin_values[0], begin_values[1], ["0bin{}".format(cd["b1"][i]) for i in range(0, len(cd["b1"]))])
    statement += xor_operate(begin_values[0], begin_values[2], ["0bin{}".format(cd["b2"][i]) for i in range(0, len(cd["b2"]))])
    statement += xor_operate(begin_values[0], begin_values[3], ["0bin{}".format(cd["b3"][i]) for i in range(0, len(cd["b3"]))])

    statement += statement1

    statement += xor_operate(end_values[0], end_values[1], ["0bin{}".format(cd["e1"][i]) for i in range(0, len(cd["e1"]))])
    statement += xor_operate(end_values[0], end_values[2], ["0bin{}".format(cd["e2"][i]) for i in range(0, len(cd["e2"]))])
    statement += xor_operate(end_values[0], end_values[3], ["0bin{}".format(cd["e3"][i]) for i in range(0, len(cd["e3"]))])

    statement += trailer([], [])

    f = open(cd["solve_file"], "a")
    f.write(statement)
    f.close()


def model_build(cd, mode):
    if os.path.exists(cd["solve_file"]):
        os.remove(cd["solve_file"])
    if mode[0] == 0:
        __mb_mode0(cd, mode)
    if mode[0] == 1:
        __mb_mode1(cd, mode)
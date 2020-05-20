#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import copy
import os


def xor(var1, var2, var3):
    statement = ""
    for i in range(0, len(var1)):
        statement += "ASSERT(BVXOR({}, {}) = {});\n".format(var1[i], var2[i], var3[i])
    return statement


def var_value_assign(var1, var):
    statement = ""
    v = "0bin"
    le = len(var)
    for i in range(0, le):
        v += str(var[le - 1 - i])
    statement += "ASSERT({} = {});\n".format(var1, v)
    return statement


def state_dependent(a, b, c, xor_value, mod_value):
    statement = ""
    statement += "ASSERT(BVXOR({}, {}) = {});\n".format(a, b, xor_value)
    statement += "ASSERT(BVMOD(32, {}, 0bin{}0000000000100000) = {});\n".format(b, "0" * 16, mod_value)
    statement1 = "{}".format(xor_value)
    st = ["00000", "00001", "00010", "00011", "00100", "00101", "00110", "00111",
          "01000", "01001", "01010", "01011", "01100", "01101", "01110", "01111",
          "10000", "10001", "10010", "10011", "10100", "10101", "10110", "10111",
          "11000", "11001", "11010", "11011", "11100", "11101", "11110", "11111"]
    for i in range(1, 32):
        iv = "0bin" + "0" * 27
        sv = "{}[{}:{}]@{}[{}:{}]".format(xor_value, 31 - i, 0, xor_value, 31, 31 - i + 1)
        statement1 = "(IF {} = {}{} THEN {} ELSE {} ENDIF)".format(mod_value, iv, st[i], sv, statement1)
    statement += "ASSERT({} = {});\n".format(c, statement1)
    return statement


def header(var1):
    temp1 = ""
    temp = ""
    for i in range(0, len(var1)):
        temp += "{}, ".format(var1[i])
    temp = temp[0:-2]
    temp += " : BITVECTOR(32);\n"
    temp1 += temp
    return temp1


def trailer(v1, va2):
    return "QUERY(FALSE);\nCOUNTEREXAMPLE;"


def state_var_dec(var, round_index, mul):
    return ["p_{}_{}_{}".format(i, var, round_index) for i in range(0, mul)]


def diff_var_dec(var, round_index):
    return "d_{}_{}".format(var, round_index)


def key_var_dec(var, round_index, mul):
    return ["k_{}_{}_{}".format(i, var, round_index) for i in range(0, mul)]


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
    return res


def values_propagate_phrase0(cd, round_inf):
    statement = ""
    all_var = []
    key_var = []
    x = state_var_dec("x", round_inf[0], cd["mul"])
    y = state_var_dec("y", round_inf[0], cd["mul"])
    begin_values = list()
    for vi in range(0, cd["mul"]):
        begin_values.append("{}@{}".format(y[vi], x[vi]))

    for rou in range(round_inf[0], round_inf[1]):
        all_var += copy.deepcopy(x)
        all_var += copy.deepcopy(y)

        z = state_var_dec("z", rou,  cd["mul"])
        all_var += copy.deepcopy(z)

        u = state_var_dec("u", rou,  cd["mul"])
        all_var += copy.deepcopy(u)

        mod0 = state_var_dec("mo0", rou,  cd["mul"])
        all_var += copy.deepcopy(mod0)

        for i in range(0, cd["mul"]):
            statement += state_dependent(y[i], x[i], u[i], z[i], mod0[i])

        x1 = state_var_dec("x", rou + 1,  cd["mul"])
        y1 = state_var_dec("y", rou + 1,  cd["mul"])

        kk0 = key_var_dec("k0", rou,  cd["mul"])
        all_var += copy.deepcopy(kk0)
        key_var.append(kk0)

        for i in range(0, cd["mul"]):
            statement += "ASSERT(BVPLUS(32, {}, {}) = {});\n".format(u[i], kk0[i], x1[i])
            statement += "ASSERT({} = {});\n".format(x[i], y1[i])

        x = copy.deepcopy(x1)
        y = copy.deepcopy(y1)
    all_var += copy.deepcopy(x)
    all_var += copy.deepcopy(y)
    end_values = list()
    for vi in range(0, cd["mul"]):
        end_values.append("{}@{}".format(y[vi], x[vi]))

    return begin_values, end_values, key_var, all_var, statement


def __mb_mode0(cd, mode):
    statement = ""

    begin_values, end_values, key_var, all_var, statement1 = values_propagate_phrase0(cd, [mode[1][0], mode[1][1]])

    statement += header(all_var)
    statement += var_value_assign(begin_values[0], cd["b0"])
    statement += var_value_assign(begin_values[1], cd["b1"])

    statement += statement1

    statement += var_value_assign(end_values[0], cd["e0"])
    statement += var_value_assign(end_values[1], cd["e1"])
    for kv in key_var:
        statement += "ASSERT({} = {});\n".format(kv[0], kv[1])
    statement += trailer([], [])
    f = open(cd["solve_file"], "a")
    f.write(statement)
    f.close()


def __mb_mode1(cd, mode):
    statement = ""

    begin_values, end_values, key_var, all_var, statement1 = values_propagate_phrase0(cd, [mode[1][0], mode[1][1]])
    statement2 = ""
    for i in range(1, cd["mul"]):
        dx0 = "{}@{}".format(diff_var_dec("{}_y".format(i), mode[1][0]), diff_var_dec("{}_x".format(i), mode[1][0]))
        dxn = "{}@{}".format(diff_var_dec("{}_y".format(i), mode[1][1]), diff_var_dec("{}_x".format(i), mode[1][1]))
        all_var.append(diff_var_dec("{}_x".format(i), mode[1][0]))
        all_var.append(diff_var_dec("{}_y".format(i), mode[1][0]))

        all_var.append(diff_var_dec("{}_x".format(i), mode[1][1]))
        all_var.append(diff_var_dec("{}_y".format(i), mode[1][1]))

        statement2 += "ASSERT(BVXOR({}, {}) = {});\n".format(begin_values[0], begin_values[i], dx0)
        statement2 += var_value_assign(dx0, cd["b{}".format(i)])
        statement2 += "ASSERT(BVXOR({}, {}) = {});\n".format(end_values[0], end_values[i], dxn)
        statement2 += var_value_assign(dxn, cd["e{}".format(i)])
    statement += header(all_var)
    statement += statement1
    statement += statement2
    for kv in key_var:
        for i in range(1, cd["mul"]):
            statement += "ASSERT({} = {});\n".format(kv[i], kv[0])
    statement += trailer([], [])
    f = open(cd["solve_file"], "a")
    f.write(statement)
    f.close()


def __mb_mode10(cd, mode):
    statement = ""

    begin_values, end_values, key_var, all_var, statement1 = values_propagate_phrase0(cd, [mode[1][0], mode[1][1]])
    statement += header(all_var)
    #vv = [0 for si in range(0, 16)] + [0 for i in range(0, 4)] + [1 for ii in range(0, 4)] + [0 for ti in range(0, 40)]
    for i in range(0, len(begin_values[0])):
        statement += "ASSERT({} = 0bin{});\n".format(begin_values[0][i], 1)
    for i in range(0, len(begin_values[1])):
        statement += "ASSERT({} = 0bin{});\n".format(begin_values[1][i], random.randint(0, 1))

    statement += statement1
    for i in range(0, len(key_var[0])):
        statement += "ASSERT({} = {});\n".format(key_var[0][i], key_var[1][i])

    for i in range(0, len(key_var[0])):
        statement += "ASSERT({} = 0bin{});\n".format(key_var[0][i], 0)
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
    if mode[0] == 10:
        __mb_mode10(cd, mode)

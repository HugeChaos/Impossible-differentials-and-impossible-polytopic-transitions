#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import os
import copy
import random


def __xor_operate_1(var1, var2, var3):
    return "ASSERT(BVXOR({}, {}) = {});\n".format(var1, var2, var3)


def xor_operate(var1, var2, var3):
    xor_statement = ""
    for var_index in range(0, len(var1)):
        xor_statement += __xor_operate_1(var1[var_index], var2[var_index], var3[var_index])
    return xor_statement


def s9(var1, var2):
    s1 = ""
    s2 = ""
    for i in range(0, len(var1)):
        s1 += ", 0bin000@{}".format(var1[i])
        s2 += ", 0bin000@{}".format(var2[i])
    s11 = "BVPLUS(4{})".format(s1)
    s22 = "BVPLUS(4{})".format(s2)
    statement = ""
    for i in range(0, len(var1)):
        statement += "ASSERT(BVGE({}, 0bin000@{}));\n".format(s11, var2[i])
        statement += "ASSERT(BVGE({}, 0bin000@{}));\n".format(s22, var1[i])

    return statement


def s7(var1, var2):
    s1 = ""
    s2 = ""
    for i in range(0, len(var1)):
        s1 += ", 0bin000@{}".format(var1[i])
        s2 += ", 0bin000@{}".format(var2[i])
    s11 = "BVPLUS(4{})".format(s1)
    s22 = "BVPLUS(4{})".format(s2)
    statement = ""
    for i in range(0, len(var1)):
        statement += "ASSERT(BVGE({}, 0bin000@{}));\n".format(s11, var2[i])
        statement += "ASSERT(BVGE({}, 0bin000@{}));\n".format(s22, var1[i])

    return statement


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


def diff_var_dec(var, round_index, var_size):
    return ["d_{}_{}_{}".format(var, round_index, i) for i in range(0, var_size)]


def fl_1(x, y, aux0, aux1):
    statement = ""
    xr = x[0:16]
    xl = x[16:32]
    yr = y[0:16]
    yl = y[16:32]
    for i in range(0, 16):
        statement += "ASSERT(BVGE({}, {}));\n".format(xl[i], aux0[i])
    for i in range(0, 16):
        statement += "ASSERT(BVGE({}, {}));\n".format(yr[i], aux1[i])
    statement += xor_operate(xr, aux0, yr)
    statement += xor_operate(xl, aux1, yl)
    return statement


def fl_layer(rin, rout, lin, lout, rou):
    aux0 = diff_var_dec("a0", rou, 16)
    aux1 = diff_var_dec("a1", rou, 16)
    aux2 = diff_var_dec("a2", rou, 16)
    aux3 = diff_var_dec("a3", rou, 16)

    all_var = [copy.deepcopy(aux0), copy.deepcopy(aux1), copy.deepcopy(aux2), copy.deepcopy(aux3)]
    statement = fl_1(copy.deepcopy(rin), copy.deepcopy(rout), copy.deepcopy(aux0), copy.deepcopy(aux1))
    statement += fl_1(copy.deepcopy(lin), copy.deepcopy(lout), copy.deepcopy(aux2), copy.deepcopy(aux3))
    return statement, all_var


def fi_1(x, y, b):
    statement = ""
    xr = x[0:7]
    xl = x[7:16]
    yr = y[0:9]
    yl = y[9:16]
    statement += s9(xl, copy.deepcopy(b[0]))
    for i in range(0, 7):
        statement += "ASSERT(BVXOR({}, {}) = {});\n".format(xr[i], copy.deepcopy(b[0][i]), copy.deepcopy(b[1][i]))
    for i in range(7, 9):
        statement += "ASSERT({}={});\n".format(b[0][i], b[1][i])
    statement += s7(xr, copy.deepcopy(b[2]))
    for i in range(0, 7):
        statement += "ASSERT(BVXOR({}, {}) = {});\n".format(copy.deepcopy(b[1][i]), copy.deepcopy(b[2][i]),
                                                            copy.deepcopy(yl[i]))
    statement += s9(b[1], b[3])
    for i in range(0, 7):
        statement += "ASSERT(BVXOR({}, {}) = {});\n".format(b[3][i], yl[i], yr[i])
    for i in range(7, 9):
        statement += "ASSERT({} = {});\n".format(b[3][i], yr[i])
    return statement


def fo_layer(x, y, rou):
    statement = ""
    all_var = []
    p0 = diff_var_dec("p_0", rou, 16)
    q0 = diff_var_dec("q_0", rou, 16)
    p1 = diff_var_dec("p_1", rou, 16)
    q1 = diff_var_dec("q_1", rou, 16)
    p2 = diff_var_dec("p_2", rou, 16)
    q2 = diff_var_dec("q_2", rou, 16)
    all_var.append(copy.deepcopy(p0))
    all_var.append(copy.deepcopy(q0))
    all_var.append(copy.deepcopy(p1))
    all_var.append(copy.deepcopy(q1))
    all_var.append(copy.deepcopy(p2))
    all_var.append(copy.deepcopy(q2))
    p = [copy.deepcopy(p0), copy.deepcopy(p1), copy.deepcopy(p2)]
    q = [copy.deepcopy(q0), copy.deepcopy(q1), copy.deepcopy(q2)]
    for i in range(0, 3):
        b0 = diff_var_dec("b_{}_0".format(i), rou, 9)
        b1 = diff_var_dec("b_{}_1".format(i), rou, 9)
        b2 = diff_var_dec("b_{}_2".format(i), rou, 7)
        b3 = diff_var_dec("b_{}_3".format(i), rou, 9)
        all_var.append(copy.deepcopy(b0))
        all_var.append(copy.deepcopy(b1))
        all_var.append(copy.deepcopy(b2))
        all_var.append(copy.deepcopy(b3))
        b = [copy.deepcopy(b0), copy.deepcopy(b1), copy.deepcopy(b2), copy.deepcopy(b3)]
        statement += fi_1(p[i], q[i], b)

    statement += var_equal(x[16:32], p0)
    statement += var_equal(x[0:16], p1)
    statement += xor_operate(x[0:16], q0, p2)
    statement += xor_operate(p2, q1, y[16:32])
    statement += xor_operate(y[16:32], q2, y[0:16])

    return statement, all_var


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


def values_propagate_phrase0(cd, round_inf):
    statement = ""
    all_var = []

    l0 = diff_var_dec("l", round_inf[0], cd["branch_size"])
    r0 = diff_var_dec("r", round_inf[0], cd["branch_size"])

    begin_values = copy.deepcopy(r0 + l0)

    for rou in range(round_inf[0], round_inf[1]):
        all_var.append(copy.deepcopy(l0))
        all_var.append(copy.deepcopy(r0))

        l1 = diff_var_dec("l", rou + 1, cd["branch_size"])
        r1 = diff_var_dec("r", rou + 1, cd["branch_size"])

        if rou % 2 == 0:
            w = diff_var_dec("w", rou, cd["branch_size"])
            v = diff_var_dec("v", rou, cd["branch_size"])
            all_var.append(copy.deepcopy(w))
            all_var.append(copy.deepcopy(v))
            statement1, all_var1 = fl_layer(r0, v, l0, r1, rou)
            statement2, all_var2 = fo_layer(r1, w, rou)
            statement += statement1
            statement += statement2
            all_var += copy.deepcopy(all_var1)
            all_var += copy.deepcopy(all_var2)
            statement += xor_operate(w, v, l1)
        else:
            w = diff_var_dec("w", rou, cd["branch_size"])
            all_var.append(copy.deepcopy(w))
            statement2, all_var2 = fo_layer(l0, w, rou)
            statement += statement2
            all_var += copy.deepcopy(all_var2)
            statement += var_equal(r1, l0)
            statement += xor_operate(r0, w, l1)
        l0 = copy.deepcopy(l1)
        r0 = copy.deepcopy(r1)

    all_var.append(copy.deepcopy(l0))
    all_var.append(copy.deepcopy(r0))

    end_values = copy.deepcopy(r0 + l0)

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

    statement += var_value_assign(begin_values, cd["b1"])
    statement += statement1

    statement += var_value_assign(end_values, cd["e1"])
    statement += trailer([], [])
    f = open(cd["solve_file"], "a")
    f.write(statement)
    f.close()


def __mb_mode10(cd, mode):
    statement = ""

    begin_values, end_values, all_var, statement1 = values_propagate_phrase0(cd, [mode[1][0], mode[1][1]])
    statement += header(all_var)
    for i in range(0, len(begin_values[0])):
        statement += "ASSERT({} = 0bin{});\n".format(begin_values[0][i], random.randint(0, 1))
    for i in range(0, len(begin_values[1])):
        statement += "ASSERT({} = 0bin{});\n".format(begin_values[1][i], random.randint(0, 1))

    statement += statement1
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


def solver2(solve_file):
    stp_parameters = ["stp", "--minisat", "--CVC", solve_file]
    res = subprocess.check_output(stp_parameters)
    res = res.replace("\r", "")[0:-1]
    print(res)
    if res == "Valid.":
        return True, res
    else:
        return False, res

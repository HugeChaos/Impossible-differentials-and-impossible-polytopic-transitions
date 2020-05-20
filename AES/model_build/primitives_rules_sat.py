#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess


def __xor_operate_1(var1, var2, var3):
    return "ASSERT(BVXOR({}, {}) = {});\n".format(var1, var2, var3)


def __and_operate_1(var1, var2, var3):
    return "ASSERT(({} & {}) = {});\n".format(var1, var2, var3)


def __xor_operate(var1, var2, var3):
    xor_statement = ""
    for var_index in range(0, len(var1)):
        xor_statement += __xor_operate_1(var1[var_index], var2[var_index], var3[var_index])
    return xor_statement


def __xor4_operate(var1, var2, var3, var4, var5):
    xor_statement = ""
    for i in range(0, len(var1)):
        xor_statement += "ASSERT(BVXOR({}, BVXOR({}, BVXOR({}, {}))) = {});\n".format(var1[i], var2[i], var3[i], var4[i], var5[i])
    return xor_statement


def __and_operate(var1, var2, var3):
    statement = ""
    for var_index in range(0, len(var1)):
        statement += __and_operate_1(var1[var_index], var2[var_index], var3[var_index])
    return statement


def __b_shift(var1, shiftconstant):
    var = ["" for i in range(0, len(var1))]
    for i in range(0, len(var1)):
        var[(i + shiftconstant) % len(var1)] = var1[i]
    return var


def __rb_shift(var1, shiftconstant):
    var = ["" for i in range(0, len(var1))]
    for i in range(0, len(var1)):
        var[(i - shiftconstant) % len(var1)] = var1[i]
    return var


def __s_xor_operate(var1, var2, var3):
    statement = ""
    for i in range(0, len(var1)):
        for j in range(0, len(var1[0])):
            statement += __xor_operate(var1[i][j], var2[i][j], var3[i][j])
    return statement


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


def __sbox_operate(var1, var2, s_box_logic_express):
    s_box_size = len(var1) // len(s_box_logic_express)
    s_box_statement = ""
    for s_box_index in range(0, len(s_box_logic_express)):
        begin_index = s_box_index * s_box_size
        end_index = begin_index + s_box_size
        s_box_statement += __sbox_operate1(var1[begin_index:end_index], var2[begin_index:end_index], s_box_logic_express[s_box_index])
    return s_box_statement


def __s_sbox_operate(var1, var2, s_box_logic_express):
    statement = ""
    for i in range(0, len(var1)):
        for j in range(0, len(var1[0])):
            statement += __sbox_operate1(var1[i][j], var2[i][j], s_box_logic_express)
    return statement


def __var_value_assign(var, values):
    statement = ""
    for i in range(0, len(var)):
        statement += "ASSERT({} = 0bin{});\n".format(var[i], values[i])
    return statement


def __s_var_value_assign(var, values):
    statement = ""
    for i in range(0, len(var)):
        for j in range(0, len(var[0])):
            statement += __var_value_assign(var[i][j], values[i][j])
    return statement


def __var_equal(var1, var2):
    statement = ""
    for i in range(0, len(var1)):
        statement += "ASSERT({} = {});\n".format(var1[i], var2[i])
    return statement


def __s_var_equal(var1, var2):
    statement = ""
    for i in range(0, len(var1)):
        for j in range(0, len(var1[0])):
            statement += __var_equal(var1[i][j], var2[i][j])
    return statement


def __perm_wire(var1, perm):
    var = ["" for i in range(0, len(var1))]
    for i in range(0, len(var1)):
        var[i] = var1[perm[i]]
    return var


def __header(var1):
    temp1 = ""
    for var in var1:
        temp = var[0]
        for i in range(1, len(var)):
            temp += ", {}".format(var[i])
        temp += " : BITVECTOR(1);\n"
        temp1 += temp
    return temp1


def __s_header(var1):
    temp1 = ""
    for var in var1:
        temp = ""
        for i in range(0, len(var)):
            for j in range(0, len(var[0])):
                for k in range(0, len(var[0][0])):
                    temp += "{}, ".format(var[i][j][k])
        temp = temp[0:-2]
        temp += " : BITVECTOR(1);\n"
        temp1 += temp
    return temp1


def __trailer(v1, va2):
    return "QUERY(FALSE);\nCOUNTEREXAMPLE;"


def list2square(l, sp):
    squ = [[["" for k in range(0, sp[2])] for j in range(0, sp[1])] for i in range(0, sp[0])]
    for i in range(0, sp[0]):
        for j in range(0, sp[1]):
            for k in range(0, sp[2]):
                squ[i][j][k] = l[i * sp[1] * sp[2] + j * sp[2] + k]
    return squ


def list2square2(l, sp):
    lis = []
    for sl in l:
        lis.append(list2square(sl, sp))
    return lis


def __shift_row(var, cons):
    row = len(var)
    col = len(var[0])
    nibble = len(var[0][0])

    new_var = [[["" for k in range(0, nibble)] for j in range(0, col)] for i in range(0, row)]

    for i in range(0, row):
        for j in range(0, col):
            for k in range(0, nibble):
                new_var[i][j][k] = var[i][(j + cons[i]) % col][k]
    return new_var


def __s_mix_column(var1, var2, mix_column):
    statement = ""
    for i in range(0, len(mix_column)):
        statement1 = []
        for j in range(0, len(mix_column[0])):
            if mix_column[i][j] != 0:
                statement1.append(var1[j])
        if len(statement1) == 1:
            temp = statement1[0]
        else:
            temp = "BVXOR({}, {})".format(statement1[0], statement1[1])
            for k in range(2, len(statement1)):
                temp = "BVXOR({}, {})".format(temp, statement1[k])
        temp1 = "ASSERT({} = {});\n".format(temp, var2[i])
        statement += temp1
    return statement


def __s_mc(var1, var2, mix_column):
    statement = ""
    for j in range(0, len(var1[0])):
        v1 = []
        v2 = []
        for i in range(0, len(var1)):
            v1 += var1[i][j]
            v2 += var2[i][j]
        statement += __s_mix_column(v1, v2, mix_column)
    return statement


def __nibble_perm(var, perm):
    n_var = [[["" for k in range(0, len(var[0][0]))]for j in range(0, len(var[0]))] for i in range(0, len(var))]

    for i in range(0, len(var)):
        for j in range(0, len(var[0])):
            for k in range(0, len(var[0][0])):
                n_var[i][j][k] = var[perm[i][j][0]][perm[i][j][1]][k]
    return n_var


def s_operate_all(operate_type, op):#operate_parameter
    if operate_type == "xor":
        statement = __s_xor_operate(op[0], op[1], op[2])
    elif operate_type == "s_box":
        statement = __s_sbox_operate(op[0], op[1], op[2])
    elif operate_type == "header":
        statement = __s_header(op)
    elif operate_type == "trailer":
        statement = __trailer(op[0], op[1])
    elif operate_type == "var_value_assign":
        statement = __s_var_value_assign(op[0], op[1])
    elif operate_type == "mc":
        statement = __s_mc(op[0], op[1], op[2])
    elif operate_type == "nibble_perm":
        statement = __nibble_perm(op[0], op[1])
    elif operate_type == "mix_column":
        statement = __s_mix_column(op[0], op[1], op[2])
    elif operate_type == "shift_row":
        statement = __shift_row(op[0], op[1])
    else:
        print("error2!")
        statement = ""
    return statement


def operate_all(operate_type, op):#operate_parameter
    if operate_type == "xor":
        statement = __xor_operate(op[0], op[1], op[2])
    elif operate_type == "xor4":
        statement = __xor4_operate(op[0], op[1], op[2], op[3], op[4])
    elif operate_type == "and":
        statement = __and_operate(op[0], op[1], op[2])
    elif operate_type == "s_box":
        statement = __sbox_operate(op[0], op[1], op[2])
    elif operate_type == "header":
        statement = __header(op)
    elif operate_type == "trailer":
        statement = __trailer(op[0], op[1])
    elif operate_type == "var_value_assign":
        statement = __var_value_assign(op[0], op[1])
    elif operate_type == "var_equal":
        statement = __var_equal(op[0], op[1])
    elif operate_type == "perm_wire":
        statement = __perm_wire(op[0], op[1])
    elif operate_type == "b_shift":
        statement = __b_shift(op[0], op[1])
    elif operate_type == "rb_shift":
        statement = __rb_shift(op[0], op[1])
    else:
        print("error1!\n")
        statement = ""
    return statement


def __state_var_dec(var, round_index, var_size):
    var0 = ["p0_{}_{}_{}".format(var, round_index, i) for i in range(0, var_size)]
    var1 = ["p1_{}_{}_{}".format(var, round_index, i) for i in range(0, var_size)]
    return var0, var1


def __diff_var_dec(var, round_index, var_size):
    return ["d_{}_{}_{}".format(var, round_index, i) for i in range(0, var_size)]


def __key_var_dec(var, round_index, var_size):
    return ["k_{}_{}_{}".format(var, round_index, i) for i in range(0, var_size)]


def var_dec(var_dec_type, var, round_index, var_size):
    if var_dec_type == "state":
        return __state_var_dec(var, round_index, var_size)
    elif var_dec_type == "diff":
        return __diff_var_dec(var, round_index, var_size)
    elif var_dec_type == "key":
        return __key_var_dec(var, round_index, var_size)


def s_var_dec(var_dec_type, var, round_index, var_size):
    if var_dec_type == "state":
        return __state_var_dec(var, round_index, var_size)
    elif var_dec_type == "diff":
        return __diff_var_dec(var, round_index, var_size)
    elif var_dec_type == "key":
        return __key_var_dec(var, round_index, var_size)


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


#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "HugeChaos"


def __parsing1(sbox_size, out_string):
    logic_equation = []
    line = out_string
    line = line.replace("F = (", "")
    line = line.replace(");\n", "")
    line = line.split(")(")
    for item in line:
        coe_ine = []
        for var in ["x", "y"]:
            for i in range(0, sbox_size):
                st1 = var + str(sbox_size - 1 - i) + "'"
                st2 = var + str(sbox_size - 1 - i)
                if item.find(st1) != -1:
                    coe_ine.append(-1)
                elif item.find(st2) != -1:
                    coe_ine.append(1)
                else:
                    coe_ine.append(0)
        logic_equation.append(coe_ine)
    return logic_equation


def __parsing2(sbox_size, out_string):
    ine = []
    line = out_string
    line = line.replace("F = (", "")
    line = line.replace(");\n", "")
    line = line.split(")(")
    for item in line:
        coe_ine = []
        con = 0
        for var in ["x", "y"]:
            for i in range(0, sbox_size):
                st1 = var + str(sbox_size - 1 - i) + "'"
                st2 = var + str(sbox_size - 1 - i)
                if item.find(st1) != -1:
                    coe_ine.append(-1)
                    con = con + 1
                elif item.find(st2) != -1:
                    coe_ine.append(1)
                else:
                    coe_ine.append(0)
        coe_ine.append(con - 1)
        ine.append(coe_ine)
    return ine


# parsing logic friday output
def parsing_s_box(mode, sbox_size, out_string):
    if mode == "sat":
        return __parsing1(sbox_size, out_string)
    elif mode == "milp":
        return __parsing2(sbox_size, out_string)
    else:
        print("parsing error!\n")


def __element_multi_02(irr_poly, mat_in):
    mat_size = len(irr_poly)
    mat_out = [[0 for i in range(0, mat_size)] for j in range(0, mat_size)]
    for i in range(1, mat_size):
        for j in range(0, mat_size):
            mat_out[i][j] = mat_in[i - 1][j]
    for j in range(0, mat_size):
        if mat_in[mat_size - 1][j] == 1:
            for i in range(0, mat_size):
                mat_out[i][j] = mat_out[i][j] ^ irr_poly[i]
    return mat_out


def __matrix_base(irr_poly):
    mat_size = len(irr_poly)
    m_base = []
    unit_matrix = [[0 for i in range(0, mat_size)] for j in range(0, mat_size)]
    for i in range(0, mat_size):
        for j in range(0, mat_size):
            if i == j:
                unit_matrix[i][j] = 1
    m_base.append(unit_matrix)
    for i in range(1, mat_size):
        m_base.append(__element_multi_02(irr_poly, m_base[i - 1]))
    return m_base


def __mat_add(mat1, mat2):
    mat = [[0 for j in range(0, len(mat1[0]))] for i in range(0, len(mat1))]
    for i in range(0, len(mat1)):
        for j in range(0, len(mat1[0])):
            mat[i][j] = mat1[i][j] ^ mat2[i][j]
    return mat


def __finite_ele_2_matrix(m_base, finite_ele):
    mat_size = len(m_base)
    mat = [[0 for j in range(0, mat_size)] for i in range(0, mat_size)]
    for i in range(0, mat_size):
        if ((finite_ele >> i) & 0x1) == 1:
            mat = __mat_add(mat, m_base[i])
    return mat


def __finite_matrix_2_bit_matrix(finite_matrix, irr_poly):
    sub_mat_size = len(irr_poly)
    bit_matrix_row = len(finite_matrix) * sub_mat_size
    bit_matrix_col = len(finite_matrix[0]) * sub_mat_size
    m_base = __matrix_base(irr_poly)
    bit_matrix = [[0 for i in range(0, bit_matrix_row)] for j in range(0, bit_matrix_col)]
    for row in range(0, len(finite_matrix)):
        for col in range(0, len(finite_matrix[0])):
            sub_mat = __finite_ele_2_matrix(m_base, finite_matrix[row][col])
            for sub_row in range(0, len(sub_mat)):
                for sub_col in range(0, len(sub_mat[0])):
                    bit_matrix[row * len(sub_mat) + sub_row][col * len(sub_mat[0]) + sub_col] = sub_mat[sub_row][sub_col]
    return bit_matrix

#ARIA#####################################################


def __word_zero_one_matrix_2_bit_matrix(zero_one_matrix, nibble_size):
    bit_matrix_row = len(zero_one_matrix) * nibble_size
    bit_matrix_col = len(zero_one_matrix[0]) * nibble_size
    nibble_size_matrix = [[0 for j in range(0, nibble_size)] for i in range(0, nibble_size)]
    for i in range(0, nibble_size):
        for j in range(0, nibble_size):
            if i == j:
                nibble_size_matrix[i][j] = 1
    bit_matrix = [[0 for j in range(0, bit_matrix_col)] for i in range(0, bit_matrix_row)]
    for row in range(0, len(zero_one_matrix)):
        for col in range(0, len(zero_one_matrix[0])):
            if zero_one_matrix[row][col] == 1:
                for sub_row in range(0, nibble_size):
                    for sub_col in range(0, nibble_size):
                        bit_matrix[row * nibble_size + sub_row][col * nibble_size + sub_col] = nibble_size_matrix[sub_row][sub_col]
    return bit_matrix


def parsing_matrix(matrix, para):
    if type(para) == list:
        return __finite_matrix_2_bit_matrix(matrix, para)
    elif type(para) == int:
        return __word_zero_one_matrix_2_bit_matrix(matrix, para)
    else:
        print("matrix parameter error!\n")

#irr_poly = [1, 1, 0, 1, 1, 0, 0, 0] #### 1 + 1 X + 0 X^2 + 1 X^3 + 1 X^4 + 0 X^5 + 0 X^6 + 0 X^7 = X^8
#matrix_aes = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
#for i in finite_matrix_2_bit_matrix(matrix_aes, irr_poly):
#    print(i)

gift_ddt = "F = (x3'+x2'+x1'+x0+y1')(x3+x2'+x1+y3'+y2+y1')(x3+x2+x1+y3'+y2'+y1+y0')(x2+x1+y3'+y2'+y1'+y0)" \
           "(x3+x2+x1'+x0'+y2+y1+y0')(x2+x1'+x0'+y2+y1'+y0)(x3+x2'+x1'+x0'+y2'+y1')(x3'+y3+y2'+y1+y0')" \
           "(x2+x0+y3'+y1+y0)(x0'+y3+y2+y1+y0)(x2'+x0'+y3+y1'+y0')(x2+x1+x0+y1+y0')(x3+y3+y2+y1+y0')" \
           "(x2+x1'+y3+y1+y0)(x3+y3+y2'+y1+y0)(x3'+x2'+x1+x0+y0')(x3+x2+y3+y1'+y0')(x2'+y3+y2'+y1'+y0)" \
           "(x3+x0+y3'+y1'+y0')(x2+y3+y2+y1'+y0)(x3+x2'+x1'+x0+y1)(x3+x2'+x1+x0+y0)(x2+x1+x0+y1'+y0)" \
           "(x3'+x2'+x0'+y3'+y1+y0)(x3'+x2+y3+y1+y0)(x3'+x2+x0'+y3'+y1'+y0')(x2+x1'+x0+y1'+y0')(x2'+y3+y2+y1+y0)" \
           "(x3'+x1+y3'+y2+y1+y0')(x3'+x1'+x0'+y2'+y1+y0')(x3+x2'+x1+x0'+y2+y0')(x3+x2'+x1'+y3'+y2'+y0')" \
           "(x3'+x1+x0'+y3'+y2'+y1'+y0)(x3'+x1'+x0'+y3'+y2+y1'+y0);"




















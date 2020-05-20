#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy


sbox = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]


def parsing(result):
    values_dict = dict()
    for r in result:
        r = r.replace("ASSERT( ", "")
        r = r.replace(" );\n", "")
        r = r.split(" = 0b")
        values_dict[r[0]] = int(r[1])
    return values_dict


def result_parsing(file1):
    f = open(file1, "r")
    all_result = list()
    one_result = list()
    for line in f.readlines():
        one_result.append(line)
        if line == "Invalid.\n":
            one_result.remove(one_result[0])
            one_result.remove(one_result[0])
            one_result.remove(one_result[-1])
            all_result.append(one_result)
            one_result = list()
    f.close()
    return all_result


def var_dec(var_t, round_t, length_t):
    return ["{}_{}_{}".format(var_t, round_t, i) for i in range(0, length_t)]


def round_var():
    trail0 = list()
    trail1 = list()
    diff = list()
    var2values = dict()
    dx = var_dec("d_x", 0, 128)
    diff.append("d_x0")
    var2values["d_x0"] = dx

    dx = var_dec("d_x", 5, 128)
    diff.append("d_x5")
    var2values["d_x5"] = dx

    x0 = var_dec("p0_x", 1, 128)
    x1 = var_dec("p1_x", 1, 128)
    trail0.append("x1_0")
    trail1.append("x1_1")
    var2values["x1_0"] = copy.deepcopy(x0)
    var2values["x1_1"] = copy.deepcopy(x1)

    y0 = var_dec("p0_y", 1, 128)
    y1 = var_dec("p1_y", 1, 128)
    trail0.append("y1_0")
    trail1.append("y1_1")
    var2values["y1_0"] = copy.deepcopy(y0)
    var2values["y1_1"] = copy.deepcopy(y1)
    k = var_dec("k_k", 1, 128)
    trail0.append("k1")
    trail1.append("k1")
    var2values["k1"] = copy.deepcopy(k)
    z0 = var_dec("p0_z", 1, 128)
    z1 = var_dec("p1_z", 1, 128)
    trail0.append("z1_0")
    trail1.append("z1_1")
    var2values["z1_0"] = copy.deepcopy(z0)
    var2values["z1_1"] = copy.deepcopy(z1)
    x0 = var_dec("p0_x", 2, 128)
    x1 = var_dec("p1_x", 2, 128)
    trail0.append("x2_0")
    trail1.append("x2_1")
    var2values["x2_0"] = copy.deepcopy(x0)
    var2values["x2_1"] = copy.deepcopy(x1)
    k = var_dec("k_k", 2, 128)
    trail0.append("k2")
    trail1.append("k2")
    var2values["k2"] = copy.deepcopy(k)
    y0 = var_dec("p0_y", 2, 128)
    y1 = var_dec("p1_y", 2, 128)
    trail0.append("y2_0")
    trail1.append("y2_1")
    var2values["y2_0"] = copy.deepcopy(y0)
    var2values["y2_1"] = copy.deepcopy(y1)
    z0 = var_dec("p0_z", 2, 128)
    z1 = var_dec("p1_z", 2, 128)
    trail0.append("z2_0")
    trail1.append("z2_1")
    var2values["z2_0"] = copy.deepcopy(z0)
    var2values["z2_1"] = copy.deepcopy(z1)
    x0 = var_dec("p0_x", 3, 128)
    x1 = var_dec("p1_x", 3, 128)
    trail0.append("x3_0")
    trail1.append("x3_1")
    var2values["x3_0"] = copy.deepcopy(x0)
    var2values["x3_1"] = copy.deepcopy(x1)
    k = var_dec("k_k", 3, 128)
    trail0.append("k3")
    trail1.append("k3")
    var2values["k3"] = copy.deepcopy(k)
    y0 = var_dec("p0_y", 3, 128)
    y1 = var_dec("p1_y", 3, 128)
    trail0.append("y3_0")
    trail1.append("y3_1")
    var2values["y3_0"] = copy.deepcopy(y0)
    var2values["y3_1"] = copy.deepcopy(y1)
    return trail0, trail1, var2values, diff


def list2square(l):
    squ = [[[0 for k in range(0, 8)] for j in range(0, 4)] for i in range(0, 4)]
    for i in range(0, 4):
        for j in range(0, 4):
            for k in range(0, 8):
                squ[i][j][k] = l[i * 32 + j * 8 + k]
    hex_suq = [[0 for j in range(0, 4)] for i in range(0, 4)]
    for i in range(0, 4):
        for j in range(0, 4):
            bit_v = squ[i][j]
            tem = 0
            for k in range(0, 8):
                tem += bit_v[k] * int(pow(2, k))
            hex_suq[i][j] = tem
    return hex_suq


def single_trail(ar):
    trail0, trail1, var2values, diff = round_var()
    arp = parsing(ar)
    trail_values0 = dict()
    for t0 in trail0:
        var = var2values[t0]
        var_val = list()
        for i in range(0, len(var)):
            var_val.append(arp[var[i]])
        trail_values0[t0] = list2square(var_val)
    trail_values1 = dict()
    for t1 in trail1:
        var = var2values[t1]
        var_val = list()
        for i in range(0, len(var)):
            var_val.append(arp[var[i]])
        trail_values1[t1] = list2square(var_val)
    diff_values = dict()
    for d in diff:
        var = var2values[d]
        var_val = list()
        for i in range(0, len(var)):
            var_val.append(arp[var[i]])
        diff_values[d] = list2square(var_val)
    return trail_values0, trail_values1, diff_values


def verify_sbox(s, t):
    flag_equal = True
    for i in range(0, len(s)):
        for j in range(0, len(s[0])):
            if sbox[s[i][j]] != t[i][j]:
                flag_equal = False
                break
        if not flag_equal:
            break
    return flag_equal


def x_time(x):
    if (x & 0x80) != 0:
        return ((x << 1) & 0xff) ^ 0x1b
    else:
        return (x << 1) & 0xff


def multi(a, b):
    temp = [0 for i in range(0, 8)]
    temp[0] = a
    for i in range(1, 8):
        temp[i] = x_time(temp[i - 1])
    temp_multiply = (b & 0x1) * a
    for i in range(1, 8):
        temp_multiply ^= (((b >> i) & 0x1) * temp[i])
    return temp_multiply


def verify_mixcolumn(s, t):
    m = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    t1 = [[0 for j in range(0, 4)] for i in range(0, 4)]
    for i in range(0, 4):
        for j in range(0, 4):
            t1[i][j] = 0
            for k in range(0, 4):
                t1[i][j] ^= multi(m[i][k], s[k][j])
    flag_equal = True
    for i in range(0, len(s)):
        for j in range(0, len(s[0])):
            if t1[i][j] != t[i][j]:
                flag_equal = False
                break
        if not flag_equal:
            break
    return flag_equal


def verify_keyxor(s, k, t):
    flag_equal = True
    for i in range(0, len(s)):
        for j in range(0, len(s[0])):
            if t[i][j] != (s[i][j] ^ k[i][j]):
                flag_equal = False
                break
        if not flag_equal:
            break
    return flag_equal


def rev_shiftrow(values):
    res = [[0 for j in range(0, 4)] for i in range(0, 4)]
    rc = [0, 1, 2, 3]
    for i in range(0, 4):
        for j in range(0, 4):
            res[i][(j + rc[i]) % 4] = values[i][j]
    return res


def verify_trail(values_t, i):

    if not verify_keyxor(values_t["x1_{}".format(i)], values_t["k1"], values_t["y1_{}".format(i)]):
        exit("(x1, k1) --> can't --> y1;")
    if not verify_sbox(values_t["y1_{}".format(i)], rev_shiftrow(values_t["z1_{}".format(i)])):
        exit("y1 --> can't --> z1;")
    if not verify_mixcolumn(values_t["z1_{}".format(i)], values_t["x2_{}".format(i)]):
        exit("z1 --> can't --> x2;")
    if not verify_keyxor(values_t["x2_{}".format(i)], values_t["k2"], values_t["y2_{}".format(i)]):
        exit("(x2, k2) --> can't --> y2;")
    if not verify_sbox(values_t["y2_{}".format(i)], rev_shiftrow(values_t["z2_{}".format(i)])):
        exit("y2 --> can't --> z2;")
    if not verify_mixcolumn(values_t["z2_{}".format(i)], values_t["x3_{}".format(i)]):
        exit("z2 --> can't --> x3;")
    if not verify_keyxor(values_t["x3_{}".format(i)], values_t["k3"], values_t["y3_{}".format(i)]):
        exit("(x3, k3) --> can't --> y3;")


def verify_diff(values_t):
    if not verify_keyxor(values_t["x1_0"], values_t["x1_1"], values_t["d_x0"]):
        exit("(x1_0, x1_1) --> can't --> dx0;")
    if not verify_keyxor(values_t["y3_0"], values_t["y3_1"], values_t["d_x5"]):
        exit("(y3_0, y3_1) --> can't --> dx5;")


def key_r(a, b, rou):
    if rou == 1:
        c = 0x02
    else:
        c = 0x04

    if not (sbox[a[1][3]] ^ c ^ a[0][0]) == b[0][0]:
        exit("k00, sk13 --> can't --> k00")
    if not sbox[a[2][3]] ^ a[1][0] == b[1][0]:
        exit("k10, sk23 --> can't --> k10")
    if not sbox[a[3][3]] ^ a[2][0] == b[2][0]:
        exit("k20, sk33 --> can't --> k20")
    if not sbox[a[0][3]] ^ a[3][0] == b[3][0]:
        exit("k30, sk03 --> can't --> k30")
    for i in range(1, 4):
        for j in range(0, 4):
            if not (b[j][i - 1] ^ a[j][i]) == b[j][i]:
                exit("k: jth row, ith col error")


def verify_key(values_t):
    k1 = values_t["k1"]
    k2 = values_t["k2"]
    k3 = values_t["k3"]
    key_r(k1, k2, 1)
    key_r(k2, k3, 2)


def trail_get(file1):

    all_result = result_parsing(file1)
    for i in range(0, len(all_result)):
        ar = all_result[i]
        tv0, tv1, dv = single_trail(ar)
        verify_trail(tv0, 0)
        verify_trail(tv1, 1)
        verify_key(tv0)
        for t in tv1.keys():
            tv0[t] = tv1[t]
        for t in dv.keys():
            tv0[t] = dv[t]
        verify_diff(tv0)


def all_trail_verify():
    for i in range(0, 16):
        for j in range(0, 16):
            file1 = "record_file_{}_{}.txt".format(i, j)
            trail_get(file1)
            print("{}-{} result verify done!\n".format(i, j))


all_trail_verify()

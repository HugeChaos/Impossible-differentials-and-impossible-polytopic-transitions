#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import os
import copy
import random


s9_box = [0x1c3, 0x0cb, 0x153, 0x19f, 0x1e3, 0x0e9, 0x0fb, 0x035, 0x181, 0x0b9, 0x117, 0x1eb, 0x133, 0x009, 0x02d, 0x0d3,
          0x0c7, 0x14a, 0x037, 0x07e, 0x0eb, 0x164, 0x193, 0x1d8, 0x0a3, 0x11e, 0x055, 0x02c, 0x01d, 0x1a2, 0x163, 0x118,
          0x14b, 0x152, 0x1d2, 0x00f, 0x02b, 0x030, 0x13a, 0x0e5, 0x111, 0x138, 0x18e, 0x063, 0x0e3, 0x0c8, 0x1f4, 0x01b,
          0x001, 0x09d, 0x0f8, 0x1a0, 0x16d, 0x1f3, 0x01c, 0x146, 0x07d, 0x0d1, 0x082, 0x1ea, 0x183, 0x12d, 0x0f4, 0x19e,
          0x1d3, 0x0dd, 0x1e2, 0x128, 0x1e0, 0x0ec, 0x059, 0x091, 0x011, 0x12f, 0x026, 0x0dc, 0x0b0, 0x18c, 0x10f, 0x1f7,
          0x0e7, 0x16c, 0x0b6, 0x0f9, 0x0d8, 0x151, 0x101, 0x14c, 0x103, 0x0b8, 0x154, 0x12b, 0x1ae, 0x017, 0x071, 0x00c,
          0x047, 0x058, 0x07f, 0x1a4, 0x134, 0x129, 0x084, 0x15d, 0x19d, 0x1b2, 0x1a3, 0x048, 0x07c, 0x051, 0x1ca, 0x023,
          0x13d, 0x1a7, 0x165, 0x03b, 0x042, 0x0da, 0x192, 0x0ce, 0x0c1, 0x06b, 0x09f, 0x1f1, 0x12c, 0x184, 0x0fa, 0x196,
          0x1e1, 0x169, 0x17d, 0x031, 0x180, 0x10a, 0x094, 0x1da, 0x186, 0x13e, 0x11c, 0x060, 0x175, 0x1cf, 0x067, 0x119,
          0x065, 0x068, 0x099, 0x150, 0x008, 0x007, 0x17c, 0x0b7, 0x024, 0x019, 0x0de, 0x127, 0x0db, 0x0e4, 0x1a9, 0x052,
          0x109, 0x090, 0x19c, 0x1c1, 0x028, 0x1b3, 0x135, 0x16a, 0x176, 0x0df, 0x1e5, 0x188, 0x0c5, 0x16e, 0x1de, 0x1b1,
          0x0c3, 0x1df, 0x036, 0x0ee, 0x1ee, 0x0f0, 0x093, 0x049, 0x09a, 0x1b6, 0x069, 0x081, 0x125, 0x00b, 0x05e, 0x0b4,
          0x149, 0x1c7, 0x174, 0x03e, 0x13b, 0x1b7, 0x08e, 0x1c6, 0x0ae, 0x010, 0x095, 0x1ef, 0x04e, 0x0f2, 0x1fd, 0x085,
          0x0fd, 0x0f6, 0x0a0, 0x16f, 0x083, 0x08a, 0x156, 0x09b, 0x13c, 0x107, 0x167, 0x098, 0x1d0, 0x1e9, 0x003, 0x1fe,
          0x0bd, 0x122, 0x089, 0x0d2, 0x18f, 0x012, 0x033, 0x06a, 0x142, 0x0ed, 0x170, 0x11b, 0x0e2, 0x14f, 0x158, 0x131,
          0x147, 0x05d, 0x113, 0x1cd, 0x079, 0x161, 0x1a5, 0x179, 0x09e, 0x1b4, 0x0cc, 0x022, 0x132, 0x01a, 0x0e8, 0x004,
          0x187, 0x1ed, 0x197, 0x039, 0x1bf, 0x1d7, 0x027, 0x18b, 0x0c6, 0x09c, 0x0d0, 0x14e, 0x06c, 0x034, 0x1f2, 0x06e,
          0x0ca, 0x025, 0x0ba, 0x191, 0x0fe, 0x013, 0x106, 0x02f, 0x1ad, 0x172, 0x1db, 0x0c0, 0x10b, 0x1d6, 0x0f5, 0x1ec,
          0x10d, 0x076, 0x114, 0x1ab, 0x075, 0x10c, 0x1e4, 0x159, 0x054, 0x11f, 0x04b, 0x0c4, 0x1be, 0x0f7, 0x029, 0x0a4,
          0x00e, 0x1f0, 0x077, 0x04d, 0x17a, 0x086, 0x08b, 0x0b3, 0x171, 0x0bf, 0x10e, 0x104, 0x097, 0x15b, 0x160, 0x168,
          0x0d7, 0x0bb, 0x066, 0x1ce, 0x0fc, 0x092, 0x1c5, 0x06f, 0x016, 0x04a, 0x0a1, 0x139, 0x0af, 0x0f1, 0x190, 0x00a,
          0x1aa, 0x143, 0x17b, 0x056, 0x18d, 0x166, 0x0d4, 0x1fb, 0x14d, 0x194, 0x19a, 0x087, 0x1f8, 0x123, 0x0a7, 0x1b8,
          0x141, 0x03c, 0x1f9, 0x140, 0x02a, 0x155, 0x11a, 0x1a1, 0x198, 0x0d5, 0x126, 0x1af, 0x061, 0x12e, 0x157, 0x1dc,
          0x072, 0x18a, 0x0aa, 0x096, 0x115, 0x0ef, 0x045, 0x07b, 0x08d, 0x145, 0x053, 0x05f, 0x178, 0x0b2, 0x02e, 0x020,
          0x1d5, 0x03f, 0x1c9, 0x1e7, 0x1ac, 0x044, 0x038, 0x014, 0x0b1, 0x16b, 0x0ab, 0x0b5, 0x05a, 0x182, 0x1c8, 0x1d4,
          0x018, 0x177, 0x064, 0x0cf, 0x06d, 0x100, 0x199, 0x130, 0x15a, 0x005, 0x120, 0x1bb, 0x1bd, 0x0e0, 0x04f, 0x0d6,
          0x13f, 0x1c4, 0x12a, 0x015, 0x006, 0x0ff, 0x19b, 0x0a6, 0x043, 0x088, 0x050, 0x15f, 0x1e8, 0x121, 0x073, 0x17e,
          0x0bc, 0x0c2, 0x0c9, 0x173, 0x189, 0x1f5, 0x074, 0x1cc, 0x1e6, 0x1a8, 0x195, 0x01f, 0x041, 0x00d, 0x1ba, 0x032,
          0x03d, 0x1d1, 0x080, 0x0a8, 0x057, 0x1b9, 0x162, 0x148, 0x0d9, 0x105, 0x062, 0x07a, 0x021, 0x1ff, 0x112, 0x108,
          0x1c0, 0x0a9, 0x11d, 0x1b0, 0x1a6, 0x0cd, 0x0f3, 0x05c, 0x102, 0x05b, 0x1d9, 0x144, 0x1f6, 0x0ad, 0x0a5, 0x03a,
          0x1cb, 0x136, 0x17f, 0x046, 0x0e1, 0x01e, 0x1dd, 0x0e6, 0x137, 0x1fa, 0x185, 0x08c, 0x08f, 0x040, 0x1b5, 0x0be,
          0x078, 0x000, 0x0ac, 0x110, 0x15e, 0x124, 0x002, 0x1bc, 0x0a2, 0x0ea, 0x070, 0x1fc, 0x116, 0x15c, 0x04c, 0x1c2]


s7_box = [0x1b, 0x32, 0x33, 0x5a, 0x3b, 0x10, 0x17, 0x54, 0x5b, 0x1a, 0x72, 0x73, 0x6b, 0x2c, 0x66, 0x49,
          0x1f, 0x24, 0x13, 0x6c, 0x37, 0x2e, 0x3f, 0x4a, 0x5d, 0x0f, 0x40, 0x56, 0x25, 0x51, 0x1c, 0x04,
          0x0b, 0x46, 0x20, 0x0d, 0x7b, 0x35, 0x44, 0x42, 0x2b, 0x1e, 0x41, 0x14, 0x4b, 0x79, 0x15, 0x6f,
          0x0e, 0x55, 0x09, 0x36, 0x74, 0x0c, 0x67, 0x53, 0x28, 0x0a, 0x7e, 0x38, 0x02, 0x07, 0x60, 0x29,
          0x19, 0x12, 0x65, 0x2f, 0x30, 0x39, 0x08, 0x68, 0x5f, 0x78, 0x2a, 0x4c, 0x64, 0x45, 0x75, 0x3d,
          0x59, 0x48, 0x03, 0x57, 0x7c, 0x4f, 0x62, 0x3c, 0x1d, 0x21, 0x5e, 0x27, 0x6a, 0x70, 0x4d, 0x3a,
          0x01, 0x6d, 0x6e, 0x63, 0x18, 0x77, 0x23, 0x05, 0x26, 0x76, 0x00, 0x31, 0x2d, 0x7a, 0x7f, 0x61,
          0x50, 0x22, 0x11, 0x06, 0x47, 0x16, 0x52, 0x4e, 0x71, 0x3e, 0x69, 0x43, 0x34, 0x5c, 0x58, 0x7d]


def __xor_operate_1(var1, var2, var3):
    return "ASSERT(BVXOR({}, {}) = {});\n".format(var1, var2, var3)


def xor_operate(var1, var2, var3):
    xor_statement = ""
    for var_index in range(0, len(var1)):
        xor_statement += __xor_operate_1(var1[var_index], var2[var_index], var3[var_index])
    return xor_statement


def s9(var1, var2):
    v1 = "{}@{}@{}@{}@{}@{}@{}@{}@{}".format(var1[8], var1[7], var1[6], var1[5], var1[4], var1[3], var1[2], var1[1], var1[0])
    v2 = "{}@{}@{}@{}@{}@{}@{}@{}@{}".format(var2[8], var2[7], var2[6], var2[5], var2[4], var2[3], var2[2], var2[1], var2[0])
    statement1 = "0bin111000011"
    for i in range(1, 512):
        iv = "0bin"
        for j in range(0, 9):
            iv += "{}".format((i >>(8 - j)) & 0x1)
        siv = "0bin"
        for j in range(0, 9):
            siv += "{}".format((s9_box[i] >> (8 - j)) & 0x1)
        statement1 = "(IF {} = {} THEN {} ELSE {} ENDIF)".format(v1, iv, siv, statement1)
    statement = "ASSERT({} = {});\n".format(v2, statement1)
    return statement


def s7(var1, var2):
    v1 = "{}@{}@{}@{}@{}@{}@{}".format(var1[6], var1[5], var1[4], var1[3], var1[2], var1[1], var1[0])
    v2 = "{}@{}@{}@{}@{}@{}@{}".format(var2[6], var2[5], var2[4], var2[3], var2[2], var2[1], var2[0])
    statement1 = "0bin0011011"
    for i in range(1, 128):
        iv = "0bin"
        for j in range(0, 7):
            iv += "{}".format((i >> (6 - j)) & 0x1)
        siv = "0bin"
        for j in range(0, 7):
            siv += "{}".format((s7_box[i] >> (6 - j)) & 0x1)
        statement1 = "(IF {} = {} THEN {} ELSE {} ENDIF)".format(v1, iv, siv, statement1)
    statement = "ASSERT({} = {});\n".format(v2, statement1)
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


def state_var_dec(var, var_size):
    var0 = ["p0_{}_{}".format(var, i) for i in range(0, var_size)]
    var1 = ["p1_{}_{}".format(var, i) for i in range(0, var_size)]
    return var0, var1


def diff_var_dec(var, round_index, var_size):
    return ["d_{}_{}_{}".format(var, round_index, i) for i in range(0, var_size)]


def key_var_dec(var, var_size):
    key1 = ["k_{}_{}".format(var, i) for i in range(0, var_size)]
    return key1


def fl_1(x, y, kli1, kli2):
    statement = ""
    xr = x[0:16]
    xl = x[16:32]
    yr = y[0:16]
    yl = y[16:32]
    statement += xor_operate(["(({})&({}))".format(xl[i], kli1[i]) for i in range(0, 16)], xr, yr)
    statement += xor_operate(["{}|{}".format(yr[i], kli2[i]) for i in range(0, 16)], xl, yl)
    return statement


def fl_layer(rin, rout, lin, lout, rou):
    kl_l_1 = key_var_dec("kl_{}_l_1".format(rou), 16)
    kl_l_2 = key_var_dec("kl_{}_l_2".format(rou), 16)
    kl_r_1 = key_var_dec("kl_{}_r_1".format(rou), 16)
    kl_r_2 = key_var_dec("kl_{}_r_2".format(rou), 16)
    all_var = [copy.deepcopy(kl_l_1), copy.deepcopy(kl_l_2), copy.deepcopy(kl_r_1), copy.deepcopy(kl_r_2)]
    statement = fl_1(copy.deepcopy(lin[0]), copy.deepcopy(lout[0]), kl_l_1, kl_l_2)
    statement += fl_1(copy.deepcopy(lin[1]), copy.deepcopy(lout[1]), kl_l_1, kl_l_2)
    statement += fl_1(copy.deepcopy(rin[0]), copy.deepcopy(rout[0]), kl_r_1, kl_r_2)
    statement += fl_1(copy.deepcopy(rin[1]), copy.deepcopy(rout[1]), kl_r_1, kl_r_2)
    return statement, all_var


def fi_1(x, y, b, ki):
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
        statement += "ASSERT(BVXOR({}, {}) = {});\n".format(copy.deepcopy(b[1][i]), copy.deepcopy(b[2][i]), copy.deepcopy(b[3][i]))
    for i in range(0, 7):
        statement += "ASSERT(BVXOR({}, {}) = {});\n".format(copy.deepcopy(b[3][i]), copy.deepcopy(ki[0][i]),
                                                            copy.deepcopy(yl[i]))
    for i in range(0, 9):
        statement += "ASSERT(BVXOR({}, {}) = {});\n".format(copy.deepcopy(b[1][i]), copy.deepcopy(ki[1][i]),
                                                            copy.deepcopy(b[4][i]))
    statement += s9(b[4], b[5])
    for i in range(0, 7):
        statement += "ASSERT(BVXOR({}, {}) = {});\n".format(b[5][i], yl[i], yr[i])
    for i in range(7, 9):
        statement += "ASSERT({} = {});\n".format(b[5][i], yr[i])
    return statement


def fi_layer(x, y, rou, ind):
    all_var = []
    statement = ""
    b0 = state_var_dec("b_{}_{}_0".format(rou, ind), 9)
    b1 = state_var_dec("b_{}_{}_1".format(rou, ind), 9)
    b2 = state_var_dec("b_{}_{}_2".format(rou, ind), 7)
    b3 = state_var_dec("b_{}_{}_3".format(rou, ind), 7)
    b4 = state_var_dec("b_{}_{}_4".format(rou, ind), 9)
    b5 = state_var_dec("b_{}_{}_5".format(rou, ind), 9)
    all_var += copy.deepcopy(b0)
    all_var += copy.deepcopy(b1)
    all_var += copy.deepcopy(b2)
    all_var += copy.deepcopy(b3)
    all_var += copy.deepcopy(b4)
    all_var += copy.deepcopy(b5)
    kl = key_var_dec("ki_{}_{}_0".format(rou, ind), 7)
    kr = key_var_dec("ki_{}_{}_1".format(rou, ind), 9)
    all_var.append(copy.deepcopy(kl))
    all_var.append(copy.deepcopy(kr))
    statement += fi_1(x[0], y[0], [b0[0], b1[0], b2[0], b3[0], b4[0], b5[0]], [kl, kr])
    statement += fi_1(x[1], y[1], [b0[1], b1[1], b2[1], b3[1], b4[1], b5[1]], [kl, kr])
    return statement, all_var


def fo_layer(x, y, rou):
    statement = ""
    all_var = []
    ko0 = key_var_dec("ko_{}_0".format(rou), 16)
    ko1 = key_var_dec("ko_{}_1".format(rou), 16)
    ko2 = key_var_dec("ko_{}_2".format(rou), 16)
    ko3 = key_var_dec("ko_{}_3".format(rou), 16)
    all_var.append(copy.deepcopy(ko0))
    all_var.append(copy.deepcopy(ko1))
    all_var.append(copy.deepcopy(ko2))
    all_var.append(copy.deepcopy(ko3))
    p0 = state_var_dec("p_{}_0".format(rou), 16)
    p1 = state_var_dec("p_{}_1".format(rou), 16)
    p2 = state_var_dec("p_{}_2".format(rou), 16)
    q0 = state_var_dec("q_{}_0".format(rou), 16)
    q1 = state_var_dec("q_{}_1".format(rou), 16)
    q2 = state_var_dec("q_{}_2".format(rou), 16)
    a0 = state_var_dec("a_{}_0".format(rou), 16)
    a1 = state_var_dec("a_{}_1".format(rou), 16)
    all_var += copy.deepcopy(p0)
    all_var += copy.deepcopy(p1)
    all_var += copy.deepcopy(p2)
    all_var += copy.deepcopy(q0)
    all_var += copy.deepcopy(q1)
    all_var += copy.deepcopy(q2)
    all_var += copy.deepcopy(a0)
    all_var += copy.deepcopy(a1)
    statement += xor_operate(x[0][16:32], ko0, p0[0])
    statement += xor_operate(x[1][16:32], ko0, p0[1])
    statement0, all_var0 = fi_layer(p0, q0, rou, 0)
    statement += statement0
    all_var += all_var0
    statement += xor_operate(q0[0], x[0][0:16], a0[0])
    statement += xor_operate(q0[1], x[1][0:16], a0[1])
    statement += xor_operate(x[0][0:16], ko1, p1[0])
    statement += xor_operate(x[1][0:16], ko1, p1[1])
    statement1, all_var1 = fi_layer(p1, q1, rou, 1)
    statement += statement1
    all_var += all_var1
    statement += xor_operate(q1[0], a0[0], a1[0])
    statement += xor_operate(q1[1], a0[1], a1[1])
    statement += xor_operate(a0[0], ko2, p2[0])
    statement += xor_operate(a0[1], ko2, p2[1])
    statement2, all_var2 = fi_layer(p2, q2, rou, 2)
    statement += statement2
    all_var += all_var2
    statement += xor_operate(q2[0], a1[0], y[0][0:16])
    statement += xor_operate(q2[1], a1[1], y[1][0:16])
    statement += xor_operate(a1[0], ko3, y[0][16:32])
    statement += xor_operate(a1[1], ko3, y[1][16:32])
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

    l0 = state_var_dec("l_{}".format(round_inf[0]), cd["branch_size"])
    r0 = state_var_dec("r_{}".format(round_inf[0]), cd["branch_size"])

    begin_values = copy.deepcopy([r0[0] + l0[0], r0[1] + l0[1]])

    for rou in range(round_inf[0], round_inf[1]):
        all_var += copy.deepcopy(l0)
        all_var += copy.deepcopy(r0)

        l1 = state_var_dec("l_{}".format(rou + 1), cd["branch_size"])
        r1 = state_var_dec("r_{}".format(rou + 1), cd["branch_size"])

        if rou % 2 == 0:
            w = state_var_dec("w_{}".format(rou), cd["branch_size"])
            v = state_var_dec("v_{}".format(rou), cd["branch_size"])
            all_var += copy.deepcopy(w)
            all_var += copy.deepcopy(v)
            statement1, all_var1 = fl_layer(r0, v, l0, r1, rou)
            statement2, all_var2 = fo_layer(r1, w, rou)
            statement += statement1
            statement += statement2
            all_var += copy.deepcopy(all_var1)
            all_var += copy.deepcopy(all_var2)
            statement += xor_operate(w[0], v[0], l1[0])
            statement += xor_operate(w[1], v[1], l1[1])
        else:
            w = state_var_dec("w_{}".format(rou), cd["branch_size"])
            all_var += copy.deepcopy(w)
            statement2, all_var2 = fo_layer(l0, w, rou)
            statement += statement2
            all_var += copy.deepcopy(all_var2)
            statement += var_equal(r1[0], l0[0])
            statement += var_equal(r1[1], l0[1])
            statement += xor_operate(r0[0], w[0], l1[0])
            statement += xor_operate(r0[1], w[1], l1[1])
        l0 = copy.deepcopy(l1)
        r0 = copy.deepcopy(r1)

    all_var += copy.deepcopy(l0)
    all_var += copy.deepcopy(r0)

    end_values = copy.deepcopy([r0[0] + l0[0], r0[1] + l0[1]])

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
    dx0 = diff_var_dec("x", mode[1][0], cd["cipher_size"])
    dxn = diff_var_dec("x", mode[1][1], cd["cipher_size"])
    all_var.append(dx0)
    all_var.append(dxn)
    statement += header(all_var)
    statement += xor_operate(begin_values[0], begin_values[1], dx0)
    statement += var_value_assign(dx0, cd["b1"])
    statement += statement1
    statement += xor_operate(end_values[0], end_values[1], dxn)
    statement += var_value_assign(dxn, cd["e1"])
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

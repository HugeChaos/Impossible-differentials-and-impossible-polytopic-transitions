#!/usr/bin/python
# -*- coding: UTF-8 -*-


def xtime_AES(x):
    if (x & 0x80) != 0:
        return ((x << 1) & 0xff) ^ 0x1b
    else:
        return (x << 1) & 0xff


def multiply_AES(a, b):
    temp = [0 for i in range(0, 8)]
    temp[0] = a
    for i in range(1, 8):
        temp[i] = xtime_AES(temp[i - 1])
    tempmultiply = (b & 0x01) * a
    for i in range(1, 8):
        tempmultiply ^= (((b >> i) & 0x01) * temp[i])
    return tempmultiply


def mixcolumn(vec):
    res = [[0 for j in range(0, 4)] for i in range(0, 4)]
    mc = [[0x02, 0x03, 0x01, 0x01],\
          [0x01, 0x02, 0x03, 0x01],\
          [0x01, 0x01, 0x02, 0x03],\
          [0x03, 0x01, 0x01, 0x02]]
    for c in range(0, 4):
        for i in range(0, 4):
            for j in range(0, 4):
                res[i][c] ^= multiply_AES(mc[i][j], vec[j][c])
    return res


def rev_mixcolumn(vec):
    res = [[0 for j in range(0, 4)] for i in range(0, 4)]
    mc = [[0x0e, 0x0b, 0x0d, 0x09], \
          [0x09, 0x0e, 0x0b, 0x0d], \
          [0x0d, 0x09, 0x0e, 0x0b], \
          [0x0b, 0x0d, 0x09, 0x0e]]
    for c in range(0, 4):
        for i in range(0, 4):
            for j in range(0, 4):
                res[i][c] ^= multiply_AES(mc[i][j], vec[j][c])
    return res


def sr_mc(vec):
    sc = [0, 1, 2, 3]
    after_sc = [[0 for j in range(0, 4)] for i in range(0, 4)]
    for i in range(0, 4):
        for j in range(0, 4):
            after_sc[i][j] = vec[i][(j + sc[i]) % 4]
    return mixcolumn(after_sc)


def rev_sr_mc(vec):
    before_rev_sr = rev_mixcolumn(vec)
    sc = [0, 1, 2, 3]
    after_rev_sc = [[0 for j in range(0, 4)] for i in range(0, 4)]
    for i in range(0, 4):
        for j in range(0, 4):
            after_rev_sc[i][j] = before_rev_sr[i][(j - sc[i]) % 4]
    return after_rev_sc



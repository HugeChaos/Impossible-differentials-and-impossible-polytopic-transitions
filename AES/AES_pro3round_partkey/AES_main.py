#!/usr/bin/python
# -*- coding: UTF-8 -*-

import model_build.cipher_specify as mbc
import model_build.parsing as mbp
import AES_model as am
import model_build.primitives_rules_sat as mp
import AES_finite_multi as multiuply
import copy
import time


if __name__ == "__main__":

    cd = dict()

    cd["cipher_name"] = "AES"

    cd["cipher_size"] = 128
    cd["sbox_size"] = 8
    cd["sbox_num"] = 16
    cd["sp"] = [4, 4, 8]

    cd["sbox_logic"] = mbp.parsing_s_box("sat", cd["sbox_size"], mbc.aes_sbox)
    f = open("sbox_logic.txt", "w")
    for row in cd["sbox_logic"]:
        f.write(str(row) + "\n")
    f.close()

    cd["constant"] = [0, 3, 2, 1]

    cd["mix_column"] = mbp.parsing_matrix(mbc.aes_mix_column, mbc.aes_irr_poly)
    f = open("mix_column.txt", "w")
    for row in cd["mix_column"]:
        f.write(str(row) + "\n")
    f.close()

    cd["b0"] = mp.list2square([0 for i in range(0, cd["cipher_size"])], cd["sp"])
    cd["e0"] = mp.list2square([0 for i in range(0, cd["cipher_size"])], cd["sp"])
    zero_vector = [0 for i in range(0, cd["cipher_size"])]

    cd["mode"] = 1
    round_i = 5
    cd["record_file"] = cd["cipher_name"] + "_record_mode{}.txt".format(cd["mode"])
    cd["time_record"] = cd["cipher_name"] + "_time_record_mode{}.txt".format(cd["mode"])

    cd["solve_file"] = cd["cipher_name"] + "round{}_model.stp".format(round_i)

    b0 = [[2, 1, 1, 3],
          [4, 2, 2, 6],
          [195, 236, 236, 47]]
    b1 = [[3, 2, 1, 1],
          [6, 4, 2, 2],
          [47, 195, 236, 236]]
    b2 = [[1, 3, 2, 1],
          [2, 6, 4, 2],
          [236, 47, 195, 236]]
    b3 = [[1, 1, 3, 2],
          [2, 2, 6, 4],
          [236, 236, 47, 195]]
    bb = [b0, b1, b2, b3]
    bs = [[list() for j in range(0, 4)] for i in range(0, 4)]
    for i in range(0, 4):
        for j in range(0, 4):
            column_num = (j - i) % 4
            for b_i in bb[i]:
                temp = [[0 for jj in range(0, 4)] for ii in range(0, 4)]
                for kk in range(0, 4):
                    temp[kk][column_num] = b_i[kk]
                bs[i][j].append(temp)

    es = [[list() for j1 in range(0, 4)] for i1 in range(0, 4)]
    es[0][0] = [[9, 0, 0, 0], [0, 6, 0, 0], [0, 0, 1, 0], [0, 0, 0, 3]]
    es[0][1] = [[0, 9, 0, 0], [0, 0, 6, 0], [0, 0, 0, 1], [3, 0, 0, 0]]
    es[0][2] = [[0, 0, 9, 0], [0, 0, 0, 6], [1, 0, 0, 0], [0, 3, 0, 0]]
    es[0][3] = [[0, 0, 0, 9], [6, 0, 0, 0], [0, 1, 0, 0], [0, 0, 3, 0]]

    es[1][3] = [[3, 0, 0, 0], [0, 9, 0, 0], [0, 0, 6, 0], [0, 0, 0, 1]]
    es[1][0] = [[0, 3, 0, 0], [0, 0, 9, 0], [0, 0, 0, 6], [1, 0, 0, 0]]
    es[1][1] = [[0, 0, 3, 0], [0, 0, 0, 9], [6, 0, 0, 0], [0, 1, 0, 0]]
    es[1][2] = [[0, 0, 0, 3], [9, 0, 0, 0], [0, 6, 0, 0], [0, 0, 1, 0]]

    es[2][2] = [[1, 0, 0, 0], [0, 3, 0, 0], [0, 0, 9, 0], [0, 0, 0, 6]]
    es[2][3] = [[0, 1, 0, 0], [0, 0, 3, 0], [0, 0, 0, 9], [6, 0, 0, 0]]
    es[2][0] = [[0, 0, 1, 0], [0, 0, 0, 3], [9, 0, 0, 0], [0, 6, 0, 0]]
    es[2][1] = [[0, 0, 0, 1], [3, 0, 0, 0], [0, 9, 0, 0], [0, 0, 6, 0]]

    es[3][1] = [[6, 0, 0, 0], [0, 1, 0, 0], [0, 0, 3, 0], [0, 0, 0, 9]]
    es[3][2] = [[0, 6, 0, 0], [0, 0, 1, 0], [0, 0, 0, 3], [9, 0, 0, 0]]
    es[3][3] = [[0, 0, 6, 0], [0, 0, 0, 1], [3, 0, 0, 0], [0, 9, 0, 0]]
    es[3][0] = [[0, 0, 0, 6], [1, 0, 0, 0], [0, 3, 0, 0], [0, 0, 9, 0]]

    ttt1 = time.time()
    for square_i in range(0, 16):
        for square_j in range(0, 16):
            flag_trail = True
            count = 0
            tt1 = time.time()
            c_bv1 = copy.copy(bs[square_i // 4][square_i % 4])
            search_space = list()
            for iv in bs[square_i // 4][square_i % 4]:
                search_space.append([iv, es[square_j // 4][square_j % 4]])
            f = open("search_space.txt", "a")
            f.write("{}-{}\n".format(square_i, square_j))
            for ss in search_space:
                f.write(str(ss[0]) + "\n")
                f.write(str(ss[1]) + "\n\n\n")
            f.close()
            for sl in search_space:
                count += 1
                c_bv = sl[0]
                c_ev = sl[1]
                print(square_i, square_j, count, c_bv, c_ev)
                cd["b1"] = [[[0 for k in range(0, 8)] for j in range(0, 4)] for i in range(0, 4)]
                cd["e1"] = [[[0 for k in range(0, 8)] for j in range(0, 4)] for i in range(0, 4)]
                for i in range(0, 4):
                    for j in range(0, 4):
                        for k in range(0, 8):
                            cd["b1"][i][j][k] = (c_bv[i][j] >> k) & 0x1
                            cd["e1"][i][j][k] = (c_ev[i][j] >> k) & 0x1
                t1 = time.time()
                mode = [cd["mode"], [0, round_i]]
                am.model_build(cd, mode)
                flag, res = mp.solver1(cd["solve_file"])
                t2 = time.time()
                f = open("record_file_{}_{}.txt".format(square_i, square_j), "a")
                f.write("When then bv = {} and ev = {}\n".format(c_bv, c_ev))
                f.write("the solver time is {}\n".format(t2 - t1))
                f.write(res + "\n")
                f.close()
                if flag:
                    flag_trail = False
            tt2 = time.time()

            if flag_trail:
                f = open("res.txt", "a")
                f.write("After {} seconds, we prove {} --> {} is possible.\n".format(tt2 - tt1, square_i, square_j))
                f.close()
    ttt2 = time.time()
    f = open("res.txt", "a")
    f.write("Total consume time {} seconds.\n".format(ttt2 - ttt1))
    f.close()







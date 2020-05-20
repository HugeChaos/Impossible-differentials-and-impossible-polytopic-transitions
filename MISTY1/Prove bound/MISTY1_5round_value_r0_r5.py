#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MISTY1_model as mm
import os
import time
import copy


if __name__ == "__main__":

    cd = dict()

    cd["cipher_name"] = "MISTY1_5round_value_r0_r5"

    cd["cipher_size"] = 64
    cd["branch_size"] = 32
    cd["mode"] = 0
    distinguish_find = True
    round_i = 3
    folder = cd["cipher_name"] + "_mode{}".format(cd["mode"])

    if not os.path.exists(folder):
        os.mkdir(folder)

    cd["record_file"] = folder + "////" + cd["cipher_name"] + "_record_mode{}.txt".format(cd["mode"])
    cd["time_record"] = folder + "////" + cd["cipher_name"] + "_time_record_mode{}.txt".format(cd["mode"])

    fo_diff = [[0, 1342289832], \
               [1, 1431425740], \
               [2, 1237348154], \
               [3, 2425537519], \
               [4, 689744435], \
               [5, 1627271988], \
               [6, 2236463421], \
               [7, 8871764755], \
               [8, 4855845197], \
               [9, 1120896096], \
               [10, 2161393589], \
               [11, 8596924213], \
               [12, 4313529982], \
               [13, 17423012], \
               [14, 96274495], \
               [15, 150668486], \
               [16, 1342350165], \
               [17, 1431374298], \
               [18, 1237809755], \
               [19, 2426119948], \
               [20, 688854685], \
               [21, 1625132968], \
               [22, 2232242120], \
               [23, 8863498805], \
               [24, 4839096090], \
               [25, 1087226533], \
               [26, 2228651630], \
               [27, 8731122411], \
               [28, 4581897021], \
               [29, 554277457], \
               [30, 1169969832], \
               [31, 2298211202]]

    fo_dict = dict()
    for i in range(0, len(fo_diff)):
        fo_dict[fo_diff[i][0]] = fo_diff[i][1]

    search_space = list()
    input_list = dict()
    for i in range(0, 32):
        b1 = [0 for bi in range(0, cd["cipher_size"])]
        b1[i + 32] = 1
        input_list[i + 32] = copy.deepcopy(b1)
    out_list = dict()
    for j in range(0, 32):
        e1 = [0 for ei in range(0, cd["cipher_size"])]
        e1[32 + j] = 1
        e1_down = fo_dict[j]
        for ejj in range(0, 32):
            e1[ejj] = (e1_down >> ejj) & 0x1
        out_list[j] = copy.deepcopy(e1)

    for i in range(32, 64):
        for j in range(0, 32):
            search_space.append([i, j])

    cd["b0"] = [0 for i in range(0, 64)]
    cd["e0"] = [0 for i in range(0, 64)]

    distinguish_find = True

    t1 = time.time()

    cd["solve_file"] = folder + "////" + cd["cipher_name"] + "_round{}_model.stp".format(round_i)
    search_count = 0
    distinguish_count = 0
    for sp in search_space:
        search_count += 1
        cd["b1"] = input_list[sp[0]]
        cd["e1"] = out_list[sp[1]]
        mode = [cd["mode"], [0, round_i]]
        s_t1 = time.time()
        mm.model_build(cd, mode)
        flag, res = mm.solver2(cd["solve_file"])
        s_t2 = time.time()
        print(s_t2 - s_t1)
        if flag:
            distinguish_count += 1

            rf = open(cd["record_file"], "a")
            rf.write("*" * 20)
            rf.write("{} 3-round impossible distinguish found\n".format(distinguish_count))
            rf.write("when the values:\n")
            rf.write("b1 = {}\n".format(str(cd["b1"])))
            rf.write("e1 = {}\n".format(str(cd["e1"])))
            rf.close()
            distinguish_find = True
        else:
            cd["res_file"] = folder + "////" + cd["cipher_name"] + "_{}_{}_result.txt".format(sp[0], sp[1])
            f = open(cd["res_file"], "a")
            f.write("solve time = {}\n".format(s_t2 - s_t1))
            f.write(res)
            f.close()
        print("testing: round = {}, time = {}, search_count = {}".format(round_i, s_t2 - s_t1, search_count))
    t2 = time.time()
    tf = open(cd["time_record"], "a")
    tf.write("After " + str(t2 - t1) + "time, we prove no 3-round impossible differential.\n")
    tf.close()

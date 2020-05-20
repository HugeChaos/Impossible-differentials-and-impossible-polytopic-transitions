#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import Gift64_model
import Gift64_model_diff
import time
import os
import random

if __name__ == "__main__":

    cd = dict()

    cd["cipher_name"] = "gift"

    cd["mul"] = 2

    cd["cipher_size"] = 64
    cd["sbox_size"] = 4
    cd["sbox_num"] = 16

    cd["mode"] = 1

    folder = cd["cipher_name"] + "_{}way_compare".format(cd["mul"], cd["mode"])

    if not os.path.exists(folder):
        os.mkdir(folder)

    distinguish_find = True

    search_space = list()
    pb = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    pe = [0, 4, 8, 12, 17, 21, 25, 29, 34, 38, 42, 46, 51, 55, 59, 63]
    il = list()
    ol = list()
    for i in range(0, 65536):
        bv = random.randint(1, 65535)
        ev = random.randint(1, 65535)
        if (bv not in il) and (ev not in ol):
            il.append(bv)
            ol.append(ev)
    for s in range(0, len(il)):
        b1 = [0 for bi in range(0, cd["cipher_size"])]
        e1 = [0 for ei in range(0, cd["cipher_size"])]
        for i in range(0, 16):
            b1[pb[i]] = (il[s] >> i) & 0x1
            e1[pe[i]] = (ol[s] >> i) & 0x1
        search_space.append(copy.deepcopy([b1, e1]))

    round_i = 6
    cd["record_file"] = folder + "////" + cd["cipher_name"] + "_record_mode{}.txt".format(cd["mode"])
    cd["time_record"] = folder + "////" + cd["cipher_name"] + "_time_record_mode{}.txt".format(cd["mode"])
    total_search = len(search_space)
    ttt1 = time.time()

    cd["solve_file"] = folder + "////" + cd["cipher_name"] + "_round{}_1.stp".format(round_i)
    cd["solve_file1"] = folder + "////" + cd["cipher_name"] + "_round{}_2.stp".format(round_i)
    search_count = 0
    distinguish_count = 0
    for ss in search_space:
        cd["b1"] = copy.deepcopy(ss[0])
        cd["e1"] = copy.deepcopy(ss[1])
        mode = [cd["mode"], [0, round_i]]
        t11 = time.time()
        search_count += 1
        Gift64_model.model_build(cd, mode)
        Gift64_model_diff.model_build(cd, mode)
        flag1 = Gift64_model.solver(cd["solve_file"])
        flag2 = Gift64_model.solver(cd["solve_file1"])
        t22 = time.time()
        print(t22 - t11)
        if flag1 and not flag2:
            distinguish_count += 1
            rf = open(cd["record_file"], "a")
            rf.write("*" * 20)
            rf.write("{}th {}round impossible {}way distinguish found\n".format(distinguish_count, round_i, cd["mul"]))
            rf.write("when the values:\n")
            rf.write("b1 = {}\n".format(str(cd["b1"])))
            rf.write("e1 = {}\n".format(str(cd["e1"])))
            rf.close()
        print("testing: round = {}, search_count = {}, total_search = {}".format(round_i, search_count, total_search))
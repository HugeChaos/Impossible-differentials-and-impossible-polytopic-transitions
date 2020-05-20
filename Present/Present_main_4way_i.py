#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import Present_model
import Present_model_i
import time
import os
import random

if __name__ == "__main__":

    cd = dict()

    cd["mul"] = 4

    cd["cipher_name"] = "Present"

    cd["cipher_size"] = 64
    cd["sbox_size"] = 4
    cd["sbox_num"] = 16

    cd["mode"] = 1

    folder = cd["cipher_name"] + "_mode{}_{}way_i".format(cd["mode"], cd["mul"])

    if not os.path.exists(folder):
        os.mkdir(folder)

    search_space = list()

    for i in range(0, 1):
        for i1 in range(0, 4):
            for i2 in range(i1 + 1, 4):
                b1 = [0 for ii1 in range(0, 64)]
                b2 = [0 for ii2 in range(0, 64)]
                b3 = [0 for ii3 in range(0, 64)]
                b1[4 * i + i1] = 1
                b2[4 * i + i2] = 1
                b3[4 * i + i1] = 1
                b3[4 * i + i2] = 1
                for j in range(0, 16):
                    for j1 in range(0, 4):
                        for j2 in range(j1 + 1, 4):
                            e1 = [0 for jj1 in range(0, 64)]
                            e2 = [0 for jj2 in range(0, 64)]
                            e3 = [0 for jj3 in range(0, 64)]
                            e1[4 * j + j1] = 1
                            e2[4 * j + j2] = 1
                            e3[4 * j + j1] = 1
                            e3[4 * j + j2] = 1

                            search_space.append(copy.deepcopy([b1, b2, b3, Present_model.perm_wire_value(e1),
                                                               Present_model.perm_wire_value(e2), Present_model.perm_wire_value(e3)]))

    round_i = 7
    cd["record_file"] = folder + "////" + cd["cipher_name"] + "_record_mode{}.txt".format(cd["mode"])
    cd["time_record"] = folder + "////" + cd["cipher_name"] + "_time_record_mode{}.txt".format(cd["mode"])

    ttt1 = time.time()

    cd["solve_file"] = folder + "////" + cd["cipher_name"] + "_round{}.stp".format(round_i)
    cd["solve_file1"] = folder + "////" + cd["cipher_name"] + "_round{}_1.stp".format(round_i)
    total_search = len(search_space)
    t1 = time.time()
    search_count = 0
    distinguish_count = 0
    for ss in search_space:
        cd["b1"] = copy.deepcopy(ss[0])
        cd["b2"] = copy.deepcopy(ss[1])
        cd["b3"] = copy.deepcopy(ss[2])
        cd["e1"] = copy.deepcopy(ss[3])
        cd["e2"] = copy.deepcopy(ss[4])
        cd["e3"] = copy.deepcopy(ss[5])
        mode = [cd["mode"], [0, round_i]]
        t11 = time.time()
        search_count += 1
        Present_model_i.model_build(cd, mode)
        flag1 = Present_model_i.solver(cd["solve_file1"])
        t22 = time.time()
        print(t22 - t11)
        if flag1:
            distinguish_count += 1
            rf = open(cd["record_file"], "a")
            rf.write("*" * 20)
            rf.write("{} 6-round impossible distinguish found\n".format(distinguish_count))
            rf.write("when the values:\n")
            rf.write("b1 = {}\n".format(str(cd["b1"])))
            rf.write("b2 = {}\n".format(str(cd["b2"])))
            rf.write("b3 = {}\n".format(str(cd["b3"])))
            rf.write("e1 = {}\n".format(str(cd["e1"])))
            rf.write("e2 = {}\n".format(str(cd["e2"])))
            rf.write("e3 = {}\n".format(str(cd["e3"])))
            rf.close()
        print("testing: round = {}, search_count = {}, total_search = {}".format(round_i, search_count, total_search))
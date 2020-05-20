#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import Gift64_model
import time
import os

if __name__ == "__main__":

    cd = dict()

    cd["cipher_name"] = "gift"

    cd["mul"] = 3

    cd["cipher_size"] = 64
    cd["sbox_size"] = 4
    cd["sbox_num"] = 16

    cd["mode"] = 1

    folder = cd["cipher_name"] + "_{}way_mode_{}".format(cd["mul"], cd["mode"])

    if not os.path.exists(folder):
        os.mkdir(folder)

    distinguish_find = True

    search_space = list()

    for i in range(0, 1):
        for i_value1 in [1, 2, 4, 8]:
            b1 = [0 for bii1 in range(0, cd["cipher_size"])]
            for ii1 in range(0, 4):
                b1[4 * i + ii1] = (i_value1 >> ii1) & 0x1
            for i_value2 in [1, 2, 4, 8]:
                if i_value2 == i_value1:
                    continue
                b2 = [0 for bii2 in range(0, cd["cipher_size"])]
                for ii2 in range(0, 4):
                    b2[4 * i + ii2] = (i_value2 >> ii2) & 0x1
                for j in range(0, 16):
                    for j_value1 in [1, 2, 4, 8]:
                        e1 = [0 for eii1 in range(0, cd["cipher_size"])]
                        for jj1 in range(0, 4):
                            e1[4 * j + jj1] = (j_value1 >> jj1) & 0x1
                        for j_value2 in [1, 2, 4, 8]:
                            if j_value2 == j_value1:
                                continue
                            e2 = [0 for eii2 in range(0, cd["cipher_size"])]
                            for jj2 in range(0, 4):
                                e2[4 * j + jj2] = (j_value2 >> jj2) & 0x1
                            search_space.append([b1, b2, e1, e2])

    round_i = 0
    cd["record_file"] = folder + "////" + cd["cipher_name"] + "_record_mode{}.txt".format(cd["mode"])
    cd["time_record"] = folder + "////" + cd["cipher_name"] + "_time_record_mode{}.txt".format(cd["mode"])
    total_search = len(search_space)
    ttt1 = time.time()
    while distinguish_find:
        distinguish_find = False
        round_i += 1
        cd["solve_file"] = folder + "////" + cd["cipher_name"] + "_round{}.stp".format(round_i)
        t1 = time.time()
        search_count = 0
        for ss in search_space:
            cd["b1"] = copy.deepcopy(ss[0])
            cd["b2"] = copy.deepcopy(ss[1])
            cd["e1"] = copy.deepcopy(ss[2])
            cd["e2"] = copy.deepcopy(ss[3])
            mode = [cd["mode"], [0, round_i]]
            t11 = time.time()
            search_count += 1
            Gift64_model.model_build(cd, mode)
            flag = Gift64_model.solver(cd["solve_file"])
            t22 = time.time()
            print(t22 - t11)
            if flag:
                rf = open(cd["record_file"], "a")
                rf.write("*" * 20)
                rf.write("{} round impossible {}way distinguish found\n".format(round_i, cd["mul"]))
                rf.write("when the values:\n")
                rf.write("b1 = {}\n".format(str(cd["b1"])))
                rf.write("b2 = {}\n".format(str(cd["b2"])))
                rf.write("e1 = {}\n".format(str(cd["e1"])))
                rf.write("e2 = {}\n".format(str(cd["e2"])))
                rf.close()
                distinguish_find = True
                break
            else:
                print("testing: round = {}, search_count = {}, total_search = {}".format(round_i, search_count, total_search))
        t2 = time.time()
        tf = open(cd["time_record"], "a")
        if distinguish_find:
            tf.write("After " + str(t2 - t1) + "time, we found {} rounds impossible {}way.\n\n".format(round_i, cd["mul"]))
        else:
            tf.write("After " + str(t2 - t1) + "time, we show no {} round impossible {}way.\n\n".format(round_i, cd["mul"]))
        tf.close()

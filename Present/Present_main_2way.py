#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import Present_model
import time
import os

if __name__ == "__main__":

    cd = dict()

    cd["mul"] = 2

    cd["cipher_name"] = "Present"

    cd["cipher_size"] = 64
    cd["sbox_size"] = 4
    cd["sbox_num"] = 16

    cd["mode"] = 1

    folder = cd["cipher_name"] + "_mode{}_{}way".format(cd["mode"], cd["mul"])

    if not os.path.exists(folder):
        os.mkdir(folder)

    distinguish_find = True

    search_space = list()
    for i in range(0, 16):
        for i_value in range(1, 16):
            b1 = [0 for bii in range(0, cd["cipher_size"])]
            for ii in range(0, 4):
                b1[4 * i + ii] = (i_value >> ii) & 0x1
            for j in range(0, 16):
                for j_value in range(1, 16):
                    e1 = [0 for eii in range(0, cd["cipher_size"])]
                    for jj in range(0, 4):
                        e1[4 * j + jj] = (j_value >> jj) & 0x1
                    search_space.append([copy.deepcopy(b1), copy.deepcopy(Present_model.perm_wire_value(e1))])

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
            cd["e1"] = copy.deepcopy(ss[1])
            mode = [cd["mode"], [0, round_i]]
            t11 = time.time()
            search_count += 1
            Present_model.model_build(cd, mode)
            flag = Present_model.solver(cd["solve_file"])
            t22 = time.time()
            print(t22 - t11)
            if flag:
                rf = open(cd["record_file"], "a")
                rf.write("*" * 20)
                rf.write("{} round impossible distinguish found\n".format(round_i))
                rf.write("when the values:\n")
                rf.write("b1 = {}\n".format(str(cd["b1"])))
                rf.write("e1 = {}\n".format(str(cd["e1"])))
                rf.close()
                distinguish_find = True
                break
            else:
                print("testing: round = {}, search_count = {}, total_search = {}".format(round_i, search_count, total_search))
        t2 = time.time()
        tf = open(cd["time_record"], "a")
        if distinguish_find:
            tf.write("After " + str(t2 - t1) + "time, we found {} rounds impossible differential.\n\n".format(round_i))
        else:
            tf.write("After " + str(t2 - t1) + "time, we show no {} round impossible differential.\n\n".format(round_i))
        tf.close()

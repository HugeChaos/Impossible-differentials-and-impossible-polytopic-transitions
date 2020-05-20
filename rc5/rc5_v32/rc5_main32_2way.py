#!/usr/bin/python
# -*- coding: UTF-8 -*-

import rc5_model32
import copy
import time
import os

if __name__ == "__main__":

    cd = dict()

    cd["mul"] = 2

    cd["cipher_name"] = "rc5_32_{}way".format(cd["mul"])

    cd["cipher_size"] = 32

    cd["mode"] = 1

    folder = cd["cipher_name"] + "_mode{}".format(cd["mode"])

    if not os.path.exists(folder):
        os.mkdir(folder)

    distinguish_find = True

    search_space = list()
    for i in range(0, 16):
        x = [0 for xii in range(0, 32)]
        x[i] = 1
        x[i + 16] = 1
        for j in range(0, 32):
            y = [0 for yii in range(0, 32)]
            y[j] = 1
            search_space.append([x, y])

    round_i = 0
    cd["record_file"] = folder + "\\\\" + cd["cipher_name"] + "_record_mode{}.txt".format(cd["mode"])
    cd["time_record"] = folder + "\\\\" + cd["cipher_name"] + "_time_record_mode{}.txt".format(cd["mode"])
    cd["max_round"] = folder + "\\\\" + cd["cipher_name"] + "_max_round_mode{}".format(cd["mode"])
    total_search = len(search_space)

    while distinguish_find:
        distinguish_find = False
        round_i += 1
        cd["solve_file"] = folder + "\\\\" + cd["cipher_name"] + "_round{}.stp".format(round_i)
        t1 = time.time()
        search_count = 0
        for ss in search_space:
            for i in range(0, cd["mul"] - 1):
                cd["b{}".format(i + 1)] = copy.deepcopy(ss[i])
                cd["e{}".format(i + 1)] = copy.deepcopy(ss[i + cd["mul"] - 1])
            mode = [cd["mode"], [0, round_i]]
            t11 = time.time()
            search_count += 1
            rc5_model32.model_build(cd, mode)
            flag = rc5_model32.solver(cd["solve_file"])
            t22 = time.time()
            print(t22 - t11)
            if flag:
                rf = open(cd["record_file"], "a")
                rf.write("*" * 20)
                rf.write("{} round {}way impossible found\n".format(round_i, cd["mul"]))
                rf.write("when the values:\n")
                for i in range(0, cd["mul"] - 1):
                    rf.write("b{} = {}\n".format(i + 1, str(cd["b{}".format(i + 1)])))
                for i in range(0, cd["mul"] - 1):
                    rf.write("e{} = {}\n".format(i + 1, str(cd["e{}".format(i + 1)])))
                rf.close()
                distinguish_find = True
                break
            else:
                print("testing: round = {}, search_count = {}, total_search = {}".format(round_i, search_count, total_search))
        t2 = time.time()
        tf = open(cd["time_record"], "a")
        if distinguish_find:
            tf.write("After " + str(t2 - t1) + "time, we found {} rounds  {}way impossible.\n\n".format(round_i, cd["mul"]))
        else:
            tf.write("After " + str(t2 - t1) + "time, we show no {} round  {}way impossible.\n\n".format(round_i, cd["mul"]))
        tf.close()
    print("program end\n")





#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MISTY1_model as mm
import os
import time

if __name__ == "__main__":

    cd = dict()

    cd["cipher_name"] = "MISTY1_max_round"

    cd["cipher_size"] = 64
    cd["branch_size"] = 32
    cd["mode"] = 1
    distinguish_find = True
    round_i = 4
    folder = cd["cipher_name"] + "_mode{}".format(cd["mode"])

    if not os.path.exists(folder):
        os.mkdir(folder)

    cd["record_file"] = folder + "////" + cd["cipher_name"] + "_record_mode{}.txt".format(cd["mode"])
    cd["time_record"] = folder + "////" + cd["cipher_name"] + "_time_record_mode{}.txt".format(cd["mode"])

    '''
    search_space = [[0, 43]]
    '''
    search_space = list()
    for i in range(0, 32):
        for j in range(32, 64):
            search_space.append([i, j])

    distinguish_find = True

    t1 = time.time()

    cd["solve_file"] = folder + "////" + cd["cipher_name"] + "_round{}_model.stp".format(round_i)
    search_count = 0
    distinguish_count = 0
    for sp in search_space:
        search_count += 1
        cd["b1"] = [0 for i in range(0, 64)]
        cd["e1"] = [0 for i in range(0, 64)]

        cd["b1"][sp[0]] = 1
        cd["e1"][sp[1]] = 1
        mode = [cd["mode"], [0, round_i]]
        s_t1 = time.time()
        mm.model_build(cd, mode)
        flag = mm.solver(cd["solve_file"])
        s_t2 = time.time()
        print(s_t2 - s_t1)
        if flag:
            distinguish_count += 1

            rf = open(cd["record_file"], "a")
            rf.write("*" * 20)
            rf.write("{} 4-round impossible distinguish found\n".format(distinguish_count))
            rf.write("when the values:\n")
            rf.write("b1 = {}\n".format(str(cd["b1"])))
            rf.write("e1 = {}\n".format(str(cd["e1"])))
            rf.close()
            distinguish_find = True
        print("testing: round = {}, time = {}, search_count = {}".format(round_i, s_t2 - s_t1, search_count))
    t2 = time.time()
    tf = open(cd["time_record"], "a")
    tf.write("After " + str(t2 - t1) + "time, we found total ({}) 4-round impossible differential.\n\n".format(search_count))
    tf.close()

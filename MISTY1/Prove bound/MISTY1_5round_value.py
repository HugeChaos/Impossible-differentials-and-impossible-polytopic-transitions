#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MISTY1_model as mm
import os
import time

if __name__ == "__main__":

    cd = dict()

    cd["cipher_name"] = "MISTY1_5round_value"

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

    '''
    search_space = [[0, 43]]
    '''
    search_space = list()
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
        cd["b1"] = [0 for i in range(0, 64)]
        cd["e1"] = [0 for i in range(0, 64)]

        cd["b1"][sp[0]] = 1
        cd["e1"][sp[1]] = 1
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

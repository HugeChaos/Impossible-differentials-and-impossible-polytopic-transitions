#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import PrintCipher48_model_3way
import time
import os

if __name__ == "__main__":

    cd = dict()

    cd["cipher_name"] = "PrintCipher48_3way_max_round"

    cd["cipher_size"] = 48
    cd["sbox_size"] = 3
    cd["sbox_num"] = 16

    cd["mode"] = 1

    folder = cd["cipher_name"] + "_mode_{}".format(cd["mode"])

    if not os.path.exists(folder):
        os.mkdir(folder)

    distinguish_find = True

    search_space = list()
    bs = []
    es = []
    for i in range(0, 6):
        b1 = [0 for bii in range(0, cd["cipher_size"])]
        b1[i] = 1
        bs.append(PrintCipher48_model_3way.perm_wire_value(copy.deepcopy(b1)))

    for j in range(0, 48):
        e1 = [0 for eii in range(0, cd["cipher_size"])]
        e1[j] = 1
        es.append(e1)

    for i1 in range(0, len(bs)):
        for i2 in range(i1 + 1, len(bs)):
            for j1 in range(0, len(es)):
                for j2 in range(j1 + 1, len(es)):
                    search_space.append(copy.deepcopy([bs[i1], bs[i2], es[j1], es[j2]]))

    round_i = 6
    cd["record_file"] = folder + "////" + cd["cipher_name"] + "_record_mode{}.txt".format(cd["mode"])
    cd["time_record"] = folder + "////" + cd["cipher_name"] + "_time_record_mode{}.txt".format(cd["mode"])
    total_search = len(search_space)
    ttt1 = time.time()

    distinguish_count = 0
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
        PrintCipher48_model_3way.model_build(cd, mode)
        flag = PrintCipher48_model_3way.solver(cd["solve_file"])
        t22 = time.time()
        print(t22 - t11)
        if flag:
            distinguish_count += 1
            rf = open(cd["record_file"], "a")
            rf.write("*" * 20)
            rf.write("{} 6-round impossible distinguish (3 way) found\n".format(distinguish_count))
            rf.write("when the values:\n")
            rf.write("b1 = {}\n".format(str(cd["b1"])))
            rf.write("b2 = {}\n".format(str(cd["b2"])))
            rf.write("e1 = {}\n".format(str(cd["e1"])))
            rf.write("e2 = {}\n".format(str(cd["e2"])))
            rf.close()

        print("testing: round = {}, search_count = {}, total_search = {}".format(round_i, search_count, total_search))
    t2 = time.time()
    tf = open(cd["time_record"], "a")
    if distinguish_find:
        tf.write("After " + str(t2 - t1) + "time, we found total {} 6-rounds impossible differential.\n\n".format(distinguish_count))
    tf.close()

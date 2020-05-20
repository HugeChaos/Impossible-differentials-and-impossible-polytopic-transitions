#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import PrintCipher48_model_4way
import time
import os
import random

if __name__ == "__main__":

    cd = dict()

    cd["cipher_name"] = "PrintCipher48_4way"

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
        bs.append(PrintCipher48_model_4way.perm_wire_value(copy.deepcopy(b1)))

    for j in range(0, 48):
        e1 = [0 for eii in range(0, cd["cipher_size"])]
        e1[j] = 1
        es.append(e1)

    for i1 in range(0, len(bs)):
        for i2 in range(i1 + 1, len(bs)):
            b1 = copy.deepcopy(bs[i1])
            b2 = copy.deepcopy(bs[i2])
            b3 = [0 for ii0 in range(0, cd["cipher_size"])]
            for ii1 in range(0, cd["cipher_size"]):
                b3[ii1] = b1[ii1] ^ b2[ii1]
            for j1 in range(0, len(es)):
                for j2 in range(j1 + 1, len(es)):
                    e1 = copy.deepcopy(es[j1])
                    e2 = copy.deepcopy(es[j2])
                    e3 = [0 for jj0 in range(0, cd["cipher_size"])]
                    for jj1 in range(0, cd["cipher_size"]):
                        e3[jj1] = e1[jj1] ^ e2[jj1]
                    search_space.append(copy.deepcopy([b1, b2, b3, e1, e2, e3]))
    '''bs = []
    es = []
    for i in range(0, 16):
        b1 = [0 for bii in range(0, cd["cipher_size"])]
        b1[3 * i] = 1
        bs.append(b1)

    for j in range(0, 16):
        e1 = [0 for eii in range(0, cd["cipher_size"])]
        e1[3 * j] = 1
        es.append(e1)

    count = 0
    while count < 100:
        a = random.randint(0, 15)
        b = a
        while b == a:
            b = random.randint(0, 15)
        a1 = random.randint(0, 15)
        b1 = a1
        while b1 == a1:
            b1 = random.randint(0, 15)
        lbs = [0 for ii in range(0, len(bs[a]))]
        for iii in range(0, len(bs[a])):
            lbs[iii] = bs[a][iii] ^ bs[b][iii]

        les = [0 for jj in range(0, len(es[a1]))]
        for jjj in range(0, len(es[a1])):
            les[jjj] = es[a1][jjj] ^ es[b1][jjj]

        search_space.append(copy.deepcopy([bs[a], bs[b], lbs, es[a1], es[b1], les]))
        count += 1
    cd["search_space"] = folder + "////" + cd["cipher_name"] + "search.txt"

    f = open(cd["search_space"], "w")
    count = 1
    for tuple1 in search_space:
        f.write("count{}:\n".format(count))
        count += 1
        f.write(str(tuple1) + "\n")
    f.close()'''

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
            cd["b3"] = copy.deepcopy(ss[2])
            cd["e1"] = copy.deepcopy(ss[3])
            cd["e2"] = copy.deepcopy(ss[4])
            cd["e3"] = copy.deepcopy(ss[5])
            mode = [cd["mode"], [0, round_i]]
            t11 = time.time()
            search_count += 1
            PrintCipher48_model_4way.model_build(cd, mode)
            flag = PrintCipher48_model_4way.solver(cd["solve_file"])
            t22 = time.time()
            print(t22 - t11)
            if flag:
                rf = open(cd["record_file"], "a")
                rf.write("*" * 20)
                rf.write("{} round impossible distinguish (4 way) found\n".format(round_i))
                rf.write("when the values:\n")
                rf.write("b1 = {}\n".format(str(cd["b1"])))
                rf.write("b2 = {}\n".format(str(cd["b2"])))
                rf.write("b3 = {}\n".format(str(cd["b3"])))
                rf.write("e1 = {}\n".format(str(cd["e1"])))
                rf.write("e2 = {}\n".format(str(cd["e2"])))
                rf.write("e3 = {}\n".format(str(cd["e3"])))
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

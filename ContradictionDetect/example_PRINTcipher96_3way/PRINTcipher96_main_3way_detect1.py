#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import PRINTcipher96_model_3way_detect1
import time
import os

if __name__ == "__main__":

    cd = dict()

    cd["cipher_name"] = "PrintCipher96_3way"

    cd["cipher_size"] = 96
    cd["sbox_size"] = 3
    cd["sbox_num"] = 32

    cd["mode"] = 1

    folder = cd["cipher_name"] + "_detect_up"

    if not os.path.exists(folder):
        os.mkdir(folder)

    b1 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    b2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    e1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    e2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    round_i = 7
    cd["record_file"] = folder + "////" + cd["cipher_name"] + "_record_mode{}.txt".format(cd["mode"])

    cd["solve_file"] = folder + "////" + cd["cipher_name"] + "_round{}.stp".format(round_i)
    possible_value = []
    for ss in range(0, 8):
        cd["value"] = [0, 0, 0]

        cd["value"][0] = ss & 0x1
        cd["value"][1] = (ss >> 1) & 0x1
        cd["value"][2] = (ss >> 2) & 0x1

        cd["b1"] = copy.deepcopy(b1)
        cd["b2"] = copy.deepcopy(b2)
        cd["e1"] = copy.deepcopy(e1)
        cd["e2"] = copy.deepcopy(e2)
        mode = [cd["mode"], [0, round_i]]
        t11 = time.time()
        PRINTcipher96_model_3way_detect1.model_build(cd, mode)
        flag = PRINTcipher96_model_3way_detect1.solver(cd["solve_file"])
        t22 = time.time()
        print(t22 - t11)
        if not flag:
            possible_value.append(ss)
    f = open(cd["record_file"], "w")
    f.write("contradiction_position is {}.\n".format(str(possible_value)))
    f.close()

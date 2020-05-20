#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import Gift64_model_detect
import time
import os
import random

if __name__ == "__main__":

    cd = dict()

    cd["cipher_name"] = "gift"

    cd["mul"] = 3

    cd["cipher_size"] = 64
    cd["sbox_size"] = 4
    cd["sbox_num"] = 16

    cd["mode"] = 1

    folder = cd["cipher_name"] + "_detect"

    if not os.path.exists(folder):
        os.mkdir(folder)

    b1 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    b2 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    e1 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    e2 = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    round_i = 7
    cd["record_file"] = folder + "////" + cd["cipher_name"] + "_record_mode{}.txt".format(cd["mode"])
    ttt1 = time.time()

    cd["solve_file"] = folder + "////" + cd["cipher_name"] + "_round{}.stp".format(round_i)

    contradiction_position = []
    for ss in range(0, 16):
        cd["release"] = [ss * 4 for j in range(0, 4)]
        cd["b1"] = copy.deepcopy(b1)
        cd["b2"] = copy.deepcopy(b2)
        cd["e1"] = copy.deepcopy(e1)
        cd["e2"] = copy.deepcopy(e2)
        mode = [cd["mode"], [0, round_i]]
        t11 = time.time()
        Gift64_model_detect.model_build(cd, mode)
        flag = Gift64_model_detect.solver(cd["solve_file"])
        t22 = time.time()
        print(t22 - t11)
        if not flag:
            contradiction_position.append(ss)
    f = open(cd["record_file"], "w")
    f.write("contradiction_position is {}.\n".format(str(contradiction_position)))
    f.close()


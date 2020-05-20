#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import PRINTcipher48_model_detect
import time
import os

if __name__ == "__main__":

    cd = dict()

    cd["cipher_name"] = "PrintCipher48_3way"

    cd["cipher_size"] = 48
    cd["sbox_size"] = 3
    cd["sbox_num"] = 16

    cd["mode"] = 1

    folder = cd["cipher_name"] + "detect"

    if not os.path.exists(folder):
        os.mkdir(folder)

    b1 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    b2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    e1 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    e2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    round_i = 6
    cd["record_file"] = folder + "////" + cd["cipher_name"] + "_record_mode{}.txt".format(cd["mode"])

    cd["solve_file"] = folder + "////" + cd["cipher_name"] + "_round{}.stp".format(round_i)
    contradiction_position = []
    for ss in range(0, 48):
        cd["release"] = [ss]
        cd["b1"] = copy.deepcopy(b1)
        cd["b2"] = copy.deepcopy(b2)
        cd["e1"] = copy.deepcopy(e1)
        cd["e2"] = copy.deepcopy(e2)
        mode = [cd["mode"], [0, round_i]]
        t11 = time.time()
        PRINTcipher48_model_detect.model_build(cd, mode)
        flag = PRINTcipher48_model_detect.solver(cd["solve_file"])
        t22 = time.time()
        print(t22 - t11)
        if not flag:
            contradiction_position.append(ss)
    f = open(cd["record_file"], "w")
    f.write("contradiction_position is {}.\n".format(str(contradiction_position)))
    f.close()

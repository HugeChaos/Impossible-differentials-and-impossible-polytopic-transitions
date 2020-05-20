#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy


rc = [0, 0, 0, 0, 0, 0, 0, 0]

RC = []

for rou in range(0, 7):
    RC.append(copy.deepcopy(rc))
    t = rc[7] ^ rc[6] ^ 1
    for i in range(0, 7):
        rc[7 - i] = rc[6 - i]
    rc[0] = t
for rr in RC:
    print(str(rr) + ",\\")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from orth import Orth, OrthTree
from itertools import combinations


def test_lookup(IOrth):
    x_max = 100
    x_step = 3
    nums = range(1, x_max, x_step)
    nums_np = np.array(nums)
    orth = IOrth(nums)

    def check_ij(i, j):
        np_res = nums_np[(nums_np >= i) & (nums_np <= j)]
        my_res = np.array(orth.lookup(i, j))

        len_test = len(np_res) == len(my_res)
        eq_test = len_test and all(np_res == my_res)
        if not (len_test and eq_test):
            print("x: [{} {}]".format(i, j))
            print("Expected:")
            print(np_res)
            print("Got:")
            print(my_res)
        assert len_test, "len: {} vs {}".format(len(np_res), len(my_res))
        assert eq_test
    for i in range(1, x_max-x_step):
        for j in range(i, x_max-x_step):
            check_ij(i, j)
        for j in range(0, i):
            check_ij(i, j)


def test_count(IOrth):
    x_max = 100
    x_step = 3
    nums = range(1, x_max, x_step)
    nums_np = np.array(nums)
    orth = IOrth(nums)

    def check_ij(i, j):
        np_res = len(nums_np[(nums_np >= i) & (nums_np <= j)])
        my_res = orth.count(i, j)
        #  my_res = orth.countn([[i,j]])

        eq_test = np_res == my_res
        if not eq_test:
            print("x: [{} {}]".format(i, j))
            print("Expected:")
            print(np_res)
            print("Got:")
            print(my_res)
        assert eq_test
    for i in range(1, x_max-x_step):
        for j in range(i, x_max-x_step):
            check_ij(i, j)
        for i2 in range(0, i):
            check_ij(i2, j)


def test_countn(IOrth, n):
    x_max = 100
    x_step = 3
    nums = np.vstack([np.arange(1, x_max, x_step)+x_max*i for i in range(n)])
    nums = nums.transpose()
    # nums_np = np.array(nums)
    orth = IOrth(nums)

    def npc2(M):
        ms = [
            (nums[
                :,
                i] >= M[i][0]) & (
                nums[
                    :,
                    i] <= M[i][1]) for i in range(
                len(M))]
        m = np.bitwise_and.reduce(ms)
        #  print(nums[m])
        return sum(m)
    # m = 12
    #  print(npc2(2*100,20*100,2,m))
    #  print(orth.count2(2*100,20*100,2,m))
    # combos = list(combinations(np.arange(0,x_max,4),2))
    combos = [[0, 100], [50+100, 100+100], [20+200, 60+200], [355, 357]]

    # import pdb; pdb.set_trace()
    comboss = combinations(combos, n)
    # import pdb; pdb.set_trace()
    # import pdb; pdb.set_trace()
    #  comboss.append([[0,10],[2,1000]])
    ress = []

    for M in comboss:
        # res = orth.count2(x1,x2,y1,y2)
        # print(["{} <= xn <= {}".format(m[0],m[1]) for m in M])
        expected = npc2(M)
        #  print(expected)
        res = orth.countn(M)
        ress.append((res, expected))
        if res != expected:
            print("M:")
            print(["{} <= xn <= {}".format(m[0], m[1]) for m in M])
            print("{} vs {}".format(res, expected))
        assert res == expected


def test_succ(IOrth):
    nums = range(1, 67, 3)
    for i in range(1, 64):
        successor_i = IOrth.successor(nums, i)
        successor = nums[successor_i]
        previous = nums[successor_i-1]
        if successor_i == 0:
            continue
        assert previous < successor, "{} vs {} [i={}]".format(
            previous, successor, successor_i)
    succ_pre = IOrth.successor(nums, min(nums)-1)
    assert succ_pre == 0, "actual: {}".format(succ_pre)

    succ_err = IOrth.successor(nums, max(nums)+1)
    assert succ_err is None, "actual: {}".format(succ_err)


def test_pred(IOrth):
    nums = range(1, 67, 3)
    for i in range(1, 64):
        predecessor_i = IOrth.predecessor(nums, i)
        predecessor = nums[predecessor_i]
        successor = nums[predecessor_i+1]
        assert predecessor < successor, "{} vs {} [i={}]".format(
            predecessor, successor, i)
    pred_err = IOrth.predecessor(nums, min(nums)-1)
    assert pred_err is None, "actual: {}".format(pred_err)
    pred_post = IOrth.predecessor(nums, max(nums)+1)
    assert pred_post == len(nums)-1, "actual: {}".format(pred_post)


def main():
    test_succ(Orth)
    test_pred(Orth)
    test_lookup(Orth)
    test_lookup(OrthTree)
    test_count(Orth)
    test_count(OrthTree)
    test_countn(OrthTree, 1)
    test_countn(OrthTree, 2)
    test_countn(OrthTree, 3)
    test_countn(OrthTree, 4)

if __name__ == "__main__":
    main()

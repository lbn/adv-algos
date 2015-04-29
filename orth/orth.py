

class Orth(object):
    """docstring for Orth"""
    def __init__(self, arr):
        self.arr = arr

    def lookup(self,x1,x2):
        """
        Lookup using the walking method
        
        Takes O(log(n) + k)
        1) binary search to find successor
        2) walk k (matches found) steps
        """
        i = Orth.successor(self.arr,x1)
        while i < len(self.arr) and self.arr[i] <= x2:
            yield self.arr[i]
            i += 1

    @staticmethod
    def successor(nums,x):
        if x > max(nums):
            return None
        def successor_to(s,e):
            mid = (s+e)/2
            #print(nums[s:mid],nums[mid],nums[mid+1:e])
            if nums[mid] == x:
                return mid
            elif nums[mid] > x:
                if nums[mid-1] < x:
                    return mid
                return successor_to(s,mid)
            elif nums[mid] < x:
                return successor_to(mid+1,e)
        return successor_to(0,len(nums))

def test_succ():
    nums = range(1,67,3)
    for i in range(1,64):
        successor_i = Orth.successor(nums,i)
        successor = nums[successor_i]
        previous = nums[successor_i-1]
        if successor_i == 0:
            continue
        assert previous < successor, "{} vs {} [i={}]".format(previous,successor,successor_i)

class OrthTree(object):
    """docstring for OrthTree"""
    def __init__(self, arr):
        self.tree = Tree(arr)

    class Tree(object):
        """docstring for Tree"""
        def __init__(self, arr):
            self.arg = arg
            

        
        

import numpy as np
def test_lookup():
    x_max = 100
    x_step = 3
    nums = range(1,x_max,x_step)
    nums_np = np.array(nums)
    orth = Orth(nums)
    def check_ij(i,j):
        np_res = nums_np[(nums_np >= i) & (nums_np <= j)]
        my_res = list(orth.lookup(i,j))
        if not all(np_res == my_res):
            print(np_res)
            print(my_res)
        assert all(np_res == my_res), "x: [{} {}]".format(i,j)
    for i in range(1,x_max-x_step):
        for j in range(i,x_max-x_step):
            check_ij(i,j)
        for j in range(0,i):
            check_ij(i,j)

test_succ()
test_lookup()

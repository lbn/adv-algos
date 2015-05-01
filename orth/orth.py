

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
        nums = []
        while i < len(self.arr) and self.arr[i] <= x2:
            nums.append(self.arr[i])
            i += 1
        return nums

    @staticmethod
    def successor(nums,x):
        if x > max(nums):
            return None
        def successor_to(s,e):
            mid = int((s+e)/2)
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
    """
    Lookup using the balanced tree 
    
    Takes O(log(n) + k)
    1) find successor and predecessor nodes
    2) save the path for both and find the split node
    3) for each node on the path the offpath subtree is all or nothing
    """
    def lookup(self,x1,x2):
        print((x1,x2))
        def find_split(t1,t2):
            return max(set(t1.path())&set(t2.path()),key=lambda t:t.depth)

        def find_offpath(parent,child):
            if parent.right is child:
                return parent.left
            elif parent.left is child:
                return parent.right
            else:
                return None

        def filter_offpath(split,tree,f):
            if tree is split:
                return []
            nums = []
            if tree.left is not None and f(tree.left.this):
                for n in tree.left.to_list():
                    nums.append(n)
            if tree.right is not None and f(tree.right.this):
                for n in tree.right.to_list():
                    nums.append(n)
            off = None
            while True:
                if f(tree.this):
                    nums.append(tree.this)
                if off is not None and f(off.this):
                    for n in off.to_list():
                        nums.append(n)
                tree_old = tree
                tree = tree.parent    
                if tree is split:
                    break
                off = find_offpath(tree,tree_old)
            return nums
        x1s, x2p = OrthTree.successor(self.tree,x1),OrthTree.predecessor(self.tree,x2)
        print(list(x1s.path()))
        print(list(x2p.path()))
        split = find_split(x1s,x2p) 
        #print(split)

        nums = filter_offpath(split,x1s,lambda n: n>=x1)+[split.this]+filter_offpath(split,x2p,lambda n: n<=x2)
        print(nums)
        return nums

    @staticmethod
    def successor(tree,x):
        if tree.this == x:
            return tree

        if tree.this > x:
            if tree.left is None:
                return tree
            else:
                left_s = OrthTree.successor(tree.left,x)
                if left_s.this < x:
                    return tree
                else:
                    return left_s
        if tree.this < x:
            if tree.right is None:
                return tree
            else:
                return OrthTree.successor(tree.right,x)
    @staticmethod
    def predecessor(tree,x):
        if tree.this == x:
            return tree

        if tree.this > x:
            if tree.left is None:
                return tree
            else:
                left_s = OrthTree.predecessor(tree.left,x)
                return left_s
        if tree.this < x:
            if tree.right is None:
                return tree
            else:
                right_s = OrthTree.predecessor(tree.right,x)
                if right_s.this > x:
                    return tree
                else:
                    return right_s


class Tree(object):
    """docstring for Tree"""
    def __init__(self, arr,parent=None):
        self.parent = parent
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth+1

        mid_i = int(len(arr)/2)
        self.this = arr[mid_i]
        if mid_i > 0:
            self.left = Tree(arr[:mid_i],parent=self)
        else:
            self.left = None
        if mid_i+1 < len(arr):
            self.right = Tree(arr[mid_i+1:],parent=self)
        else:
            self.right = None
    def path(self):
        node = self
        while node is not None:
            yield node
            node = node.parent
    def to_list(self):
        tr = []
        if self.left is not None:
            for e in self.left.to_list():
                tr.append(e)

        tr.append(self.this)

        if self.right is not None:
            for e in self.right.to_list():
                tr.append(e)
        return tr

    def __repr__(self):
        leftc = "/" if self.left is not None else " "
        rightc = "\\" if self.right is not None else " "
        return "Tree[{}]({}:{}:{})".format(self.depth,leftc,self.this,rightc)


            

        
        

import numpy as np
def test_lookup(IOrth):
    x_max = 100
    x_step = 3
    nums = range(1,x_max,x_step)
    nums_np = np.array(nums)
    orth = IOrth(nums)
    def check_ij(i,j):
        np_res = nums_np[(nums_np >= i) & (nums_np <= j)]
        my_res = np.array(orth.lookup(i,j))

        len_test = len(np_res) == len(my_res)
        eq_test = len_test and all(np_res == my_res)
        if not (len_test and eq_test):
            print("x: [{} {}]".format(i,j))
            print("Expected:")
            print(np_res)
            print("Got:")
            print(my_res)
        assert len_test, "len: {} vs {}".format(len(np_res),len(my_res))
        assert eq_test
    for i in range(1,x_max-x_step):
        for j in range(i,x_max-x_step):
            check_ij(i,j)
        for j in range(0,i):
            check_ij(i,j)



test_succ()
test_lookup(Orth)
test_lookup(OrthTree)

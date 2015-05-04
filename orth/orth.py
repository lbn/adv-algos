

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
    def count(self,x1,x2):
        def get_tsum(split,tree,f):
            if tree is split:
                return 0
            #nums = []
            tsum = 0

            if tree.left is not None and f(tree.left.this):
                tsum += tree.left.ssum
            if tree.right is not None and f(tree.right.this):
                tsum += tree.right.ssum
            off = None
            while True:
                if f(tree.this):
                    tsum += 1
                if off is not None and f(off.this):
                    tsum += off.ssum
                tree_old = tree
                tree = tree.parent    
                if tree is split:
                    break
                off = OrthTree.find_offpath(tree,tree_old)
            return tsum
        f = lambda n: n>=x1 and n<=x2

        x1s, x2p = OrthTree.successor(self.tree,x1),OrthTree.predecessor(self.tree,x2)
        split = OrthTree.find_split(x1s,x2p) 

        ts = 0
        ts_x1 = get_tsum(split,x1s,f)
        ts_x2 = get_tsum(split,x2p,f)
        ts += ts_x1
        if f(split.this):
            ts += 1
        ts += ts_x2
        return ts
    def countn(self,M):
        def get_tsum(split,tree,f):
            if tree is split:
                return 0
            tsum = 0
            off = None
            while True:
                if f(tree):
                    tsum += 1
                if off is not None and f(off,1):
                    if len(M) == 1:
                        tsum += off.ssum
                    else:
                        tsum += off.thist.countn(M[1:])
                tree_old = tree
                tree = tree.parent    
                if tree is split:
                    break
                off = OrthTree.find_offpath(tree,tree_old)
            return tsum
        x1, x2 = M[0]

        def f(t,n=None):
            if n is None:
                n = len(M)
            a = all([p >= m[0] and p <= m[1] for p,m in zip(t.thisp,M[:n])])
            return a

        x1s, x2p = OrthTree.successor(self.tree,x1),OrthTree.predecessor(self.tree,x2)
        split = OrthTree.find_split(x1s,x2p) 
        if x1s is x2p:
            if x1s.this >= x1 and x1s.this <= x2:
                if len(M) > 1:
                    return self.tree.thist.countn(M[1:])
                else:
                    return 1
            else:
                return 0

        ts = 0
        ts_x1 = get_tsum(split,x1s,f)
        ts_x2 = get_tsum(split,x2p,f)
        ts += ts_x1
        # f(split) - testing if the actual split point matches
        if f(split):
            ts += 1
        ts += ts_x2
        return ts


    def count2(self,x1,x2,y1,y2):
        def get_tsum(split,tree,f):
            if tree is split:
                return 0
            #nums = []
            tsum = 0

            if tree.left is not None and f(tree.left):
                tsum += tree.left.thist.count(y1,y2)
                #tsum += tree.left.ssum
            if tree.right is not None and f(tree.right):
                tsum += tree.right.thist.count(y1,y2)
                #tsum += tree.right.ssum
            off = None
            while True:
                if f(tree):
                    tsum += 1#tree.thist.count(y1,y2)
                if off is not None and f(off):
                    tsum += off.thist.count(y1,y2)
                    #tsum += off.ssum
                tree_old = tree
                tree = tree.parent    
                if tree is split:
                    break
                off = OrthTree.find_offpath(tree,tree_old)
            return tsum
        f = lambda t: t.this>=x1 and t.this<=x2 and t.thisn[0] >= y1 and t.thisn[0] <= y2

        x1s, x2p = OrthTree.successor(self.tree,x1),OrthTree.predecessor(self.tree,x2)
        split = OrthTree.find_split(x1s,x2p) 

        ts = 0
        ts_x1 = get_tsum(split,x1s,f)
        ts_x2 = get_tsum(split,x2p,f)
        ts += ts_x1
        if f(split):
            ts += 1
            #ts += split.thist.count(y1,y2)
        ts += ts_x2
        return ts

    @staticmethod
    def find_split(t1,t2):
        return max(set(t1.path())&set(t2.path()),key=lambda t:t.depth)
    @staticmethod
    def find_offpath(parent,child):
        if parent.right is child:
            return parent.left
        elif parent.left is child:
            return parent.right
        else:
            return None

    """
    Lookup using the balanced tree 
    
    Takes O(log(n) + k)
    1) find successor and predecessor nodes
    2) save the path for both and find the split node
    3) for each node on the path the offpath subtree is all or nothing
    """
    def lookup(self,x1,x2):
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
                off = OrthTree.find_offpath(tree,tree_old)
            return nums
        x1s, x2p = OrthTree.successor(self.tree,x1),OrthTree.predecessor(self.tree,x2)
        split = OrthTree.find_split(x1s,x2p) 

        f = lambda n: n>=x1 and n<=x2
        nums = filter_offpath(split,x1s,f)
        if f(split.this):
            nums = nums+[split.this]
        nums = nums+filter_offpath(split,x2p,f)
        
        # workaround
        #return nums
        return sorted(nums)

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
        if type(arr) is not np.ndarray:
            arr = np.array(arr)
        if arr.ndim == 1:
            arr = arr.reshape((len(arr),1))
        self.parent = parent
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth+1

        mid_i = int(len(arr)/2)
        self.this = arr[mid_i][0]
        self.thisp = arr[mid_i]

        self.thisn = arr[mid_i][1:]
        self.dim = len(arr[mid_i])
        self.thisn = self.thisn.reshape((1,self.dim-1))
        if mid_i > 0:
            self.left = Tree(arr[:mid_i,:],parent=self)
            self.thisn = np.vstack([self.thisn,self.left.thisn])
        else:
            self.left = None

        if mid_i+1 < len(arr):
            self.right = Tree(arr[mid_i+1:,:],parent=self)
            self.thisn = np.vstack([self.thisn,self.right.thisn])
        else:
            self.right = None

        if self.dim > 1:
            self.thist = OrthTree(self.thisn)

        self.ssum = 1#self.this
        if self.left is not None:
            self.ssum += self.left.ssum
        if self.right is not None:
            self.ssum += self.right.ssum
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
        return "Tree[depth={depth},sum={sum},dim={dim}]({}:{}:{})".format(leftc,self.this,rightc,depth=self.depth,sum=self.ssum,dim=self.dim)


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


def test_count(IOrth):
    x_max = 100
    x_step = 3
    nums = range(1,x_max,x_step)
    nums_np = np.array(nums)
    orth = IOrth(nums)
    def check_ij(i,j):
        np_res = len(nums_np[(nums_np >= i) & (nums_np <= j)])
        my_res = orth.count(i,j)

        eq_test = np_res == my_res
        if not eq_test:
            print("x: [{} {}]".format(i,j))
            print("Expected:")
            print(np_res)
            print("Got:")
            print(my_res)
        assert eq_test
    for i in range(1,x_max-x_step):
        for j in range(i,x_max-x_step):
            check_ij(i,j)
        for i2 in range(0,i):
            check_ij(i2,j)


from itertools import combinations
def test_countn(IOrth,n):
    x_max = 100
    x_step = 3
    nums = np.vstack([np.arange(1,x_max,x_step)+x_max*i for i in range(n)])
    nums = nums.transpose()
    #nums_np = np.array(nums)
    orth = IOrth(nums)
    def npc2(M):
        ms = [(nums[:,i] >= M[i][0]) & (nums[:,i] <= M[i][1]) for i in range(len(M))]
        m = np.bitwise_and.reduce(ms)
        #print(nums[m])
        return sum(m)
    m = 12
    #print(npc2(2*100,20*100,2,m))
    #print(orth.count2(2*100,20*100,2,m))
    #combos = list(combinations(np.arange(0,x_max,4),2))
    combos = [[0,100],[50+100,100+100],[20+200,60+200],[355,357]]

    #import pdb; pdb.set_trace()
    comboss = combinations(combos,n)
    #import pdb; pdb.set_trace()
    #import pdb; pdb.set_trace()
    #comboss.append([[0,10],[2,1000]])
    ress = []

    for M in comboss:
        #res = orth.count2(x1,x2,y1,y2)
        #print(["{} <= xn <= {}".format(m[0],m[1]) for m in M])
        expected = npc2(M)
        #print(expected)
        res = orth.countn(M)
        ress.append((res,expected))
        if res != expected:
            print("M:")
            print(["{} <= xn <= {}".format(m[0],m[1]) for m in M])
            print("{} vs {}".format(res,expected))
        assert res == expected
    print(ress)
    #import pdb; pdb.set_trace()

    #for x1,x2 in combos:
        #for y1,y2 in combos2:

#test_succ()
#test_lookup(Orth)
#test_lookup(OrthTree)
#test_count(OrthTree)
#test_count2(OrthTree)
test_countn(OrthTree,2)
test_countn(OrthTree,3)
test_countn(OrthTree,4)



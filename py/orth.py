import numpy as np
import operator


class Orth(object):

    """1D array orthogonal range structure"""

    def __init__(self, arr, is_sorted=False):
        if is_sorted:
            self.arr = arr
        else:
            self.arr = sorted(arr)

    """
    Lookup using the walking method

    Takes O(log(n) + k)
    1) binary search to find successor
    2) walk k (matches found) steps
    """

    def lookup(self, x1, x2):
        i = Orth.successor(self.arr, x1)
        nums = []
        while i < len(self.arr) and self.arr[i] <= x2:
            nums.append(self.arr[i])
            i += 1
        return nums

    def count(self, x1, x2):
        x1i = Orth.successor(self.arr, x1)
        x2i = Orth.predecessor(self.arr, x2)
        if x1i is None or x2i is None:
            return 0
        return x2i-x1i+1

    def countn(self, M):
        if len(M) == 1:
            return self.count(*M[0])
        else:
            raise ValueError("1D Orth count can only operate on 1x2 M")

    @staticmethod
    def successor(nums, x):
        if x > max(nums):
            return None

        def successor_to(s, e):
            if e == s == 0:
                if nums[s] < x:
                    return None
                else:
                    return s

            mid = int((s+e)/2)
            if nums[mid] == x:
                return mid
            elif nums[mid] > x:
                if nums[mid-1] < x:
                    return mid
                return successor_to(s, mid)
            elif nums[mid] < x:
                return successor_to(mid+1, e)
        return successor_to(0, len(nums))

    @staticmethod
    def predecessor(nums, x):
        def predecessor_to(s, e):
            if e == s == 0:
                return None

            mid = int((s+e)/2)
            if nums[mid] == x:
                return mid
            elif nums[mid] > x:
                return predecessor_to(s, mid)
            elif nums[mid] < x:
                if mid+1 >= len(nums):
                    return len(nums)-1
                if nums[mid+1] > x:
                    return mid
                return predecessor_to(mid+1, e)
        return predecessor_to(0, len(nums))


class OrthTree(object):

    """d-dimensional orthogonal range structure"""

    def __init__(self, arr):
        self.tree = Tree(arr)

    def count(self, x1, x2):
        def get_tsum(split, tree, f):
            if tree is split:
                return 0
            # nums = []
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
                off = OrthTree.find_offpath(tree, tree_old)
            return tsum

        def f(n):
            return n >= x1 and n <= x2

        x1s, x2p = OrthTree.successor(
            self.tree, x1), OrthTree.predecessor(
            self.tree, x2)
        split = OrthTree.find_split(x1s, x2p)
        if x1s is x2p:
            if f(x1s.this) and f(x2p.this):
                return 1
            else:
                return 0

        ts = 0
        ts_x1 = get_tsum(split, x1s, f)
        ts_x2 = get_tsum(split, x2p, f)
        ts += ts_x1
        if f(split.this):
            ts += 1
        ts += ts_x2
        return ts

    def countn(self, M):
        def get_tsum(split, tree, f):
            if tree is split:
                return 0
            tsum = 0
            if len(M) == 1:
                if tree.left is not None and f(tree.left):
                    tsum += tree.left.ssum
                if tree.right is not None and f(tree.right):
                    tsum += tree.right.ssum
            off = None
            while True:
                if f(tree):
                    tsum += 1
                if off is not None and f(off, 1):
                    if len(M) == 1:
                        tsum += off.ssum
                    else:
                        tsum += off.thist.countn(M[1:])
                tree_old = tree
                tree = tree.parent
                if tree is split:
                    break
                off = OrthTree.find_offpath(tree, tree_old)
            return tsum
        x1, x2 = M[0]

        def f(t, n=None):
            if n is None:
                n = len(M)
            a = all([p >= m[0] and p <= m[1] for p, m in zip(t.thisp, M[:n])])
            return a

        x1s, x2p = OrthTree.successor(
            self.tree, x1), OrthTree.predecessor(
            self.tree, x2)
        split = OrthTree.find_split(x1s, x2p)
        if x1s is x2p:
            if f(x1s, n=1) and f(x2p, n=1):
                if len(M) > 1:
                    return self.tree.thist.countn(M[1:])
                else:
                    return 1
            else:
                return 0

        ts = 0
        ts_x1 = get_tsum(split, x1s, f)
        ts_x2 = get_tsum(split, x2p, f)
        ts += ts_x1
        # f(split) - testing if the actual split point matches
        if f(split):
            ts += 1
        ts += ts_x2
        return ts

    def count2(self, x1, x2, y1, y2):
        def get_tsum(split, tree, f):
            if tree is split:
                return 0
            tsum = 0
            off = None
            while True:
                if f(tree):
                    tsum += 1
                if off is not None and f(off, n=1):
                    tsum += off.thist.count(y1, y2)
                tree_old = tree
                tree = tree.parent
                if tree is split:
                    break
                off = OrthTree.find_offpath(tree, tree_old)
            return tsum

        def f(t, n=None):
            M = [(x1, x2), (y1, y2)]
            if n is None:
                n = len(M)
            a = all([p >= m[0] and p <= m[1] for p, m in zip(t.thisp, M[:n])])
            return a

        x1s, x2p = OrthTree.successor(
            self.tree, x1), OrthTree.predecessor(
            self.tree, x2)
        split = OrthTree.find_split(x1s, x2p)

        if x1s is x2p:
            if f(x1s, n=1) and f(x2p, n=1):
                return self.tree.thist.count(y1, y2)
            else:
                return 0
        ts = 0
        ts_x1 = get_tsum(split, x1s, f)
        ts_x2 = get_tsum(split, x2p, f)
        ts += ts_x1
        if f(split):
            ts += 1
        ts += ts_x2
        return ts

    @staticmethod
    def find_split(t1, t2):
        return max(set(t1.path()) & set(t2.path()), key=lambda t: t.depth)

    @staticmethod
    def find_offpath(parent, child):
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

    def lookup(self, x1, x2):
        def filter_offpath(split, tree, f):
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
                off = OrthTree.find_offpath(tree, tree_old)
            return nums
        x1s, x2p = OrthTree.successor(
            self.tree, x1), OrthTree.predecessor(
            self.tree, x2)
        split = OrthTree.find_split(x1s, x2p)

        def f(n):
            return n >= x1 and n <= x2
        nums = filter_offpath(split, x1s, f)
        if f(split.this):
            nums = nums+[split.this]
        nums = nums+filter_offpath(split, x2p, f)

        # workaround
        # return nums
        return sorted(nums)

    @staticmethod
    def successor(tree, x):
        if tree.this == x:
            return tree

        if tree.this > x:
            if tree.left is None:
                return tree
            else:
                left_s = OrthTree.successor(tree.left, x)
                if left_s.this < x:
                    return tree
                else:
                    return left_s
        if tree.this < x:
            if tree.right is None:
                return tree
            else:
                return OrthTree.successor(tree.right, x)

    @staticmethod
    def predecessor(tree, x):
        if tree.this == x:
            return tree

        if tree.this > x:
            if tree.left is None:
                return tree
            else:
                left_s = OrthTree.predecessor(tree.left, x)
                return left_s
        if tree.this < x:
            if tree.right is None:
                return tree
            else:
                right_s = OrthTree.predecessor(tree.right, x)
                if right_s.this > x:
                    return tree
                else:
                    return right_s


class Tree(object):

    """Tree for the d-dimensional orthogonal range structure"""

    def __init__(self, arr, parent=None):
        if not isinstance(arr, np.ndarray):
            arr = np.array(arr)
        if arr.ndim == 1:
            arr = arr.reshape((len(arr), 1))
        self.parent = parent
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth+1

        mid_i = int(len(arr)/2)
        self.this = arr[mid_i][0]
        self.thisp = arr[mid_i]

        # self.thisn = arr[mid_i][1:]
        self.dim = len(arr[mid_i])
        # self.thisn = self.thisn.reshape((1,self.dim-1))
        self.thisn = []

        # assign left and right if they exist
        if mid_i > 0:
            self.left = Tree(arr[:mid_i, :], parent=self)
        else:
            self.left = None

        if mid_i+1 < len(arr):
            self.right = Tree(arr[mid_i+1:, :], parent=self)
        else:
            self.right = None

        self.ssum = 1

        # store number of items and nx(d-1) tree
        if self.left is not None:
            self.ssum += self.left.ssum
            for point in self.left.thisn:
                self.thisn.append(point)
            self.left.thisn = None

        self.thisn.append(list(self.thisp[1:]))

        if self.right is not None:
            self.ssum += self.right.ssum
            for point in self.right.thisn:
                self.thisn.append(point)
            self.right.thisn = None

        if self.dim > 1:
            self.thisn = sorted(self.thisn, key=operator.itemgetter(0))

        if self.dim == 2:
            nnums = [p[0] for p in self.thisn]
            self.thist = Orth(nnums, is_sorted=True)
        elif self.dim >= 3:
            self.thist = OrthTree(self.thisn)

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
        return "Tree[depth={depth},sum={sum},dim={dim}]({}:{}:{})".format(
            leftc,
            self.this,
            rightc,
            depth=self.depth,
            sum=self.ssum,
            dim=self.dim)

import logging as log
import numpy as np

log.basicConfig(level=log.DEBUG)


class NaiveLCP(object):

    """Fake O(n) preprocessing and space complexity"""

    def __init__(self, T, P):
        self.T = T
        self.P = P

    def get(self, i, j):
        """Fake O(1) query"""
        matches = 0
        while i < len(self.T) and j < len(self.P):
            if self.T[i] == self.P[j]:
                matches += 1
                i += 1
                j += 1
            else:
                break
        return matches

from collections import Counter

class KSpread(object):

    """docstring for KSpread"""

    def __init__(self, T, P, k):
        self.T = T
        self.P = P
        self.k = k
        log.debug("n = {}".format(len(self.T)))
        log.debug("m = {}".format(len(self.P)))
        self.lcp = NaiveLCP(self.T, self.P)

        freqs = self.get_frequent()
        fs = 0
        for c in self.P:
            if c in freqs:
                fs += 1
            log.debug(c + " - " + ("F" if c in freqs else "NF"))
        log.debug("F: {} | NF: {}".format(fs,len(self.P) - fs))
        log.debug("sqrt(m) = {}".format(np.sqrt(len(self.P))))

    def get_frequent(self):
        """docstring for get_frequent"""
        return [c for c, n in Counter(self.P).items() if n >= np.sqrt(len(self.P))]



    def distances(self):
        Dn = len(self.T) - len(self.P) + 1
        D = np.zeros(Dn)
        # O(n) times
        for i in range(Dn):
            D[i] = self.d(i)
        D[D > self.k] = None
        return D

    def d(self, i):
        it = i
        j = 0
        j_last = None
        cost = 0
        # O(k + 1) -> O(k) times
        while j < len(self.P) and i < len(self.T):
            # O(1)
            jp = self.lcp.get(i, j)
            i += jp
            j += jp
            if j >= len(self.P):
                break

            if j_last is None:
                cost += 1
                log.debug("(i={},j={})\t cost += 1".format(it, j))
            else:
                costp = len(self.P)/float(j - j_last)
                log.debug("(i={},j={})\t cost += {}/({} - {})\t (+{})"
                          .format(it, j, len(self.P), j, j_last, costp))
                cost += costp
                if cost > self.k:
                    break
            j_last = j
            i += 1
            j += 1
        return cost


def main():
    """docstring for main"""

    test1 = ["bananabanna", "baaa"]
    #test1 = ["abcbababcababa", "bcbcaabaaba"]
    #ks = KSpread(test1[0], test1[1], k=(len(test1[1])-1)**2)
    ks = KSpread(test1[0], test1[1], k=len(test1[1]))
    print(ks.distances())


if __name__ == '__main__':
    main()

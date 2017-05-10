from banks.database.graph import Graph
from banks.algorithm.djisktra import BANKSIterator
import time


class GenericBANKS:

    def __init__(self):
        self.graph = Graph()

    def createSearchIterator(self, keywords):
        keywordNodes = dict()
        for kw in keywords:
            keywordNodes[kw] = self.graph.getKeywordNodes(kw)
            if len(keywordNodes[kw]) == 0:
                keywordNodes.pop(kw, None)
        return BANKSIterator(self.graph, keywordNodes)

    def search(self, keywords, maxResult=30, maxTime=30, strictDiff=False):
        print "Start: ", time.strftime('%H:%M:%S %Y/%m/%d', time.localtime())

        start = time.time()

        banksIt = self.createSearchIterator(keywords)
        banksIt.setStrict(strictDiff)

        while time.time() - start < maxTime and banksIt.next() and banksIt.getNbTrees() <= maxResult:
            banksIt.findRoots()
            banksIt.constructTrees()

        print "End: ", time.strftime('%H:%M:%S %Y/%m/%d'), "\n"
        return map(lambda t: t.getEgdeIDs(), banksIt.getTrees())


if __name__ == '__main__':
    banks = GenericBANKS()
    trees = banks.search(["Busta Rhymes", "Cube Zero", "273", "76U87JFUTVUYJBGIVF"], 10, strictDiff=True)
    for tree in trees:
        print tree


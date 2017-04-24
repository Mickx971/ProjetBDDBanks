from banks.neo4j.graph import Graph
from banks.algorithm.djisktra import BANKSIterator


class GenericBANKS:

    def __init__(self):
        self.graph = Graph()

    def createSearchIterator(self, keywords):
        keywordNodes = dict()
        for kw in keywords:
            keywordNodes[kw] = self.graph.getKeywordNodes(kw)
        return BANKSIterator(self.graph, keywordNodes)

    def search(self, keywords, nbResult):
        banksIt = self.createSearchIterator(keywords)
        while banksIt.next() and banksIt.getNbTrees() <= nbResult:
            banksIt.findRoots()
            banksIt.constructTrees()
        return banksIt.getTrees()

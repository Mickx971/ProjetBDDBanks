from banks.neo4j.graph import Graph
from banks.algorithm.djisktra import DjisktraIterator


class GenericBANKS:

    def __init__(self):
        self.graph = Graph()

    def createSearchIterator(self, keywords):
        keywordNodes = dict()
        for kw in keywords:
            keywordNodes[kw] = self.graph.getKeywordNodes(kw)
        return DjisktraIterator(self.graph, keywordNodes)

    def search(self, keywords, nbResult):
        djisk = self.createSearchIterator(keywords)
        while djisk.next() and djisk.getNbRoots() <= nbResult:
            djisk.findRoots()
            djisk.constructTrees()
        return djisk.getTrees()

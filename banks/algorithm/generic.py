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
        roots = set()
        while djisk.next() and len(roots) <= nbResult:
            roots.add(djisk.getRoots())
        return self.constructTrees(roots, keywords)

    def constructTrees(self, keywords):
        pass


if __name__ == '__main__':
    searchEngine = GenericBANKS()
    searchEngine.search(["1", "3", "4"], None)

from banks.neo4j.graph import Graph

class GenericBANKS:

    def __init__(self):
        self.graph = Graph()

    def search(self, keywords):
        keywordNodes = dict()
        for kw in keywords:
            keywordNodes[kw] = self.graph.getKeywordNodes(kw)


if __name__ == '__main__':
    searchEngine = GenericBANKS()
    searchEngine.search(["1", "3", "4"], None)

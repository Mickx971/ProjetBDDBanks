

class DjisktraIterator:

    def __init__(self, graph, keywordNodes):
        self.graph = graph
        self.keywordNodes = keywordNodes
        self.iterators = list()
        for kw in self.keywordNodes.keys():
            for initialNode in self.keywordNodes[kw]:
                self.iterators.append({"keyword": kw, "visited": {initialNode: 0}, "path": {}, "nodes": graph.getNodes()})

    def next(self, default=False):
        for kw in self.keywordNodes.keys():
            for node in self.keywordNodes[kw]:
                pass

        return default

    def nextDjisktra(self):
        pass

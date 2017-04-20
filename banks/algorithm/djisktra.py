

class DjisktraIterator:

    def __init__(self, graph, keywordNodes):
        self.graph = graph
        self.keywordNodes = keywordNodes
        self.iterators = list()
        self.roots = set()
        for kw in self.keywordNodes.keys():
            for initialNode in self.keywordNodes[kw]:
                self.iterators.append({"keyword": kw, "visited": {initialNode: 0}, "path": {}, "nodes": graph.getNodes()})

    def next(self, default=False):
        haveChanged = default
        for it in self.iterators:
            haveChanged = haveChanged or self.nextDjisktra(it)
        return haveChanged

    def nextDjisktra(self, djiskIt):
        nodes = djiskIt["nodes"]
        visited = djiskIt["visited"]
        path = djiskIt["path"]

        if len(nodes) == 0:
            return False

        minNode = None
        for node in nodes:
            if node in visited:
                if minNode is None:
                    minNode = node
                elif visited[node] < visited[minNode]:
                    minNode = node

        if minNode is None:
            return False

        nodes.remove(minNode)
        currentWeight = visited[minNode]

        edges = self.graph.getEdgesFrom(minNode)

        for edge in edges:
            weight = currentWeight + edge.getCost()
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = minNode

        return True

    def findRoots(self):
        roots = self.graph.getNodes()
        for it in self.iterators:
            roots = roots & set(it["visited"].keys())
        self.roots = roots
        return roots

    def getNbRoots(self):
        return len(self.roots)

    def constructTrees(self):
        pass

    def getTrees(self):
        pass

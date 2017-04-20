class DjisktraIterator:
    def __init__(self, graph, keywordNodes):
        self.graph = graph
        self.keywordNodes = keywordNodes
        self.iterators = list()
        self.roots = set()
        self.trees = dict()
        for kw in self.keywordNodes.keys():
            for initialNode in self.keywordNodes[kw]:
                self.iterators.append(
                    {"keyword": kw, "visited": {initialNode: 0}, "path": {}, "nodes": graph.getNodes()})

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
            weight = currentWeight + self.graph.getEdgeCost(edge)
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
        for root in self.roots:
            if root not in self.trees.keys():
                tree = {"root": root, "paths": {}, "weight": 0}
                self.trees[root] = tree
                for it in self.iterators:
                    if root in it["visited"]:
                        self.mergePaths(tree, it["path"].copy())

    def mergePaths(self, tree, path):
        currentNode = tree["root"]
        treePaths = tree["paths"]
        while len(path) != 0:
            nextNode = path.pop(currentNode)
            if currentNode not in treePaths.keys():
                treePaths[currentNode] = list()
            edge = self.graph.getEdge(currentNode, nextNode)
            tree["weight"] = tree["weight"] + self.graph.getEdgeCost(edge)
            treePaths[currentNode].append(nextNode)
            currentNode = nextNode

    def getTrees(self):
        return self.trees

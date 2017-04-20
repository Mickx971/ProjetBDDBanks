import sys

class DjisktraIterator:

    class InnerIterator:
        def __init__(self, keyword, initialNode, masterIterator):
            self.keyword = keyword
            self.initialNode = initialNode
            self.visited = {initialNode: 0}
            self.path = {}
            self.masterIterator = masterIterator

        def next(self):
            if len(self.visited) == self.masterIterator.nbTuples:
                return False

            minNode = None
            for node in self.visited:
                if minNode is None:
                    minNode = node
                elif self.visited[node] < self.visited[minNode]:
                    minNode = node

            currentWeight = self.visited[minNode]
            edges = self.masterIterator.graph.getEdgesFrom(minNode)

            for edge in edges:
                weight = currentWeight + self.masterIterator.graph.getEdgeCost(edge)
                if edge not in self.visited or weight < self.visited[edge]:
                    self.visited[edge] = weight
                    self.path[edge] = minNode

            return True

    class Tree:
        def __init__(self, root, leaves):
            self.root = root
            self.paths = {}
            self.weight = 0
            self.leaves = leaves

    def __init__(self, graph, keywordNodes):
        self.graph = graph
        self.keywordNodes = keywordNodes
        self.iterators = dict()
        self.roots = set()
        self.trees = list()
        self.nbTuples = graph.getNbTuples()
        for kw in self.keywordNodes.keys():
            for initialNode in self.keywordNodes[kw]:
                self.iterators[initialNode] = self.InnerIterator(kw, initialNode)

    def next(self, default=False):
        haveChanged = default
        for it in self.iterators.values():
            haveChanged = it.next() or haveChanged
        return haveChanged

    def findRoots(self):
        keywordPaths = dict()

        for kw in self.keywordNodes.keys():
            keywordPaths[kw] = set()
            for initialNode in self.keywordNodes[kw]:
                keywordPaths[kw].add(self.iterators[initialNode].path)

        roots = self.graph.getNodes()
        for paths in keywordPaths.values():
            roots = roots & paths

        self.roots = roots
        return roots

    def getNbRoots(self):
        return len(self.roots)

    def getKwIteratorsContainingNode(self, root):
        iterators = dict()
        for itKey in self.iterators.values():
            if root in self.iterators[itKey].path.values() or root == itKey:
                kw = self.iterators[itKey].keyword
                if iterators[kw] is None:
                    iterators[kw] = list()
                iterators[kw].append(self.iterators[itKey])
        return iterators

    def computeNbTrees(self, kwIterators):
        if len(kwIterators) == 0:
            return 0
        nbTrees = 1
        for kw in kwIterators.keys():
            nbTrees = nbTrees * len(kwIterators[kw])
        return nbTrees

    def getLeavesFromIterators(self, selectedIterators):
        leaves = set()
        for it in selectedIterators:
            leaves.add(it.keyword)
        return leaves

    def isNewTree(self, root, selectedIterators):
        leaves = self.getLeavesFromIterators(selectedIterators)
        for tree in self.trees:
            if tree.root == root and len(tree.leaves - leaves) == 0:
                return False
        return True

    def constructTrees(self):
        for root in self.roots:
            kwIterators = self.getKwIteratorsContainingNode(root)
            nbTrees = self.computeNbTrees(kwIterators)
            for i in range(0, nbTrees):
                selectedIterators = list()
                for kw in kwIterators.keys():
                    selectedIterators.append(kwIterators[kw][i % len(kwIterators[kw])])
                if self.isNewTree(root, selectedIterators):
                    tree = self.Tree(root, self.getLeavesFromIterators(selectedIterators))
                    self.trees.append(tree)
                    for it in selectedIterators:
                        self.mergePaths(tree, it.path.copy())

    def mergePaths(self, tree, path):
        currentNode = tree.root
        treePaths = tree.paths
        while len(path) != 0:
            nextNode = path.pop(currentNode)
            if currentNode not in treePaths.keys():
                treePaths[currentNode] = list()
            edge = self.graph.getEdge(currentNode, nextNode)
            tree.weight = tree.weight + self.graph.getEdgeCost(edge)
            treePaths[currentNode].append(nextNode)
            currentNode = nextNode

    def getTrees(self):
        return self.trees


def computeNbTrees(map):
    if len(map) == 0:
        return 0
    nb = 1
    for kw in map.keys():
        nb = nb * len(map[kw])
    return nb


if __name__ == '__main__':
    data = dict()
    data["l1"] = ['1', '2', '3']
    data["l2"] = ['4', '5']
    data["l3"] = ['6']
    data["l4"] = ['7', '8', '9', 'd']

    nbTrees = computeNbTrees(data)
    print nbTrees
    for i in range(0, nbTrees):
        selectedIterators = list()
        for kw in data.keys():
            selectedIterators.append(data[kw][i % len(data[kw])])
        for it in selectedIterators:
            sys.stdout.write(it)
        else:
            print


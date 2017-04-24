import sys


class BANKSIterator:

    class DjisktraIterator:
        def __init__(self, keyword, initialNode, nbTuples, graph):
            self.keyword = keyword
            self.initialNode = initialNode
            self.reached = {initialNode: 0}
            self.shortestPathsTree = {}
            self.nbTuples = nbTuples
            self.graph = graph
            self.traversed = set()

        def next(self):
            if len(self.reached) == self.nbTuples:
                return False

            minNode = None
            for node in self.reached:
                if node not in self.traversed:
                    if minNode is None:
                        minNode = node
                    elif self.reached[node] < self.reached[minNode]:
                        minNode = node

            self.traversed.add(minNode)

            currentWeight = self.reached[minNode]
            neighbours = self.graph.getNeighbours(minNode)

            for n in neighbours:
                edge = self.graph.getEdge(n, minNode)
                weight = currentWeight + self.graph.getEdgeCost(edge)
                if n not in self.reached or weight < self.reached[n]:
                    self.reached[n] = weight
                    self.shortestPathsTree[n] = minNode

            return True

    class Tree:
        def __init__(self, root, leaves):
            self.root = root
            self.paths = {}
            self.weight = 0
            self.leaves = leaves

    def __init__(self, graph, keywordNodes):
        self.keywordNodes = keywordNodes
        self.iterators = dict()
        self.roots = set()
        self.trees = list()
        nbTuples = graph.getNbTuples()
        for kw in self.keywordNodes.keys():
            for initialNode in self.keywordNodes[kw]:
                self.iterators[initialNode] = self.DjisktraIterator(kw, initialNode, nbTuples, graph)

    def next(self):
        haveChanged = False
        for it in self.iterators.values():
            haveChanged = it.next() or haveChanged
        return haveChanged

    def findRoots(self):
        keywordPaths = dict()

        for kw in self.keywordNodes.keys():
            keywordPaths[kw] = set()
            for initialNode in self.keywordNodes[kw]:
                keywordPaths[kw].add(self.iterators[initialNode].reached.keys())

        roots = keywordPaths.itervalues().next()
        for paths in keywordPaths.itervalues():
            roots = roots & paths

        self.roots = roots

    def getNbTrees(self):
        return len(self.trees)

    def getKwIteratorsContainingNode(self, root):
        iterators = dict()
        for it in self.iterators.iterkeys():
            if root in it.reached.keys():
                if iterators[it.keyword] is None:
                    iterators[it.keyword] = list()
                iterators[it.keyword].append(it)
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
            leaves.add(it.initialNode)
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
                        self.mergePaths(tree, it.shortestPathsTree, it.initialNode, it.reached)

    def mergePaths(self, tree, shortestPathsTree, keywordNode, shortestPathsWeight):
        currentNode = tree.root
        while currentNode != keywordNode:
            nextNode = shortestPathsTree[currentNode]
            tree.paths[nextNode] = nextNode
            currentNode = nextNode
        tree.weight = tree.weight + shortestPathsWeight[tree.root]

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


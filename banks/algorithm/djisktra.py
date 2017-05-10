import sys


class BANKSIterator:

    class Edge:
        def __init__(self, edgeId, fromNode, toNode):
            self.id = edgeId
            self.n1 = fromNode
            self.n2 = toNode

    class Tree:
        def __init__(self, root, leaves):
            self.root = root
            self.paths = {}
            self.weight = 0
            self.leaves = leaves
            self.edges = set()

        def addEdge(self, edge):
            self.edges.add(edge)

        def getEgdeIDs(self):
            return map(lambda edge: edge.id, self.edges)

        def printTree(self):
            print "Tree: "
            for leave in self.leaves:
                node = leave
                spaces = ""
                while node != self.root:
                    print spaces, node
                    node = self.paths[node]
                    spaces += "\t"
                    if node == self.root:
                        print spaces, node
                        break

        def keyToString(self, N):
            nodes = []
            for n in N:
                if isinstance(n, str):
                    nodes.append(n)
                else:
                    nodes.append(str(n))
            return nodes

        def getNodesToString(self):
            nodes = set(self.paths.keys())
            nodes.add(self.root)
            nodes = sorted(nodes)
            nodes = self.keyToString(nodes)
            return nodes

        def printSummary(self):
            leaves = self.keyToString(self.leaves)
            nodes = self.getNodesToString()
            print "Nodes:", " ".join(nodes)
            print "Leaves:", " ".join(leaves)
            print "Root: ", self.root

        def printEdges(self):
            for edge in self.edges:
                print edge.id, "from: ", edge.n1, " to: ", edge.n2

    class DjisktraIterator:
        def __init__(self, keyword, initialNode, nbTuples, graph):
            self.keyword = keyword
            self.initialNode = initialNode
            self.reached = {initialNode: 0}
            self.shortestPathsTree = {}
            self.nbTuples = nbTuples
            self.graph = graph
            self.edges = set()
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

            # Non connex Graph
            if minNode is None:
                return False

            self.traversed.add(minNode)

            currentWeight = self.reached[minNode]
            neighbours = self.graph.getNeighbours(minNode)

            for n in neighbours:
                edge = self.graph.getEdge(n, minNode)
                weight = currentWeight + self.graph.getEdgeCost(edge)
                if n not in self.reached or weight < self.reached[n]:
                    self.reached[n] = weight
                    self.shortestPathsTree[n] = minNode
                    self.edges.add(BANKSIterator.Edge(edge, n, minNode))

            return True

        def getEdge(self, fromNode, toNode):
            for edge in self.edges:
                if edge.n1 == fromNode and edge.n2 == toNode:
                    return edge
            return None


    def __init__(self, graph, keywordNodes, strictDiff=False):
        self.keywordNodes = keywordNodes
        self.iterators = dict()
        self.roots = set()
        self.trees = list()
        self.strictDiff = strictDiff
        nbTuples = graph.getNbTuples()
        for kw in self.keywordNodes.keys():
            for initialNode in self.keywordNodes[kw]:
                self.iterators[initialNode] = self.DjisktraIterator(kw, initialNode, nbTuples, graph)

    def setStrict(self, setStrict):
        self.strictDiff = setStrict

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
                keywordPaths[kw].update(self.iterators[initialNode].reached.keys())

        roots = keywordPaths.itervalues().next()
        for paths in keywordPaths.itervalues():
            roots = roots & paths

        self.roots = roots

    def getNbTrees(self):
        return len(self.trees)

    def getKwIteratorsContainingNode(self, root):
        iterators = dict()
        for it in self.iterators.itervalues():
            if root in it.reached.keys():
                if it.keyword not in iterators:
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

    def isStrictlyNewTree(self, tree):
        treeNodes = set(tree.paths.keys())
        treeNodes.add(tree.root)
        for t in self.trees:
            tNodes = set(t.paths.keys())
            tNodes.add(t.root)
            if len(tNodes - treeNodes) == 0 or len(treeNodes - tNodes) == 0:
                return False
        return True

    def isNewTree(self, t):
        for tree in self.trees:
            if tree.root == t.root and len(tree.leaves - t.leaves) == 0:
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
                tree = self.Tree(root, self.getLeavesFromIterators(selectedIterators))
                if self.isNewTree(tree):
                    for it in selectedIterators:
                        self.mergePaths(tree, it)
                    if self.strictDiff == False or self.isStrictlyNewTree(tree):
                        self.trees.append(tree)

    def mergePaths(self, tree, it):

        shortestPathsTree = it.shortestPathsTree
        keywordNode = it.initialNode
        shortestPathsWeight = it.reached
        currentNode = tree.root

        while currentNode != keywordNode:
            nextNode = shortestPathsTree[currentNode]
            tree.paths[nextNode] = currentNode
            tree.addEdge(it.getEdge(currentNode, nextNode))
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


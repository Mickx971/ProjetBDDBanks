from connector import Connector


class Graph:
    def __init__(self):
        self.db = Connector()
        self.db.connect()
        self.numberOfNodes = self.__getNumberOfNodes()

    def getNeighbours(self, node):
        session = self.db.getSession()
        temp = session.run("match(a)-[]->(b) where id(a) = {nodeId} return distinct id(b) as id", {"nodeId": node})
        neighbors = []
        for neighbor in temp:
            neighbors.append(neighbor["id"])
        return neighbors

    def getKeywordNodes(self, kw):
        session = self.db.getSession()
        result = session.run("match(a:__value__) where a.value = {value} return distinct id(a) as id", {"value": kw})
        for node in result:
            valueNode = node["id"]
        return self.getNeighbours(valueNode)

    def getNodes(self):
        if self.nodes is None:
            self.fetchNode()
        return set(self.nodes)

    def fetchNode(self):
        pass

    def getEdge(self, fromNode, toNode):
        session = self.db.getSession()
        result = session.run('''match(a)-[edge]->(b) where id(a) = {from} and id(b) = {to} 
        return id(edge) as id, edge.__weight__ as weight order by weight limit 1''',
                    {"from": fromNode, "to": toNode})
        for i in result:
            edge = i["id"]
        return edge

    def getEdgeCost(self, edge):
        session = self.db.getSession()
        result = session.run("match()-[edge]->() where id(edge) = {edgeId} return edge",
                             {"edgeId": edge})
        for i in result:
            cost = i["edge"]["__weight__"]
        return cost

    def __getNumberOfNodes(self):
        session = self.db.getSession()
        result = session.run("match(a) where not a:__value__  return count(a) as nodeCount")
        for i in result:
            numberOfNodes = i["nodeCount"]
        return numberOfNodes

    def getNbTuples(self):
        return self.numberOfNodes
if __name__ == "__main__":
    graph = Graph()
    print graph.getKeywordNodes("toufik")
    print graph.getNeighbours(50)
    print graph.getEdge(50,47)
    print graph.getEdgeCost(100)
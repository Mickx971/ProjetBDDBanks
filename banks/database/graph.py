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
        valueNode = []
        session = self.db.getSession()
        result = session.run("""match(a) where a:__value__ and lower({value}) in extract(v in split(lower(a.value), " ") | replace(replace(trim(v), ",", ""), ".","")) return id(a) as id order by length(a.value)""", {"value": kw})
        for node in result:
            valueNode.append(node["id"])

        keywordNodes = []
        for node in valueNode:
            keywordNodes.extend(self.getNeighbours(node))
        return keywordNodes


    def getEdge(self, fromNode, toNode):
        session = self.db.getSession()
        result = session.run('''match(a)-[edge]->(b) where id(a) = {from} and id(b) = {to} 
        return id(edge) as id, edge.__weight__ as weight order by weight limit 1''',
                    {"from": fromNode, "to": toNode})
        edge = None
        for i in result:
            edge = i["id"]
        return edge

    def getEdgeCost(self, edge):
        cost = None
        session = self.db.getSession()
        result = session.run("match()-[edge]->() where id(edge) = {edgeId} return edge",
                             {"edgeId": edge})
        for i in result:
            cost = i["edge"]["__weight__"]
        return cost

    def __getNumberOfNodes(self):
        session = self.db.getSession()
        result = session.run("match(a) where not a:__value__  return count(a) as nodeCount")
        numberOfNodes = None
        for i in result:
            numberOfNodes = i["nodeCount"]
        return numberOfNodes

    def getNbTuples(self):
        return self.numberOfNodes

    def getNodeById(self,id):
        session = self.db.getSession()
        results = session.run("""start n = Node({nodeId}) match (n)<-[edge]-(v) 
        where v:__value__ return type(edge) as key, v.value as value""", {"nodeId": id})
        node = {}
        for result in results:
            key = str(result["key"]) if isinstance(result["key"], int) else result["key"]
            node[key] = result["value"]
        return node

    def transformToClientStructure(self, listOfSolutions):
        transformedSolutions = []
        session = self.db.getSession()
        for solution in listOfSolutions:
            resutls = session.run("""start r = rel({solution}) match (a)-[r]->(b) 
            return id(a) as source,id(b) as target, id(r) as id, type(r) as type """,
                                  {"solution": solution})
            nodes = list()
            edges = list()
            for result in resutls:
                if not {"id": result["source"]} in nodes:
                    nodes.append({"id": result["source"]})

                if not {"id": result["target"]} in nodes:
                    nodes.append({"id": result["target"]})

                source = nodes.index({"id": result["source"]})
                target = nodes.index({"id": result["target"]})
                edges.append({"source": source , "target": target, "weight": 2, "name": result["type"]})

            transformedSolutions.append({"nodes": nodes, "links": edges})

        interessedFields = [ "value","title", "name"]
        for solution in transformedSolutions:
            for node in solution["nodes"]:
                n = self.getNodeById(node["id"])
                keys = n.keys()
                for interessedField in interessedFields:
                    if interessedField in keys:
                        node["name"] = n[interessedField]
                if "name" not in node.keys():
                    if len(keys) > 0:
                        node["name"] = n[n.keys()[0]]
                    else:
                        node["name"] = node["id"]



        return transformedSolutions



if __name__ == "__main__":
    graph = Graph()
    print graph.transformToClientStructure([[520437, 412699],[412250]])
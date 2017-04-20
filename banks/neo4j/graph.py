from banks.neo4j.connector import Connector


class Graph:
    def __init__(self):
        self.db = Connector()
        self.nodes = None

    def getKeywordNodes(self, kw):
        pass

    def getNodes(self):
        if self.nodes is None:
            self.fetchNode()
        return set(self.nodes)

    def fetchNode(self):
        pass

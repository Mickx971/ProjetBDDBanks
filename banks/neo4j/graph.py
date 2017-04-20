from banks.neo4j.connector import Connector


class Graph:
    def __init__(self):
        self.db = Connector()

    def getKeywordNodes(self, kw):
        pass
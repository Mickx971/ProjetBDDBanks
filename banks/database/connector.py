from neo4j.v1 import GraphDatabase, basic_auth


class Connector:

    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=basic_auth("neo4j", "password"))
        self.session = None

    def connect(self):
        self.session = self.driver.session()

    def disconnect(self):
        self.session.close()
        
    def getSession(self):
        return self.session

    def run(self, statement):
        for i in self.session.run(statement):
            print i


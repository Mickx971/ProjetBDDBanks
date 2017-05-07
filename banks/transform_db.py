from database.connector import Connector
import time;


def transform_db():
    connection = Connector()
    connection.connect()
    session = connection.getSession()
    for i in session.run("match ()-[edge]->() set edge += {__weight__: 1}"):
        print i

    connection.run("match (a) set a +={__tempWeight__:log(size(()-[]->(a))+1)}")
    edges = session.run('''match (b)-[c]->(a) return id(b) as b, type(c) as type, id(a) as a''')

    for edge in edges:
        print edge["a"], edge["b"], edge ["type"]
        connection.run('''match (a) where id(a) = '''+str(edge["a"])+'''  
        match(b) where id(b) ='''+str(edge["b"])+'''  create (a)-[:'''+str(edge["type"])+'''{__weight__:a.__tempWeight__}]->(b)''')
    connection.run("match(a) set a.__tempWeight__=null")
    nodes = session.run('''
            MATCH (n)
            return n, keys(n) as key, ID(n) as id
            ''')
    temp = []
    for node in nodes:
        temp.append(node)

    nodes = temp
    temp = []

    values = []
    for node in nodes:
        for key in node["key"]:
            if not node["n"][str(key)] in values:
                values.append(node["n"][str(key)])

    i = 0
    for value in values:
        statement = "create (value:__value__{value:'"+str(value)+"'}) "
        i = i+1
        for node in nodes:
            if value in node["n"].values():
                variableName = "v"+str(node["id"])
                statement = "match("+variableName+") where ID("+variableName+") = " + str(node["id"]) + " " + statement
                labels = ""
                for key in node["key"]:
                    if node["n"][str(key)] == value:
                        labels = labels + ":" + str(key)
                        statement = statement + "create (value) -[:"+str(key)+"]-> ("+variableName+") "
        for i in session.run(statement):
            print i
        '''print statement
        time.sleep(1)'''

    del nodes
    connection.run("match(a) where not a:__value__ set a = {}")
    connection.run("match (a)-[edge]->() where a:__value__ set edge.__weight__ = 1")









if __name__ == "__main__":
    transform_db()
from database.connector import Connector
from collections import defaultdict


def transform_db():
    connection = Connector()
    connection.connect()
    session = connection.getSession()
    for i in session.run("match ()-[edge]->() set edge += {__weight__: 1}"):
        print i

    connection.run("match (a) set a +={__tempWeight__:log(size(()-[]->(a))+1)}")
    edges = session.run('''match (b)-[c]->(a) return id(b) as b, type(c) as type, id(a) as a''')

    i = 0
    for edge in edges:
        print i, "of 71000"
        connection.run(''.join(["match (a) where id(a) = ",str(edge["a"]),'''  
        match(b) where id(b) =''',str(edge["b"])," create (a)-[:",str(edge["type"]),\
                                "{__weight__:a.__tempWeight__}]->(b)"]))
        i = i+1
    connection.run("match(a) set a.__tempWeight__=null")
    nodes = session.run('''
            MATCH (n)
            return n, keys(n) as key, ID(n) as id
            ''')
    i = 0
    values = defaultdict(list)
    for node in nodes:
        for key in node["key"]:
            values[node["n"][key]].append({"id": node["id"], "attr": key})
            print i, "of 60000"
            i = i + 1


    i = 0
    length = len(values)
    for key in values.iterkeys():
        i = i + 1
        statement = ''.join(["create (value:__value__{value:'", key, "'}) "])
        subQueryNode = list()
        subQueryMatch = list()
        subQueryCreate = list()
        j = 0
        for node in values[key]:
            j = j + 1
            nodeId = str(node["id"])
            variableName = "".join(["v", str(j)])
            subQueryNode.extend([variableName,"=NODE(", nodeId, "),"])
            subQueryMatch.extend([" match(", variableName, ') '])
            subQueryCreate.extend([" create(value)-[:",\
                                     node["attr"],"]->(", variableName, ") "])
        subQueryNode = ''.join(subQueryNode)
        subQueryMatch = ''.join(subQueryMatch)
        subQueryCreate = ''.join(subQueryCreate)
        subQueryNode = subQueryNode[:-1]
        query = ''.join(["start ",subQueryNode,subQueryMatch,statement,subQueryCreate])
        print i, " of ", length
        connection.run(query)


    connection.run("match(a) where not a:__value__ set a = {}")
    connection.run("match (a)-[edge]->() where a:__value__ set edge.__weight__ = 1")









if __name__ == "__main__":
    transform_db()
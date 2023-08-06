class Continent(object):

    def __init__(self, id, nodes):
        self.nodes = nodes
        self.id = id
        for node in nodes:
            node.continent = self


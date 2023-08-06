import os

from nevolution_risk.constants.colors import green, blue, deepskyblue
from nevolution_risk.v3.logic.continent import Continent
from nevolution_risk.v3.logic.continent_loader import ContinentLoader
from nevolution_risk.v3.logic.graphlogic import GraphLoader, RiskGraph
from nevolution_risk.v3.logic.node import Node
from nevolution_risk.v3.logic.player import Player


class Graph(object):

    def __init__(self, player_positions):
        self.player1 = Player('player_one', 120, green)
        self.player2 = Player("player_two", 120, deepskyblue)
        loader = GraphLoader()
        dir_name = os.path.dirname(os.path.realpath(__file__))
        source_graph = loader.load_graph(os.path.join(dir_name, '../../res', 'small.txt'))
        self.graph = RiskGraph(graph=source_graph[0], coord=source_graph[1])
        self.nodes = []
        for n in range(0, self.graph.node_count):
            self.add_node(Node(n, self.graph.get_attributes(n)))

        for n in range(0, self.graph.node_count):
            for m in self.graph.get_adjlist()[n]:
                self.nodes[n].add_node_to_list(self.nodes[m])
                self.nodes[m].add_node_to_list(self.nodes[n])

        continents = ContinentLoader().load_continents(os.path.join(dir_name, '../../res', 'continents.txt'))
        self.continents = []
        n = 0
        countries = []
        for continent in continents:
            for country in continent:
                countries.append(self.nodes[country])
            Continent(n, countries)
            self.continents.append(Continent(n, countries)
                                   )
            countries = []
            n = n + 1

        self.set_player_start(player_positions[0], 0)
        self.set_player_start(player_positions[1], 1)

    def add_node(self, node):
        self.nodes.append(node)

    def set_player_start(self, node, player):
        if player == 0:
            self.nodes[node].player = self.player1
            self.nodes[node].troops = 5
        elif player == 1:
            self.nodes[node].player = self.player2
            self.nodes[node].troops = 5

    def attack(self, v0, v1, attacker):
        attack = self.nodes[v0]
        defend = self.nodes[v1]
        if defend in attack.adj_list:
            if attack.player == attacker:
                if defend.player.name == 'default':
                    defend.player = attacker
                    return True
        return False

    def is_conquered(self):
        for v in self.nodes:
            if v.player.name == 'default':
                return False
        return True


if __name__ == '__main__':
    graph = Graph((1, 8))
    for node in graph.nodes:
        print(node.x, node.y)

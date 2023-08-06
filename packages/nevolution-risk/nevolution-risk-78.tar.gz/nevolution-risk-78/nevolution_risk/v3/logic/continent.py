class Continent(object):

    def __init__(self, id, nodes):
        self.capital = None
        self.reward_level = 0
        self.nodes = nodes
        self.id = id

        for node in nodes:
            node.continent = self

        if self.id == 0:
            self.init(2, 4)
        elif self.id == 1:
            self.init(1, 10)
        elif self.id == 2:
            self.init(2, 17)
        elif self.id == 3:
            self.init(1, 25)
        elif self.id == 4:
            self.init(3, 30)
        elif self.id == 5:
            self.init(1, 41)

    def reward(self):
        reward = self.reward_level
        if self.capital is not None:
            while self.capital.troops <= 5 and reward >= 1:
                self.capital.troops = self.capital.troops + 1
                reward = reward - 1

    def init(self, lvl, capital):
        self.reward_level = lvl
        for node in self.nodes:
            if self.id == capital:
                self.capital = node
                node.capital = True

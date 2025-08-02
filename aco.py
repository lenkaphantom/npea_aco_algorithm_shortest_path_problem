import random

class Ant:
    def __init__(self, graph, distances, pheromones, alpha, beta):
        self.graph = graph
        self.distances = distances
        self.pheromones = pheromones
        self.alpha = alpha  # značaj feromona
        self.beta = beta    # značaj heuristike (udaljenosti)

        self.path = []
        self.total_cost = 0.0
        self.visited = set()

    def select_next_node(self, current_node):
        neighbors = self.graph[current_node]["neighbours"]
        probabilities = []
        total = 0.0

        for neighbor in neighbors:
            if neighbor not in self.visited:
                pheromone = self.pheromones[current_node][neighbor]
                distance = self.distances[(current_node, neighbor)]
                prob = (pheromone ** self.alpha) * ((1.0 / distance) ** self.beta)
                probabilities.append((neighbor, prob))
                total += prob

        if not probabilities:
            return None

        r = random.uniform(0, total)
        cumulative = 0.0
        for neighbor, prob in probabilities:
            cumulative += prob
            if cumulative >= r:
                return neighbor

        return probabilities[-1][0]

    def find_path(self, start, end):
        self.path = [start]
        self.visited = {start}
        current = start

        while current != end:
            next_node = self.select_next_node(current)
            if next_node is None:
                return None
            self.path.append(next_node)
            self.visited.add(next_node)
            self.total_cost += self.distances[(current, next_node)]
            current = next_node

        return self.path

class AntColonyOptimization:
    def __init__(self, graph, distances, num_ants=10, num_iterations=100, alpha=1.0, beta=5.0,
                 evaporation_rate=0.5, pheromone_deposit=100.0):
        self.graph = graph
        self.distances = distances
        self.alpha = alpha
        self.beta = beta
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.evaporation_rate = evaporation_rate
        self.pheromone_deposit = pheromone_deposit

        self.pheromones = self.initialize_pheromones()
        self.best_path = None
        self.best_cost = float('inf')

    def initialize_pheromones(self):
        pheromones = {}
        for node_id, node_data in self.graph.items():
            pheromones[node_id] = {}
            for neighbor_id in node_data['neighbours']:
                pheromones[node_id][neighbor_id] = 1.0  # inicijalna vrednost
        return pheromones

    def evaporate_pheromones(self):
        for u in self.pheromones:
            for v in self.pheromones[u]:
                self.pheromones[u][v] *= (1 - self.evaporation_rate)
                self.pheromones[u][v] = max(self.pheromones[u][v], 1e-6)

    def deposit_pheromones(self, ants):
        for ant in ants:
            if not ant.path:
                continue
            deposit = self.pheromone_deposit / ant.total_cost
            for i in range(len(ant.path) - 1):
                u, v = ant.path[i], ant.path[i + 1]
                self.pheromones[u][v] += deposit

    def run(self, start, end):
        for iteration in range(self.num_iterations):
            ants = [
                Ant(self.graph, self.distances, self.pheromones, self.alpha, self.beta)
                for _ in range(self.num_ants)
            ]

            for ant in ants:
                path = ant.find_path(start, end)
                if path and ant.total_cost < self.best_cost:
                    self.best_path = path
                    self.best_cost = ant.total_cost

            self.evaporate_pheromones()
            self.deposit_pheromones(ants)

        return self.best_path, self.best_cost
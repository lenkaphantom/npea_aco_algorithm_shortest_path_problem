import random

class Ant:
    """
    Represents an ant in the Ant Colony Optimization algorithm.
    
    Each ant traverses the graph to find a path from start to end node,
    using pheromone trails and heuristic information to guide decisions.
    """
    
    def __init__(self, graph, distances, pheromones, alpha, beta):
        """
        Initialize an ant with graph data and ACO parameters.
        
        Args:
            graph (dict): Graph adjacency list with coordinates and neighbors
            distances (dict): Distance dictionary for edge weights
            pheromones (dict): Pheromone levels on edges
            alpha (float): Pheromone influence parameter
            beta (float): Heuristic influence parameter
        """
        self.graph = graph
        self.distances = distances
        self.pheromones = pheromones
        self.alpha = alpha
        self.beta = beta
        self.path = []
        self.visited = set()
        self.total_cost = 0
        self.recent_nodes = []
        self.max_recent = 5
        
    def find_path(self, start, end, max_steps=20000):
        """
        Find a path from start to end node using ACO principles.
        
        Args:
            start (str): Starting node ID
            end (str): Target node ID
            max_steps (int): Maximum number of steps before giving up
            
        Returns:
            list: Path as list of node IDs, or None if no path found
        """
        self.path = [start]
        self.visited = {start}
        self.total_cost = 0
        self.recent_nodes = [start]
        
        current = start
        steps_without_progress = 0
        last_visited_count = 0
        escape_mode = False
        escape_steps = 0
        
        for step in range(max_steps):
            if current == end:
                return self.path
                
            neighbors = self.graph[current]["neighbours"]
            available = [(neighbor, cost) for neighbor, cost in neighbors.items() 
                        if neighbor in self.graph]
            
            if not available:
                break
            
            # Progress tracking
            if len(self.visited) == last_visited_count:
                steps_without_progress += 1
            else:
                steps_without_progress = 0
                last_visited_count = len(self.visited)
                escape_mode = False
                escape_steps = 0
            
            # Mode selection
            if steps_without_progress > 100:
                if not escape_mode:
                    escape_mode = True
                    escape_steps = 0
                escape_steps += 1
            
            # Node selection
            if escape_mode and escape_steps < 200:
                next_node = self._aggressive_escape(available, current, end)
            else:
                next_node = self._greedy_selection(available, current, end)
                if escape_mode and escape_steps >= 200:
                    escape_mode = False
                    escape_steps = 0
            
            if next_node is None:
                break
            
            # Move to next node
            edge_cost = neighbors[next_node]
            self.total_cost += edge_cost
            self.path.append(next_node)
            self.visited.add(next_node)
            
            self.recent_nodes.append(next_node)
            if len(self.recent_nodes) > self.max_recent:
                self.recent_nodes.pop(0)
            
            current = next_node
        
        return None
    
    def _greedy_selection(self, available, current, end):
        """
        Select next node using greedy strategy with goal-oriented heuristic.
        
        Args:
            available (list): List of (neighbor, cost) tuples
            current (str): Current node ID
            end (str): Target node ID
            
        Returns:
            str: Selected neighbor node ID
        """
        unvisited = [(n, c) for n, c in available if n not in self.visited]
        visited_non_recent = [(n, c) for n, c in available 
                             if n in self.visited and n not in self.recent_nodes]
        visited_recent = [(n, c) for n, c in available 
                         if n in self.visited and n in self.recent_nodes]
        
        if unvisited:
            candidates = unvisited
        elif visited_non_recent:
            candidates = visited_non_recent
        else:
            candidates = visited_recent
        
        best_candidates = []
        best_heuristic = -1
        
        for neighbor, edge_cost in candidates:
            if end in self.distances and neighbor in self.distances[end]:
                goal_distance = self.distances[end][neighbor]
            else:
                goal_distance = float('inf')
            
            heuristic = 1.0 / (goal_distance + edge_cost + 1.0)
            
            if heuristic > best_heuristic:
                best_heuristic = heuristic
                best_candidates = [neighbor]
            elif abs(heuristic - best_heuristic) < 1e-6:
                best_candidates.append(neighbor)
        
        return random.choice(best_candidates) if best_candidates else None

    def _aggressive_escape(self, available, current, end):
        """
        Escape strategy to break out of local search areas.
        
        Args:
            available (list): List of (neighbor, cost) tuples
            current (str): Current node ID
            end (str): Target node ID
            
        Returns:
            str: Selected neighbor node ID for escape
        """
        unvisited = [n for n, c in available if n not in self.visited]
        
        if unvisited:
            if end in self.distances:
                def goal_distance(node):
                    return self.distances[end].get(node, float('inf'))
                
                unvisited.sort(key=goal_distance)
                top_candidates = unvisited[:min(3, len(unvisited))]
                return random.choice(top_candidates)
            else:
                return random.choice(unvisited)
        
        visited_with_distance = []
        for neighbor, cost in available:
            if neighbor in self.path:
                try:
                    last_visit_index = len(self.path) - 1 - self.path[::-1].index(neighbor)
                    distance_from_last_visit = len(self.path) - last_visit_index
                    visited_with_distance.append((neighbor, distance_from_last_visit))
                except ValueError:
                    continue
        
        if visited_with_distance:
            visited_with_distance.sort(key=lambda x: x[1], reverse=True)
            return visited_with_distance[0][0]
        
        return random.choice([n for n, c in available]) if available else None


class AntColonyOptimization:
    """
    Ant Colony Optimization algorithm for pathfinding.
    
    Uses multiple ants to explore the graph and find optimal paths
    by depositing and following pheromone trails.
    """
    
    def __init__(self, graph, distances, num_ants=25, num_iterations=50, 
                 alpha=1.5, beta=3.0, evaporation_rate=0.1, pheromone_deposit=50):
        """
        Initialize ACO algorithm with parameters.
        
        Args:
            graph (dict): Graph adjacency list
            distances (dict): Edge distance dictionary
            num_ants (int): Number of ants per iteration
            num_iterations (int): Number of iterations to run
            alpha (float): Pheromone influence weight
            beta (float): Heuristic influence weight
            evaporation_rate (float): Pheromone evaporation rate (0-1)
            pheromone_deposit (float): Amount of pheromone deposited
        """
        self.graph = graph
        self.distances = distances
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone_deposit = pheromone_deposit
        self.pheromones = {}
        self.best_path = None
        self.best_cost = float('inf')
        
    def run(self, start, end):
        """
        Execute the ACO algorithm to find optimal path.
        
        Args:
            start (str): Starting node ID
            end (str): Target node ID
            
        Returns:
            tuple: (best_path, best_cost) where best_path is list of node IDs
                   and best_cost is the total path cost
        """
        for iteration in range(self.num_iterations):
            iteration_best_cost = float('inf')
            successful_ants = 0
            
            for ant_id in range(self.num_ants):
                ant = Ant(self.graph, self.distances, self.pheromones, 
                         self.alpha, self.beta)
                
                path = ant.find_path(start, end)
                
                if path and len(path) < 10000:
                    successful_ants += 1
                    cost = ant.total_cost
                    
                    if cost < iteration_best_cost:
                        iteration_best_cost = cost
                        
                    if cost < self.best_cost:
                        self.best_cost = cost
                        self.best_path = path
                    
                    self._deposit_pheromones(path, cost)
            
            self._evaporate_pheromones()
            
            if self.best_path and len(self.best_path) < 200:
                break
        
        return self.best_path, self.best_cost
    
    def _deposit_pheromones(self, path, cost):
        """
        Deposit pheromones along the given path.
        
        Args:
            path (list): List of node IDs representing the path
            cost (float): Total cost of the path
        """
        if len(path) > 1000:
            deposit_amount = self.pheromone_deposit / (cost * 0.1)
        else:
            deposit_amount = self.pheromone_deposit / cost
            
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            if edge not in self.pheromones:
                self.pheromones[edge] = 0
            self.pheromones[edge] += deposit_amount
    
    def _evaporate_pheromones(self):
        """
        Apply pheromone evaporation to all edges.
        """
        for edge in self.pheromones:
            self.pheromones[edge] *= (1 - self.evaporation_rate)
            if self.pheromones[edge] < 0.01:
                self.pheromones[edge] = 0.01
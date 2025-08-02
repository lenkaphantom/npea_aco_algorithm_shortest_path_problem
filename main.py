from graph_parser import *
from aco import AntColonyOptimization
from collections import deque


def is_reachable(graph, start, end):
    visited = set()
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        if node == end:
            return True
        visited.add(node)
        for neighbor in graph[node]["neighbours"]:
            if neighbor not in visited and neighbor in graph:
                queue.append(neighbor)
    return False


if __name__ == "__main__":
    graph = parse_graph("data/data_path_nodes.txt")
    graph = make_graph_bidirectional(graph)
    graph = calculate_distances(graph) 
    distances = get_distance_dict(graph)

    start = "3653296222"
    end = "3653134376"
    
    print("Start node in graph:", start in graph)
    print("End node in graph:", end in graph)

    aco = AntColonyOptimization(
        graph, distances,
        num_ants=20,
        num_iterations=100,
        alpha=1.0,
        beta=3.0,
        evaporation_rate=0.5,
        pheromone_deposit=100
    )

    best_path, best_cost = aco.run(start, end)
    
    if not is_reachable(graph, start, end):
        print(f"No path exists between {start} and {end}.")
        exit(1)

    if best_path:
        print(f"Best path found: {' -> '.join(best_path)}")
        print(f"Total cost: {best_cost}")
    else:
        print("No path found.")

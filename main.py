from graph_parser import *
from aco import AntColonyOptimization

if __name__ == "__main__":
    graph = parse_graph("data/data_path_nodes.txt")
    graph = calculate_distances(graph)
    distances = get_distance_dict(graph)

    start = "3653296222"
    end = "3653134376"

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

    if best_path:
        print(f"Best path found: {' -> '.join(best_path)}")
        print(f"Total cost: {best_cost}")
    else:
        print("No path found.")

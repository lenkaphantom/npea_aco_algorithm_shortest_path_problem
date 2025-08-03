from graph_parser import *
from aco import AntColonyOptimization

if __name__ == "__main__":
    # Učitaj i pripremi graf
    graph = parse_graph("data/data_path_nodes.txt")
    graph = calculate_distances(graph)
    distances = get_distance_dict(graph)

    start = "3653296222"
    end = "3653134376"
    
    print(f"Graph loaded: {len(graph)} nodes")
    print(f"Searching path from {start} to {end}")
    
    # Kreiraj i pokreni ACO
    aco = AntColonyOptimization(
        graph, distances,
        num_ants=25,
        num_iterations=50,
        alpha=1.5,
        beta=3.0,
        evaporation_rate=0.1,
        pheromone_deposit=50
    )
    
    print("\nRunning ACO...")
    best_path, best_cost = aco.run(start, end)

    if best_path:
        print(f"\nSUCCESS!")
        print(f"Best path length: {len(best_path)} nodes")
        print(f"Total cost: {best_cost:.2f}")
        print(f"Path sample: {' -> '.join(best_path[:10])}...")
    else:
        print("\nFAILED: No path found.")

from graph_parser import *

if __name__ == "__main__":
    graph = parse_graph("data/data_path_nodes.txt")
    graph = calculate_distances(graph)
    print(graph)

import math

def parse_graph(filepath):
    """
    Parses a graph from a file and returns its adjacency list representation.

    The input file must contain lines in the format:
    node_id(x,y):neighbor_id1,neighbor_id2,...

    Returns:
        dict: A dictionary where each node ID maps to a dict containing its coordinates 
              and a dictionary of neighboring node IDs with placeholder None distances.
    """
    graph = {}

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or ':' not in line:
                continue

            node, neighbours = line.split(':')
            node = node.strip()
            node_id, coords = node.split('(')
            coords = coords.strip(')')
            x_coord, y_coord = coords.split(',')

            x = float(x_coord)
            y = float(y_coord)

            neighbours = neighbours.strip().split(',')

            graph[node_id.strip()] = {
                'coords': (x, y),
                'neighbours': {}
            }

            for neighbour in neighbours:
                graph[node_id]['neighbours'][neighbour.strip()] = None

    return graph


def euclidean_distance(x1, y1, x2, y2):
    """
    Calculates the Euclidean distance between two 2D points.

    Args:
        x1, y1 (float): Coordinates of the first point.
        x2, y2 (float): Coordinates of the second point.

    Returns:
        float: Euclidean distance between the two points.
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_distances(graph):
    """
    Calculates and fills in the Euclidean distances between each node and its neighbors.

    Args:
        graph (dict): The graph dictionary with node coordinates and neighbor placeholders.

    Returns:
        dict: The updated graph with actual distances between connected nodes.
    """
    for node_id, values in graph.items():
        x1, y1 = values['coords']
        for neighbour_id in values['neighbours']:
            if neighbour_id in graph:
                x2, y2 = graph[neighbour_id]['coords']
                distance = euclidean_distance(x1, y1, x2, y2)
                graph[node_id]['neighbours'][neighbour_id] = distance

    return graph

if __name__ == "__main__":
    graph = parse_graph("data/data_path_nodes.txt")
    graph = calculate_distances(graph)
    print(graph)
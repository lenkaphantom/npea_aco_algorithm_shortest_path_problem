import math


def parse_graph(filepath):
    """
    Parses a graph from a file and returns its adjacency list representation.

    Each line in the file should have the format:
        node_id(x,y):neighbor_id1,neighbor_id2,...

    Returns:
        dict: A dictionary where each node ID maps to a dict containing:
              - 'coords': Tuple[float, float] with (x, y) coordinates
              - 'neighbours': Dict[str, None] mapping neighbor IDs to None (to be filled later)
    """
    graph = {}

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or ':' not in line:
                continue

            try:
                node_part, neighbours_part = line.split(':')
                node_id, coords = node_part.strip().split('(')
                coords = coords.strip(')')
                x, y = map(float, coords.split(','))

                neighbour_ids = [nid.strip() for nid in neighbours_part.strip().split(',') if nid.strip()]

                graph[node_id.strip()] = {
                    'coords': (x, y),
                    'neighbours': {nid: None for nid in neighbour_ids}
                }
            except ValueError:
                print(f"Skipping malformed line: {line}")
                continue

    return graph


def euclidean_distance(x1, y1, x2, y2):
    """
    Calculates the Euclidean distance between two 2D points.

    Args:
        x1, y1, x2, y2 (float): Coordinates of the two points.

    Returns:
        float: The Euclidean distance.
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_distances(graph):
    """
    Calculates and fills the actual Euclidean distances between each node and its neighbors.

    Args:
        graph (dict): Graph where each node has coordinates and neighbor IDs.

    Returns:
        dict: Graph with distances filled into the 'neighbours' dicts.
    """
    for node_id, data in graph.items():
        x1, y1 = data['coords']
        for neighbour_id in list(data['neighbours']):
            if neighbour_id in graph:
                x2, y2 = graph[neighbour_id]['coords']
                dist = euclidean_distance(x1, y1, x2, y2)
                if dist == 0:
                    print(f"Warning: skipping zero-distance edge {node_id} <-> {neighbour_id}")
                    del data['neighbours'][neighbour_id]
                    continue
                data['neighbours'][neighbour_id] = dist
            else:
                print(f"Warning: neighbor {neighbour_id} of {node_id} not found in graph.")
    return graph



def get_distance_dict(graph):
    """
    Extracts a flat dictionary of distances between directly connected nodes.

    Args:
        graph (dict): Graph with coordinates and neighbor distances.

    Returns:
        dict: Dictionary with keys as (from_node, to_node) tuples and values as distances.
    """
    distances = {}
    for node_id, data in graph.items():
        for neighbour_id, dist in data['neighbours'].items():
            if dist is not None:
                distances[(node_id, neighbour_id)] = dist
    return distances


def make_graph_bidirectional(graph):
    """
    Makes the graph bidirectional by adding edges in both directions.
    """
    for node_id, data in graph.items():
        for neighbor_id in list(data['neighbours']):
            if neighbor_id in graph:
                graph[neighbor_id]['neighbours'][node_id] = graph[node_id]['neighbours'][neighbor_id]
                
    return graph


if __name__ == "__main__":
    filepath = "data/data_path_nodes.txt"
    graph = parse_graph(filepath)
    graph = calculate_distances(graph)
    distances = get_distance_dict(graph)

    print("Sample node data:")
    for node, data in list(graph.items())[:5]:
        print(f"{node}: {data}")

    print("\nSample distances:")
    for edge, dist in list(distances.items())[:5]:
        print(f"{edge}: {dist:.2f}")

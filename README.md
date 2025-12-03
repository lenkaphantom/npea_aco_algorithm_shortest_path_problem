## 🐜 Ant Colony Optimization – Shortest Path Solver

This project implements an Ant Colony Optimization (ACO) algorithm to solve the Shortest Path Problem in a 2D graph.
Nodes and adjacency information are loaded from a file, and the algorithm uses a nature-inspired, probabilistic approach to iteratively converge toward the optimal route between two points.

📌 Features
- ACO-based pathfinding inspired by real ant foraging behavior
- Graph loaded from text file (data_path_nodes.txt)
- Automatic edge weight calculation using Euclidean distance
- Customizable ACO parameters (pheromone importance, heuristic importance, evaporation rate, number of ants, etc.)
- Search for shortest path from a user-defined start node to a destination node
- Modular structure — easy to extend or integrate into another project

## 📁 Project Structure
```
├─ main.py                # Program entry point
├─ graph_parser.py        # Loads nodes & neighbors, builds graph
├─ aco.py                 # Ant Colony Optimization implementation
├─ data/
│   └─ data_path_nodes.txt # Graph input file
└─ README.md
```

Ant Colony Optimization – Shortest Path Problem
This project implements an Ant Colony Optimization (ACO) algorithm to solve the shortest path problem in a graph defined by 2D nodes. 
The nodes and their neighbors are loaded from a file (data_path_nodes.txt), where each edge weight is calculated as the Euclidean distance between two connected nodes. 
The goal is to find the shortest path from a given start node to a destination node using a nature-inspired, probabilistic search strategy.

project structure:
├── main.py
├── graph_parser.py
├── aco.py
├── data/
│   └── data_path_nodes.txt
└── README.md

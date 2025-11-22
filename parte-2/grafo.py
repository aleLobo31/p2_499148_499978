import re


class Graph:
    # Graph Constructor
    def __init__(self, vertices: int, edges: int, lines: list) -> None:
        # Define private members
        self._n_vertices = vertices
        self._n_edges = edges
        self._adjacency_list = [[] for v in range(vertices+1)]
                
        # Define regex for extract vertices and its associated distances
        regex = re.compile(r'^a\s+(\d+)\s+(\d+)\s+(\d+)\s+$')

        # Process graph file to create adjacency matrix
        for i in range(0, len(lines)):
            # Extract the edge and its distance
            match = re.match(regex, lines[i])
            if(match):
                # Update adjacency matrix
                self._adjacency_list[int(match[1])].append((match[2], match[3]))
    
    # Attributes Getters
    @property
    def n_vertices(self):
        return self._n_vertices
    
    @property
    def n_edges(self):
        return self._n_edges
    
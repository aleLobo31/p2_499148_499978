import re, math, random


class Graph:
    # Graph Constructor
    def __init__(self, vertices: int, edges: int, lines: list) -> None:
        # Define private members
        self._n_vertices = vertices
        self._n_edges = edges
        self._adjacency_list = [[] for v in range(vertices+1)]
        self._coordinates = [None] * (vertices + 1)
                
        # Define regex for extract vertices and its associated distances
        regex = re.compile(r'^a\s+(\d+)\s+(\d+)\s+(\d+)\s+$')

        # Process graph file to create adjacency matrix
        for i in range(0, len(lines)):
            # Extract the edge and its distance
            match = re.match(regex, lines[i])
            if(match):
                # Update adjacency matrix
                self._adjacency_list[int(match[1])].append((int(match[3]), int(match[2])))
    
    def load_coordinates(self, lines: list) -> None:
        # Regex: v <id> <lon> <lat>
        # Nota: -? permite capturar números negativos (longitud oeste)
        regex_coord = re.compile(r'^v\s+(\d+)\s+(-?\d+)\s+(-?\d+)')

        for line in lines:
            if line.startswith('v'):
                match = regex_coord.match(line)
                if match:
                    node_id = int(match[1])
                    # El enunciado dice que vienen multiplicados por 10^6
                    lon_int = int(match[2])
                    lat_int = int(match[3])
                    
                    # Convertir a grados reales y guardar
                    # Guardamos como (lat, lon) para facilitar Haversine
                    self._coordinates[node_id] = (lat_int / 1000000.0, lon_int / 1000000.0)

    def get_euclid_projected(self, node1, node2):
        if self._coordinates[node1] is None or self._coordinates[node2] is None:
            return 0.0

        lat1, lon1 = self._coordinates[node1]
        lat2, lon2 = self._coordinates[node2]

        # Distancia aproximada en grados → metros
        # 1 grado de latitud ≈ 111320m
        # longitud corregida por cos(lat)
        dx = (lon2 - lon1) * 111320 * math.cos(math.radians((lat1 + lat2) / 2))
        dy = (lat2 - lat1) * 111320

        return math.sqrt(dx * dx + dy * dy) * 2

    def get_adjacent_nodes(self, node: int) -> list[tuple]:
        return self._adjacency_list[node]

    # Attributes Getters
    @property
    def n_vertices(self):
        return self._n_vertices
    
    @property
    def n_edges(self):
        return self._n_edges
    
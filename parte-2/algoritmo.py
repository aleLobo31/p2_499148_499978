from grafo import Graph
from abierta import Abierta
from cerrada import Cerrada

'''
TODO: Ahora mismo esto es un Diskstra faltan implementar
      las heurísticas para que se convierta en un A*.
'''
class SearchAlgorithm:
    def __init__(self, graph: Graph):
        # Save graph reference
        self._graph = graph
        # Create Open List
        self._abierta = Abierta()
        # Create Close List and leave it empty for the moment
        self._cerrada = Cerrada()
        # Create Empty Solution
        self._path = []
        # Stats variables
        self._generations = 0
        self._expansions = 0

    def solve_dijkstra(self, init_node: int, final_node: int) -> bool:
        # Reset Data Stuctures
        self._abierta.reset()
        self._cerrada.reset()
        self._path = []
        parents = {}
        self._generations = 1
        self._expansions = 0

        # Add init node to open list
        self._abierta.add(0, init_node)

        # While open list is not empty continue
        while(not self._abierta.is_empty()):
            # Extract node with the least cost from open list (and remove it)
            current_node_cost, current_node_id = self._abierta.get_best()

            # Check if current node is in close list
            if(self._cerrada.contains(current_node_id)):
                continue

            # Check if we have reached goal node
            if(current_node_id == final_node):
                # Save Solution Path
                self.reconstruct_path(parents, final_node)
                print(f"Solución óptima encontrada con coste {current_node_cost}")
                return True
            
            # Add current node to close list
            self._cerrada.add(current_node_id)

            # Extract current node neighbours
            neighbours = self._graph.get_adjacent_nodes(current_node_id)
            # Update Expanded nodes
            self._expansions += 1

            # Add neighbours to open list that are not in close list
            for neighbour in neighbours:
                neighbour_node_id = neighbour[1]
                neighbour_node_cost = neighbour[0]
                if not self._cerrada.contains(neighbour_node_id):
                    # Compute accumulated cost
                    new_cost = current_node_cost + neighbour_node_cost
                    # Add new node with accumulated cost
                    self._abierta.add(new_cost, neighbour_node_id)
                    # Save the parent
                    parents[neighbour_node_id] = (neighbour_node_cost, current_node_id)
                    # Update generated nodes
                    self._generations += 1
        
        return False

    def solve_astar(self, init_node: int, final_node: int) -> bool:
        self._abierta.reset()
        self._cerrada.reset()
        self._path = []
        parents = {}
        
        # Necesitamos g_score separado de la prioridad del heap
        g_score = {init_node: 0}
        
        # Calcular heurística inicial
        h_start = self._graph.get_euclid_projected(init_node, final_node)
        
        # Añadimos a abierta con f(n)
        self._abierta.add(h_start, init_node)

        while not self._abierta.is_empty():
            # Lo que sacamos es f(n), NO el coste real
            current_f, current_node = self._abierta.get_best()

            if current_node == final_node:
                self.reconstruct_path(parents, final_node)
                print(f"Solución óptima encontrada con coste {g_score[current_node]}")
                return True

            if self._cerrada.contains(current_node):
                continue
            self._cerrada.add(current_node)
            
            # Recuperamos el coste real (g) limpio para hacer las sumas
            current_g = g_score[current_node]
            self._expansions += 1

            # Expandir vecinos
            for weight, neighbour_id in self._graph.get_adjacent_nodes(current_node):
                tentative_g = current_g + weight

                # Si encontramos un camino mejor...
                if tentative_g < g_score.get(neighbour_id, float('inf')):
                    g_score[neighbour_id] = tentative_g
                    parents[neighbour_id] = (weight, current_node)
                    
                    # EN A*: Calculamos heurística y sumamos
                    h_cost = self._graph.get_euclid_projected(neighbour_id, final_node)
                    f_cost = tentative_g + h_cost

                    if not self._cerrada.contains(neighbour_id):
                        self._abierta.add(f_cost, neighbour_id)
                        self._generations += 1
        return False

    def reconstruct_path(self, parents: dict, final_node: int) -> None:
        # Create empty path
        self._path = []
        curr_node = final_node

        # Reconstruct path
        while(curr_node in parents):
            # Get parent
            prev_node = parents[curr_node]

            # Extract parent id and cost
            prev_node_id = prev_node[1]
            prev_node_cost = prev_node[0]

            # Added to the path
            self._path.append((prev_node_id, prev_node_cost, curr_node))
            
            # Update current node
            curr_node = prev_node_id

        # Invert path
        self._path.reverse()

        return
    
    @property
    def path(self):
        return self._path
    
    @property
    def generations(self):
        return self._generations
    
    @property
    def expansions(self):
        return self._expansions

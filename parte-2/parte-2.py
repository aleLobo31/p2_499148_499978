import sys
import re
import time
from grafo import Graph
from algoritmo import SearchAlgorithm

def main() -> int:
    if len(sys.argv) != 5:
        print("El número de argumentos no es correcto, debes ejecutar: ./parte-2.py <id1> <id2> <nombre-del-mapa> <fichero-salida>")
        return -1
    
    graph_path = sys.argv[3] + ".gr"
    regex_pattern = re.compile(r'^p\s+sp\s+(\d+)\s+(\d+)$')
    try:
        # Open Graph file
        with open(graph_path, "r") as g:
            # Read lines
            lines = g.readlines()
            # Extract number of vertices and edges
            match = re.match(regex_pattern, lines[4])
            # Create Graph
            map_graph = Graph(int(match[1]), int(match[2]), lines)
            
    except FileNotFoundError:
        print(f"El fichero {graph_path} no existe o la ruta es incorrecta.")
        return -1
    
    print(f"# vertices: {map_graph.n_vertices}")
    print(f"# arcos   : {map_graph.n_edges}")
    print("\n")
    
    # Create Solver with our implementation of Heuristic Search Algorithm
    engine = SearchAlgorithm(map_graph)

    # Compute the solution if exists
    start_time = time.perf_counter()
    engine.solve(int(sys.argv[1]), int(sys.argv[2]))
    end_time = time.perf_counter()
    diff = end_time - start_time

    print(f"Tiempo de ejecución: {diff:.2f} segundos")
    print(f"# expansiones      : {engine.expansions} ({engine.generations/diff:.2f} nodes/sec)")

    # Write the solution into output file
    output_file = sys.argv[4]
    try:
        with open(output_file, "w") as f:
            for idx, segment in enumerate(engine.path):
                if(idx == 0):
                    f.write(f'{str(segment[0])} - ({str(segment[1])}) - {str(segment[2])} ')
                else:
                    f.write(f'- ({str(segment[1])}) - {str(segment[2])} ')
                
    except FileNotFoundError:
        print(f"El fichero {output_file} no existe o la ruta es incorrecta.")
        return -1

    return 0

if __name__ == "__main__":
    main()
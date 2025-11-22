import sys
import re
from grafo import Graph

def main() -> int:
    if len(sys.argv) != 5:
        print("El número de argumentos no es correcto, debes ejecutar: ./parte-2.py <id1> <id2> <nombre-del-mapa> <fichero-salida>")
        return -1
    
    # Open Graph file
    graph_path = sys.argv[3] + ".gr"
    regex_pattern = re.compile(r'^p\s+sp\s+(\d+)\s+(\d+)$')
    try:
        with open(graph_path, "r") as g:
            lines = g.readlines()

            # Extract number of vertices and edges
            match = re.match(regex_pattern, lines[4])

            # Create Graph
            Graph(int(match[1]), int(match[2]), lines)
            
    except FileNotFoundError:
        print(f"El fichero {graph_path} no existe o la ruta es incorrecta.")
        return -1
    
    return 0

if __name__ == "__main__":
    main()
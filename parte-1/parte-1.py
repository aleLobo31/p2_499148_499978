#!/usr/bin/env python3

import sys
import constraint as c
from itertools import combinations

def main() -> int:
    # Comprobamos que el script haya recibido el número de argumentos correcto
    if len(sys.argv) != 3:
        print("El script debe ejecutarse de la siguiente manera: ./parte-1.py <nombre_fichero_entrada>.in <nombre_fichero_salida>.out")
        return -1
    
    # Creamos una instancia de SCP
    problem = c.Problem()
    
    # Abrimos el fichero de entrada
    i = 0
    input_file = sys.argv[1]
    try:
        # Procesamos el fichero y agregamos las variables
        with open(input_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                j = 0
                for elem in line.strip():
                    if(elem == "."):
                        problem.addVariable(f'c{i}{j}', [0, 1])
                    elif(elem == "X"):
                        problem.addVariable(f'c{i}{j}', [0])
                    elif(elem == "O"):
                        problem.addVariable(f'c{i}{j}', [1])
                    else:
                        print(f"Error: El elemento {elem} no está reconocido.")
                        return -1
                    j += 1
                i += 1
    except FileNotFoundError:
        print("Error: El fichero de entrada proporcionado no existe.")
        return -1
    
    # =================================================================
    # Escribimos en la salida el escenario y lo imprimimos por pantalla
    # =================================================================
    output_file = sys.argv[2]
    scenario = problem._variables
    try:
        with open(output_file, 'w') as of:
            for col in range(j):
                of.write("+---")
                print("+---", end="")
            of.write("+\n")
            print("+")

            for row in range(i):
                for col in range(j):
                    key = f"c{row}{col}"
                    if(len(scenario[key]) == 1):
                        if(scenario[key][0]):
                            of.write("| O ")
                            print("| O ", end="")
                        else:
                            of.write("| X ")
                            print("| X ", end="")
                    else:
                        of.write("|   ")
                        print("|   ", end="")
                of.write("|\n")
                print("|")

            for col in range(j):
                of.write("+---")
                print("+---", end="")
            of.write("+\n")
            print("+")
    except Exception as e:
        print(f"Error: No se ha podido escribir la solución correctamente en el fichero de salida")
        return -1

    # ===========================
    # Agregamos las restricciones
    # ===========================
    # [1] Todas las filas deben tener el mismo número de fichas negras y blancas
    for row in range(i):
        row_variables = [f'c{row}{col}' for col in range(j)]
        problem.addConstraint(
            lambda *values: sum(values) == i/2,
            row_variables
        )
    # [2] Todas las columnas deben tener el mismo número de fichas negras y blancas
    for col in range(j):
        col_variables = [f'c{row}{col}' for row in range(j)]
        problem.addConstraint(
            lambda *values: sum(values) == i/2,
            col_variables
        )
    
    # [3] No puede haber más de dos fichas del mismo tipo consecutivas en una fila
    for row in range(i):
        soporte = 0
        while(soporte <= j - 3):
            # Extraemos el grupo de 3 variables consecutivas
            col_variables = [f'c{row}{col}' for col in range(soporte, soporte+3)]
            # Añadimos la restricción la suma del grupo no puede ser ni 0 (3 'X') ni 3 (3 'O')
            problem.addConstraint(
                lambda *values: sum(values) != 0 and sum(values) != 3,
                col_variables
            )
            # Iteramos la ventana deslizante
            soporte += 1

    # [4] No puede haber más de dos fichas del mismo tipo consecutivas en una columna
    for col in range(j):
        soporte = 0
        while(soporte <= i - 3):
            # Extraemos el grupo de 3 variables consecutivas
            row_variables = [f'c{row}{col}' for row in range(soporte, soporte+3)]
            # Añadimos la restricción la suma del grupo no puede ser ni 0 (3 'X') ni 3 (3 'O')
            problem.addConstraint(
                lambda *values: sum(values) != 0 and sum(values) != 3,
                row_variables
            )
            # Iteramos la ventana deslizante
            soporte += 1

    # ======================
    # Computamos la solución
    # ======================
    sols = problem.getSolutions()
    if sols:
        print(f"{len(sols)} soluciones encontradas")
    else:
        print("0 soluciones encontradas")

        try:
            with open(output_file, 'a') as of:
                of.write("No se ha encontrado solución\n")
        except Exception as e:
            print(f"Error: No se ha podido escribir la solución correctamente en el fichero de salida")
        return 0

    # ====================================
    # Escribimos la solución en la salida
    # ====================================
    try:
        with open(output_file, 'a') as of:
            for col in range(j):
                of.write("+---")
            of.write("+\n")

            for row in range(i):
                for col in range(j):
                    key = f"c{row}{col}"
                    if sols[0][key]:
                        of.write("| O ")
                    else:
                        of.write("| X ")
                of.write("|\n")

            for col in range(j):
                of.write("+---")
            of.write("+\n")
    except Exception as e:
        print(f"Error: No se ha podido escribir la solución correctamente en el fichero de salida")
        return -1
    
    return 0

if __name__ == "__main__":
    main()
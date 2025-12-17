class Abierta:
    '''
    Lista Abierta basado en Árbol Binario donde la RAÍZ siempre tiene al valor MÁS PEQUEÑO
    '''
    def __init__(self) -> None:
        self._abierta = []

    def add(self, cost: int, node: int) -> None:
        # Creamos la tupla (el objeto abstracto que vamos a añadir)
        new_node = (cost, node)

        # Primero añadimos el elemento al final de la lista
        self._abierta.append(new_node)

        # Extraemos el índice del nuevo nodo
        new_node_idx = len(self._abierta) - 1

        # Reestructuramos el árbol
        self._float(new_node_idx)

        return None

    def get_best(self) -> tuple:
        # Calculamos los elementos de la lista
        n_elems = len(self._abierta)

        # Comprobamos si la lista está vacía, tiene un elemento o es un caso 'normal'
        if(n_elems > 1):
            # Guardamos el mejor temporal para devolerlo más tarde
            best_node = self._abierta[0]

            # Eliminamos el último elemento
            last_node = self._abierta.pop()

            if(self._abierta):
                # Movemos el último elemento a la raíz
                self._abierta[0] = last_node

                # Volvemos a balancear el árbol 'hundiendo' el elemento
                self._sink(0)

            # Devolvemos el mejor nodo
            return best_node
        elif(n_elems == 1):
            return self._abierta.pop()
        else:
            raise IndexError("La lista se encuentra vacía")

    def is_empty(self) -> bool:
        return len(self._abierta) == 0
    
    def reset(self) -> None:
        self._abierta = []

    def _float(self, idx: int) -> None:
        '''
        'Hace flotar' el elemento hasta que no es menor que su padre
        '''
        # Declaramos las variables que vamos a utilizar
        is_balanced = False
        curr_idx = idx

        # Hasta que llege a la raíz o ya esté ordenado intercambio hijo con padre hasta que se ordene
        while(curr_idx > 0 and not is_balanced):
            # Calculamos la posición del padre
            parent_idx = (curr_idx - 1) // 2

            # Comprobamos si hay que intercambiarlo con el padre
            if self._abierta[curr_idx][0] < self._abierta[parent_idx][0]:
                # Guardamos el elemento a intercambiar
                curr_elem = self._abierta[curr_idx]

                # Cambiamos el padre a la posición del hijo
                self._abierta[curr_idx] = self._abierta[parent_idx]

                # Cambiamos el hijo a la posición del padre
                self._abierta[parent_idx] = curr_elem

                # Cambiamos el índice actual
                curr_idx = parent_idx
            else:
                is_balanced = True

        return None
    
    def _sink(self, idx: int) -> None:
        '''
        'Hundimos' el elemento de la posición pasada hasta que no tenga hijos menores que él
        '''
        # Declaramos las variables que vamos a utilizar
        is_balanced = False
        curr_idx = idx
        length = len(self._abierta)
        
        while not is_balanced:
            left_child = 2 * curr_idx + 1
            right_child = 2 * curr_idx + 2
            
            # Si no tiene hijos finalizamos
            if left_child >= length:
                is_balanced = True
            else:
                # Determinamos cuál de los hijos es el menor (el candidato a subir)
                # Asumimos que el izquierdo es el mejor inicialmente
                best_child_idx = left_child
                
                # Si existe el derecho Y es menor que el izquierdo, cambiamos al derecho
                if right_child < length and self._abierta[right_child][0] < self._abierta[left_child][0]:
                    best_child_idx = right_child
                
                # Comparamos el padre (nodo actual) con el hijo menor
                if self._abierta[best_child_idx][0] < self._abierta[curr_idx][0]:
                    # Guardamos el nodo actual
                    curr_node = self._abierta[curr_idx]

                    # Intercambiamos el hijo
                    self._abierta[curr_idx] = self._abierta[best_child_idx]

                    # Intercambiamos el padre
                    self._abierta[best_child_idx] = curr_node
                    
                    # Guardamos el índice del hijo como nodo actual
                    curr_idx = best_child_idx
                else:
                    # El padre es menor que los hijos: el orden es correcto
                    is_balanced = True
            
        
import heapq

'''
Wrapper del Árbol Binario que implementa heapq
'''
class Abierta:
    def __init__(self) -> None:
        self._abierta = []

    def add(self, cost: int, node: int) -> None:
        heapq.heappush(self._abierta, (cost, node))

    def get_best(self) -> tuple:
        return heapq.heappop(self._abierta)

    def is_empty(self) -> bool:
        return len(self._abierta) == 0
    
    def reset(self) -> None:
        self._abierta = []
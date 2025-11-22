class Cerrada:
    def __init__(self) -> None:
        self._cerrada = set()

    def add(self, node: int) -> None:
        self._cerrada.add(node)

    def contains(self, node: int) -> bool:
        return node in self._cerrada
    
    def reset(self) -> None:
        self._cerrada = set()
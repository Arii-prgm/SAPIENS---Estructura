from collections import deque

class ColaTareas:
    # Estructura de datos tipo Cola (FIFO - First In, First Out)
    def __init__(self):
        self.elementos = deque()

    @property
    def tamaño(self):
        # Retorna el tamaño de la cola
        return len(self.elementos)

    def enqueue(self, dato):
        # Inserta un elemento al final de la cola
        self.elementos.append(dato)

    def dequeue(self):
        # Retira y retorna el primer elemento de la cola
        if self.esta_vacia():
            return None
        return self.elementos.popleft()

    def peek(self):
        # Retorna el primer elemento de la cola sin retirarlo
        if self.esta_vacia():
            return None
        return self.elementos[0]

    def esta_vacia(self):
        # Verifica si la cola está vacía
        return len(self.elementos) == 0

    def obtener_elementos(self):
        # Recorre la cola sin modificarla y retorna sus elementos como lista
        elementos_dict = []
        for dato in self.elementos:
            if hasattr(dato, 'to_dict'):
                elementos_dict.append(dato.to_dict())
            else:
                elementos_dict.append(dato)
        return elementos_dict

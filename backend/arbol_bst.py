class NodoArbol:
    # Nodo para una estructura de datos de tipo Árbol Binario
    def __init__(self, dato):
        self.dato = dato 
        self.izquierdo = None
        self.derecho = None

class ArbolMaterias:
    # Estructura de datos tipo Árbol Binario de Búsqueda (BST - Binary Search Tree) para organizar materias por código
    def __init__(self):
        self.raiz = None

    def insertar(self, dato):
        # Inserta una nueva materia en el árbol binario de búsqueda
        if self.raiz is None:
            self.raiz = NodoArbol(dato)
        else:
            self._insertar_recursivo(self.raiz, dato)

    def _insertar_recursivo(self, nodo_actual, dato):
        # Método auxiliar recursivo para ubicar e insertar la materia según su código
        if dato.codigo < nodo_actual.dato.codigo:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = NodoArbol(dato)
            else:
                self._insertar_recursivo(nodo_actual.izquierdo, dato)
        elif dato.codigo > nodo_actual.dato.codigo:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = NodoArbol(dato)
            else:
                self._insertar_recursivo(nodo_actual.derecho, dato)
        else:
            pass

    def buscar_por_codigo(self, codigo):
        # Busca una materia en el árbol por su código
        codigo_buscado = str(codigo).upper()
        return self._buscar_recursivo(self.raiz, codigo_buscado)

    def _buscar_recursivo(self, nodo_actual, codigo):
        # Método auxiliar recursivo que realiza la búsqueda binaria en el árbol
        if nodo_actual is None:
            return None
        
        if codigo == nodo_actual.dato.codigo:
            return nodo_actual.dato
        elif codigo < nodo_actual.dato.codigo:
            return self._buscar_recursivo(nodo_actual.izquierdo, codigo)
        else:
            return self._buscar_recursivo(nodo_actual.derecho, codigo)

    def recorrido_inorden(self):
        # Retorna los elementos del árbol ordenados de forma ascendente (Inorden)
        elementos = []
        self._inorden_recursivo(self.raiz, elementos)
        return elementos

    def _inorden_recursivo(self, nodo_actual, lista):
        # Método auxiliar recursivo para el recorrido inorden del árbol
        if nodo_actual is not None:
            self._inorden_recursivo(nodo_actual.izquierdo, lista)
            if hasattr(nodo_actual.dato, 'to_dict'):
                lista.append(nodo_actual.dato.to_dict())
            else:
                lista.append(nodo_actual.dato)
            self._inorden_recursivo(nodo_actual.derecho, lista)

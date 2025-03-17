import csv

class Grafo:
    def __init__(self, nodos_file, edges_file):
        self.__nodos = self.build_nodes(nodos_file, edges_file)
    
    def build_nodes(self, nodos_file, edges_file):
        nodes = {}
        # Cargar nodos desde CSV con encabezados
        with open(nodos_file, 'r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                id_nodo = row['id']
                nombre_nodo = row['label']
                nodes[id_nodo] = Nodo(id_nodo, nombre_nodo)
        
        # Cargar aristas desde CSV con encabezados
        with open(edges_file, 'r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                id1 = row['source']
                id2 = row['target']
                if id1 in nodes and id2 in nodes:
                    nodes[id1].agregar_adyacente(nodes[id2])
                    nodes[id2].agregar_adyacente(nodes[id1])  # No dirigido
        
        return nodes

    def agregar_nodo(self, id, nombre):
        if id not in self.__nodos:
            self.__nodos[id] = Nodo(id, nombre)
    
    def eliminar_nodo(self, id):
        if id in self.__nodos:
            # Eliminar este nodo de la lista de adyacentes de otros nodos
            nodo_a_eliminar = self.__nodos[id]
            for nodo in self.__nodos.values():
                nodo.eliminar_adyacente(nodo_a_eliminar)
            # Eliminar el nodo del grafo
            del self.__nodos[id]

    def agregar_arista(self, id1, id2):
        if id1 in self.__nodos and id2 in self.__nodos:
            self.__nodos[id1].agregar_adyacente(self.__nodos[id2])
            self.__nodos[id2].agregar_adyacente(self.__nodos[id1])  # No dirigido
    
    def eliminar_arista(self, id1, id2):
        if id1 in self.__nodos and id2 in self.__nodos:
            self.__nodos[id1].eliminar_adyacente(self.__nodos[id2])
            self.__nodos[id2].eliminar_adyacente(self.__nodos[id1])
    
    # Getters
    def get_nodos(self):
        return self.__nodos
    
    def get_nodo(self, id):
        return self.__nodos.get(id)
    
    def get_num_nodos(self):
        return len(self.__nodos)
    
    def get_adyacentes(self, id):
        if id in self.__nodos:
            return self.__nodos[id].get_adyacentes()
        return set()
    
    def existe_nodo(self, id):
        return id in self.__nodos
    
    def existe_arista(self, id1, id2):
        if id1 in self.__nodos and id2 in self.__nodos:
            return self.__nodos[id2] in self.__nodos[id1].get_adyacentes()
        return False
    
    def buscar_nodo_por_nombre(self, nombre):
        for nodo in self.__nodos.values():
            if nodo.get_nombre() == nombre:
                return nodo
        return None


class Nodo:
    def __init__(self, id, nombre):
        self.__id = id
        self.__nombre = nombre
        self.__adyacentes = set()

    def agregar_adyacente(self, nodo):
        self.__adyacentes.add(nodo)
    
    def eliminar_adyacente(self, nodo):
        if nodo in self.__adyacentes:
            self.__adyacentes.remove(nodo)
    
    # Getters
    def get_id(self):
        return self.__id
    
    def get_nombre(self):
        return self.__nombre
    
    def get_adyacentes(self):
        return self.__adyacentes
    
    def get_num_adyacentes(self):
        return len(self.__adyacentes)
    
    # Setters
    def set_nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre
    
    # Para poder usar el nodo como clave en conjuntos y diccionarios
    def __hash__(self):
        return hash(self.__id)
    
    def __eq__(self, otro):
        if not isinstance(otro, Nodo):
            return False
        return self.__id == otro.get_id()
    
    def __str__(self):
        return f"Nodo(id={self.__id}, nombre={self.__nombre}, adyacentes={len(self.__adyacentes)})"



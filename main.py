from src.data_collection.spotify_api import SpotifyClient
from src.data_collection.data_scraper import DataScraper
from src.utils.config import nodes_path,edges_path
from src.data_processing.graph_builder import Grafo

def crear_grafo(max_artist,max_deep,name_artist="Melendi"):
    spotify = SpotifyClient()
    scrapper = DataScraper(spotify,max_artist,max_deep)
    scrapper.search_collaborator_deep(name_artist)


def probar_grafo():
    # Construir el grafo a partir de los archivos CSV
    grafo = Grafo(nodes_path, edges_path)
    
    # Imprimir información básica del grafo
    print(f"Grafo creado con éxito. Contiene {grafo.get_num_nodos()} nodos.")
    
    # Mostrar algunos nodos de ejemplo (primeros 5)
    print("\nAlgunos nodos de ejemplo:")
    for i, (id_nodo, nodo) in enumerate(list(grafo.get_nodos().items())[:5]):
        print(f"Nodo {i+1}: ID={nodo.get_id()}, Nombre={nodo.get_nombre()}, Conexiones={nodo.get_num_adyacentes()}")
    
    # Buscar un nodo específico (por ejemplo, el artista inicial)
    artista_inicial = "Carlos Vives"
    nodo_artista = grafo.buscar_nodo_por_nombre(artista_inicial)
    
    if nodo_artista:
        print(f"\nInformación del artista inicial ({artista_inicial}):")
        print(f"ID: {nodo_artista.get_id()}")
        print(f"Número de colaboradores: {nodo_artista.get_num_adyacentes()}")
        
        # Mostrar algunos colaboradores
        print("\nAlgunos colaboradores:")
        for i, colaborador in enumerate(list(nodo_artista.get_adyacentes())[:3]):
            print(f"  {i+1}. {colaborador.get_nombre()}")
    else:
        print(f"\nNo se encontró al artista {artista_inicial} en el grafo.")
    
    # Demostrar otras funcionalidades
    print("\n--- DEMOSTRANDO OTRAS FUNCIONALIDADES ---")
    
    # Verificar si existe un nodo
    if nodo_artista:
        id_artista = nodo_artista.get_id()
        print(f"¿Existe el nodo con ID {id_artista}? {grafo.existe_nodo(id_artista)}")
        
        # Verificar si existe una arista
        if nodo_artista.get_num_adyacentes() > 0:
            colaborador = next(iter(nodo_artista.get_adyacentes()))
            id_colaborador = colaborador.get_id()
            print(f"¿Existe arista entre {artista_inicial} y {colaborador.get_nombre()}? {grafo.existe_arista(id_artista, id_colaborador)}")
            
            # Probar eliminar y volver a agregar una arista
            print(f"Eliminando arista entre {artista_inicial} y {colaborador.get_nombre()}...")
            grafo.eliminar_arista(id_artista, id_colaborador)
            print(f"¿Existe arista después de eliminarla? {grafo.existe_arista(id_artista, id_colaborador)}")
            
            print(f"Volviendo a agregar la arista...")
            grafo.agregar_arista(id_artista, id_colaborador)
            print(f"¿Existe arista después de agregarla? {grafo.existe_arista(id_artista, id_colaborador)}")


if __name__ == "__main__":
    print("\n--- PRUEBA DE CONSTRUCCIÓN DEL GRAFO ---")
    probar_grafo()

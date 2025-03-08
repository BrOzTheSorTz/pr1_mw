import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import defaultdict


class NetworkAnalyzer:
    """
    Clase para analizar métricas de redes sociales basadas en grafos
    """

    def __init__(self, nodes_file, edges_file):
        """
        Inicializa el analizador de red

        Args:
            nodes_file (str): Ruta al archivo CSV con los nodos
            edges_file (str): Ruta al archivo CSV con las aristas
        """
        self.nodes_file = nodes_file
        self.edges_file = edges_file
        self.graph = None
        self.metrics = {}
        self.communities = None

    def load_graph(self):
        """
        Carga los datos de nodos y aristas para crear un grafo no dirigido
        """
        try:
            # Cargar nodos
            nodes_df = pd.read_csv(self.nodes_file)
            # Cargar aristas
            edges_df = pd.read_csv(self.edges_file)

            # Crear grafo no dirigido
            G = nx.Graph()

            # Añadir nodos con atributos
            for _, row in nodes_df.iterrows():
                attributes = {col: row[col] for col in nodes_df.columns if col != 'id'}
                G.add_node(row['id'], **attributes)

            # Añadir aristas
            for _, row in edges_df.iterrows():
                G.add_edge(row['source'], row['target'])

            self.graph = G
            print(f"Grafo cargado con éxito: {len(G.nodes)} nodos y {len(G.edges)} aristas")
            return True
        except Exception as e:
            print(f"Error al cargar el grafo: {e}")
            return False

    def calculate_basic_metrics(self):
        """
        Calcula métricas básicas del grafo: orden, tamaño y densidad
        """
        if not self.graph:
            print("El grafo no está cargado. Ejecute load_graph() primero.")
            return

        # Calcular métricas básicas
        order = len(self.graph.nodes)
        size = len(self.graph.edges)
        density = nx.density(self.graph)

        # Componentes conectados
        components = list(nx.connected_components(self.graph))
        largest_component = max(components, key=len)
        giant_component_size = len(largest_component)
        giant_component_ratio = giant_component_size / order

        # Grado medio y distribución
        degree_dict = dict(self.graph.degree())
        avg_degree = sum(degree_dict.values()) / order

        self.metrics['basic'] = {
            'order': order,
            'size': size,
            'density': density,
            'connected_components': len(components),
            'giant_component_size': giant_component_size,
            'giant_component_ratio': giant_component_ratio,
            'average_degree': avg_degree
        }

        return self.metrics['basic']

    def calculate_centrality(self):
        """
        Calcula medidas de centralidad: grado, cercanía e intermediación
        """
        if not self.graph:
            print("El grafo no está cargado. Ejecute load_graph() primero.")
            return

        # Centralidad de grado
        degree_centrality = nx.degree_centrality(self.graph)

        # Centralidad de cercanía
        # Usamos la versión que maneja grafos desconectados
        closeness_centrality = nx.closeness_centrality(self.graph)

        # Centralidad de intermediación
        betweenness_centrality = nx.betweenness_centrality(self.graph)

        self.metrics['centrality'] = {
            'degree': degree_centrality,
            'closeness': closeness_centrality,
            'betweenness': betweenness_centrality
        }

        return self.metrics['centrality']

    def calculate_pagerank(self):
        """
        Calcula el PageRank para todos los nodos del grafo
        """
        if not self.graph:
            print("El grafo no está cargado. Ejecute load_graph() primero.")
            return

        # Calcular PageRank con factor de amortiguación de 0.85
        pagerank = nx.pagerank(self.graph, alpha=0.85)

        self.metrics['pagerank'] = pagerank
        return pagerank

    def calculate_hits(self):
        """
        Calcula el algoritmo HITS (hub y authority) para todos los nodos
        """
        if not self.graph:
            print("El grafo no está cargado. Ejecute load_graph() primero.")
            return

        # Calcular HITS
        hubs, authorities = nx.hits(self.graph, max_iter=100)

        self.metrics['hits'] = {
            'hubs': hubs,
            'authorities': authorities
        }

        return self.metrics['hits']

    def calculate_eccentricity(self):
        """
        Calcula la excentricidad y el diámetro del grafo
        Nota: Solo funciona para grafos conexos
        """
        if not self.graph:
            print("El grafo no está cargado. Ejecute load_graph() primero.")
            return

        # Obtener el componente gigante (el más grande)
        components = list(nx.connected_components(self.graph))
        giant_component = max(components, key=len)
        giant_graph = self.graph.subgraph(giant_component)

        # Calcular excentricidad para cada nodo en el componente gigante
        eccentricity = nx.eccentricity(giant_graph)

        # Calcular diámetro (máximo de las excentricidades)
        diameter = nx.diameter(giant_graph)

        # Calcular radio (mínimo de las excentricidades)
        radius = nx.radius(giant_graph)

        self.metrics['eccentricity'] = {
            'node_eccentricity': eccentricity,
            'diameter': diameter,
            'radius': radius
        }

        return self.metrics['eccentricity']

    def detect_communities(self, algorithm='louvain'):
        """
        Detecta comunidades en el grafo

        Args:
            algorithm (str): Algoritmo a usar ('louvain', 'modularity')
        """
        if not self.graph:
            print("El grafo no está cargado. Ejecute load_graph() primero.")
            return

        community_detection = None

        if algorithm == 'louvain':
            try:
                from community import best_partition
                community_detection = best_partition(self.graph)
            except ImportError:
                print("Método Louvain no disponible. Instale python-louvain.")
                # Usar alternativa
                community_detection = self._greedy_modularity_communities()
        else:
            # Usar la función integrada de NetworkX para communidades basadas en modularidad
            community_detection = self._greedy_modularity_communities()

        self.communities = community_detection

        # Calcular número de comunidades y tamaño de cada una
        if isinstance(community_detection, dict):
            # Para Louvain que devuelve un diccionario
            community_sizes = defaultdict(int)
            for _, community_id in community_detection.items():
                community_sizes[community_id] += 1

            num_communities = len(community_sizes)
            avg_community_size = sum(community_sizes.values()) / num_communities

            self.metrics['communities'] = {
                'algorithm': algorithm,
                'num_communities': num_communities,
                'community_sizes': dict(community_sizes),
                'avg_community_size': avg_community_size,
                'community_assignment': community_detection
            }
        else:
            # Para otros algoritmos que devuelven listas de conjuntos
            community_sizes = [len(community) for community in community_detection]

            self.metrics['communities'] = {
                'algorithm': algorithm,
                'num_communities': len(community_sizes),
                'community_sizes': community_sizes,
                'avg_community_size': sum(community_sizes) / len(community_sizes),
                'community_assignment': community_detection
            }

        return self.metrics['communities']

    def _greedy_modularity_communities(self):
        """
        Implementa el algoritmo de detección de comunidades basado en modularidad
        """
        communities = list(nx.community.greedy_modularity_communities(self.graph))

        # Convertir el resultado a un diccionario {nodo: comunidad_id}
        community_dict = {}
        for i, community in enumerate(communities):
            for node in community:
                community_dict[node] = i

        return community_dict

    def calculate_all_metrics(self):
        """
        Calcula todas las métricas disponibles
        """
        self.calculate_basic_metrics()
        self.calculate_centrality()
        self.calculate_pagerank()
        self.calculate_hits()

        try:
            self.calculate_eccentricity()
        except nx.NetworkXError as e:
            print(f"No se pudo calcular la excentricidad: {e}")
            print("Esto es normal si el grafo no es completamente conexo.")

        self.detect_communities()

        return self.metrics

    def export_metrics(self, output_dir='data/metrics'):
        """
        Exporta las métricas calculadas a archivos CSV

        Args:
            output_dir (str): Directorio donde se guardarán los archivos
        """
        if not self.metrics:
            print("No hay métricas para exportar. Ejecute calculate_all_metrics() primero.")
            return

        # Crear directorio si no existe
        os.makedirs(output_dir, exist_ok=True)

        # Exportar métricas básicas
        if 'basic' in self.metrics:
            pd.DataFrame([self.metrics['basic']]).to_csv(f"{output_dir}/basic_metrics.csv", index=False)

        # Exportar centralidades
        if 'centrality' in self.metrics:
            # Unir todas las medidas de centralidad
            centrality_df = pd.DataFrame({
                'node': list(self.metrics['centrality']['degree'].keys()),
                'degree_centrality': list(self.metrics['centrality']['degree'].values()),
                'closeness_centrality': list(self.metrics['centrality']['closeness'].values()),
                'betweenness_centrality': list(self.metrics['centrality']['betweenness'].values())
            })

            # Añadir nombres de nodos si están disponibles
            if self.graph and 'label' in self.graph.nodes[list(self.graph.nodes)[0]]:
                node_labels = {node: data.get('label', node) for node, data in self.graph.nodes(data=True)}
                centrality_df['name'] = centrality_df['node'].map(node_labels)
                # Reordenar columnas
                centrality_df = centrality_df[
                    ['node', 'name', 'degree_centrality', 'closeness_centrality', 'betweenness_centrality']]

            centrality_df.to_csv(f"{output_dir}/centrality_metrics.csv", index=False)

        # Exportar PageRank
        if 'pagerank' in self.metrics:
            pagerank_df = pd.DataFrame({
                'node': list(self.metrics['pagerank'].keys()),
                'pagerank': list(self.metrics['pagerank'].values())
            })

            # Añadir nombres de nodos si están disponibles
            if self.graph and 'label' in self.graph.nodes[list(self.graph.nodes)[0]]:
                node_labels = {node: data.get('label', node) for node, data in self.graph.nodes(data=True)}
                pagerank_df['name'] = pagerank_df['node'].map(node_labels)
                # Reordenar columnas
                pagerank_df = pagerank_df[['node', 'name', 'pagerank']]

            pagerank_df.to_csv(f"{output_dir}/pagerank_metrics.csv", index=False)

        # Exportar HITS
        if 'hits' in self.metrics:
            hits_df = pd.DataFrame({
                'node': list(self.metrics['hits']['hubs'].keys()),
                'hub_score': list(self.metrics['hits']['hubs'].values()),
                'authority_score': list(self.metrics['hits']['authorities'].values())
            })

            # Añadir nombres de nodos si están disponibles
            if self.graph and 'label' in self.graph.nodes[list(self.graph.nodes)[0]]:
                node_labels = {node: data.get('label', node) for node, data in self.graph.nodes(data=True)}
                hits_df['name'] = hits_df['node'].map(node_labels)
                # Reordenar columnas
                hits_df = hits_df[['node', 'name', 'hub_score', 'authority_score']]

            hits_df.to_csv(f"{output_dir}/hits_metrics.csv", index=False)

        # Exportar excentricidad
        if 'eccentricity' in self.metrics and 'node_eccentricity' in self.metrics['eccentricity']:
            ecc_df = pd.DataFrame({
                'node': list(self.metrics['eccentricity']['node_eccentricity'].keys()),
                'eccentricity': list(self.metrics['eccentricity']['node_eccentricity'].values())
            })

            # Añadir nombres de nodos si están disponibles
            if self.graph and 'label' in self.graph.nodes[list(self.graph.nodes)[0]]:
                node_labels = {node: data.get('label', node) for node, data in self.graph.nodes(data=True)}
                ecc_df['name'] = ecc_df['node'].map(node_labels)
                # Reordenar columnas
                ecc_df = ecc_df[['node', 'name', 'eccentricity']]

            ecc_df.to_csv(f"{output_dir}/eccentricity_metrics.csv", index=False)

            # Exportar diámetro y radio
            diameter_radius = {
                'diameter': self.metrics['eccentricity']['diameter'],
                'radius': self.metrics['eccentricity']['radius']
            }
            pd.DataFrame([diameter_radius]).to_csv(f"{output_dir}/diameter_radius.csv", index=False)

        # Exportar comunidades
        if 'communities' in self.metrics and 'community_assignment' in self.metrics['communities']:
            if isinstance(self.metrics['communities']['community_assignment'], dict):
                comm_df = pd.DataFrame({
                    'node': list(self.metrics['communities']['community_assignment'].keys()),
                    'community_id': list(self.metrics['communities']['community_assignment'].values())
                })

                # Añadir nombres de nodos si están disponibles
                if self.graph and 'label' in self.graph.nodes[list(self.graph.nodes)[0]]:
                    node_labels = {node: data.get('label', node) for node, data in self.graph.nodes(data=True)}
                    comm_df['name'] = comm_df['node'].map(node_labels)
                    # Reordenar columnas
                    comm_df = comm_df[['node', 'name', 'community_id']]

                comm_df.to_csv(f"{output_dir}/communities.csv", index=False)

                # Exportar estadísticas de comunidades
                comm_stats = {
                    'algorithm': self.metrics['communities']['algorithm'],
                    'num_communities': self.metrics['communities']['num_communities'],
                    'avg_community_size': self.metrics['communities']['avg_community_size']
                }
                pd.DataFrame([comm_stats]).to_csv(f"{output_dir}/community_stats.csv", index=False)

                # Exportar tamaños de comunidades
                comm_sizes = {
                    'community_id': list(self.metrics['communities']['community_sizes'].keys()),
                    'size': list(self.metrics['communities']['community_sizes'].values())
                }
                pd.DataFrame(comm_sizes).to_csv(f"{output_dir}/community_sizes.csv", index=False)

        print(f"Métricas exportadas a {output_dir}/")

    def generate_summary(self, top_n=10):
        """
        Genera un resumen con las métricas más relevantes

        Args:
            top_n (int): Número de nodos top a mostrar en cada categoría
        """
        if not self.metrics:
            print("No hay métricas para generar el resumen. Ejecute calculate_all_metrics() primero.")
            return

        summary = {}

        # Métricas básicas
        if 'basic' in self.metrics:
            summary['basic'] = self.metrics['basic']

        # Top por centralidad de grado
        if 'centrality' in self.metrics and 'degree' in self.metrics['centrality']:
            degree_top = sorted(self.metrics['centrality']['degree'].items(), key=lambda x: x[1], reverse=True)[:top_n]

            # Convertir IDs a nombres si están disponibles
            if self.graph and 'label' in self.graph.nodes[list(self.graph.nodes)[0]]:
                node_labels = {node: data.get('label', node) for node, data in self.graph.nodes(data=True)}
                degree_top = [(node_labels.get(node, node), value) for node, value in degree_top]

            summary['top_degree_centrality'] = degree_top

        # Top por centralidad de intermediación
        if 'centrality' in self.metrics and 'betweenness' in self.metrics['centrality']:
            betweenness_top = sorted(self.metrics['centrality']['betweenness'].items(), key=lambda x: x[1],
                                     reverse=True)[:top_n]

            # Convertir IDs a nombres si están disponibles
            if self.graph and 'label' in self.graph.nodes[list(self.graph.nodes)[0]]:
                node_labels = {node: data.get('label', node) for node, data in self.graph.nodes(data=True)}
                betweenness_top = [(node_labels.get(node, node), value) for node, value in betweenness_top]

            summary['top_betweenness_centrality'] = betweenness_top

        # Top por PageRank
        if 'pagerank' in self.metrics:
            pagerank_top = sorted(self.metrics['pagerank'].items(), key=lambda x: x[1], reverse=True)[:top_n]

            # Convertir IDs a nombres si están disponibles
            if self.graph and 'label' in self.graph.nodes[list(self.graph.nodes)[0]]:
                node_labels = {node: data.get('label', node) for node, data in self.graph.nodes(data=True)}
                pagerank_top = [(node_labels.get(node, node), value) for node, value in pagerank_top]

            summary['top_pagerank'] = pagerank_top

        # Top por score de Hub
        if 'hits' in self.metrics and 'hubs' in self.metrics['hits']:
            hubs_top = sorted(self.metrics['hits']['hubs'].items(), key=lambda x: x[1], reverse=True)[:top_n]

            # Convertir IDs a nombres si están disponibles
            if self.graph and 'label' in self.graph.nodes[list(self.graph.nodes)[0]]:
                node_labels = {node: data.get('label', node) for node, data in self.graph.nodes(data=True)}
                hubs_top = [(node_labels.get(node, node), value) for node, value in hubs_top]

            summary['top_hubs'] = hubs_top

        # Top por score de Authority
        if 'hits' in self.metrics and 'authorities' in self.metrics['hits']:
            authorities_top = sorted(self.metrics['hits']['authorities'].items(), key=lambda x: x[1], reverse=True)[
                              :top_n]

            # Convertir IDs a nombres si están disponibles
            if self.graph and 'label' in self.graph.nodes[list(self.graph.nodes)[0]]:
                node_labels = {node: data.get('label', node) for node, data in self.graph.nodes(data=True)}
                authorities_top = [(node_labels.get(node, node), value) for node, value in authorities_top]

            summary['top_authorities'] = authorities_top

        # Información de diámetro y radio
        if 'eccentricity' in self.metrics:
            if 'diameter' in self.metrics['eccentricity']:
                summary['diameter'] = self.metrics['eccentricity']['diameter']
            if 'radius' in self.metrics['eccentricity']:
                summary['radius'] = self.metrics['eccentricity']['radius']

        # Información de comunidades
        if 'communities' in self.metrics:
            summary['communities'] = {
                'algorithm': self.metrics['communities'].get('algorithm'),
                'num_communities': self.metrics['communities'].get('num_communities'),
                'avg_community_size': self.metrics['communities'].get('avg_community_size')
            }

            # Top comunidades por tamaño
            if 'community_sizes' in self.metrics['communities']:
                if isinstance(self.metrics['communities']['community_sizes'], dict):
                    top_communities = sorted(self.metrics['communities']['community_sizes'].items(),
                                             key=lambda x: x[1], reverse=True)[:top_n]
                    summary['top_communities_by_size'] = top_communities

        return summary

    def print_summary(self, top_n=10):
        """
        Imprime un resumen de las métricas en formato legible

        Args:
            top_n (int): Número de nodos top a mostrar en cada categoría
        """
        summary = self.generate_summary(top_n)

        print("\n" + "=" * 50)
        print("RESUMEN DE ANÁLISIS DE RED")
        print("=" * 50)

        # Métricas básicas
        if 'basic' in summary:
            print("\nMÉTRICAS BÁSICAS:")
            print(f"- Número de nodos (orden): {summary['basic']['order']}")
            print(f"- Número de aristas (tamaño): {summary['basic']['size']}")
            print(f"- Densidad del grafo: {summary['basic']['density']:.6f}")
            print(f"- Número de componentes conectados: {summary['basic']['connected_components']}")
            print(f"- Tamaño del componente gigante: {summary['basic']['giant_component_size']} nodos "
                  f"({summary['basic']['giant_component_ratio'] * 100:.2f}% del total)")
            print(f"- Grado medio: {summary['basic']['average_degree']:.2f}")

        # Top por centralidad de grado
        if 'top_degree_centrality' in summary:
            print("\nARTISTAS CON MAYOR CENTRALIDAD DE GRADO:")
            for i, (node, value) in enumerate(summary['top_degree_centrality'], 1):
                print(f"{i}. {node}: {value:.4f}")

        # Top por centralidad de intermediación
        if 'top_betweenness_centrality' in summary:
            print("\nARTISTAS CON MAYOR CENTRALIDAD DE INTERMEDIACIÓN:")
            for i, (node, value) in enumerate(summary['top_betweenness_centrality'], 1):
                print(f"{i}. {node}: {value:.4f}")

        # Top por PageRank
        if 'top_pagerank' in summary:
            print("\nARTISTAS CON MAYOR PAGERANK:")
            for i, (node, value) in enumerate(summary['top_pagerank'], 1):
                print(f"{i}. {node}: {value:.6f}")

        # Top por score de Hub
        if 'top_hubs' in summary:
            print("\nMEJORES HUBS (ARTISTAS QUE COLABORAN CON MUCHOS OTROS):")
            for i, (node, value) in enumerate(summary['top_hubs'], 1):
                print(f"{i}. {node}: {value:.6f}")

        # Top por score de Authority
        if 'top_authorities' in summary:
            print("\nMEJORES AUTORIDADES (ARTISTAS CON LOS QUE MUCHOS QUIEREN COLABORAR):")
            for i, (node, value) in enumerate(summary['top_authorities'], 1):
                print(f"{i}. {node}: {value:.6f}")

        # Información de diámetro y radio
        if 'diameter' in summary or 'radius' in summary:
            print("\nEXCENTRICIDAD DE LA RED:")
            if 'diameter' in summary:
                print(f"- Diámetro: {summary['diameter']}")
            if 'radius' in summary:
                print(f"- Radio: {summary['radius']}")

        # Información de comunidades
        if 'communities' in summary:
            print("\nDETECCIÓN DE COMUNIDADES:")
            print(f"- Algoritmo utilizado: {summary['communities']['algorithm']}")
            print(f"- Número de comunidades: {summary['communities']['num_communities']}")
            print(f"- Tamaño medio de comunidad: {summary['communities']['avg_community_size']:.2f} nodos")

            if 'top_communities_by_size' in summary:
                print("\nCOMUNIDADES MÁS GRANDES:")
                for i, (comm_id, size) in enumerate(summary['top_communities_by_size'], 1):
                    print(f"{i}. Comunidad {comm_id}: {size} nodos")

        print("\n" + "=" * 50)

    def create_comparison_table(self):
        """
        Crea una tabla comparativa de las diferentes métricas de centralidad, PageRank y HITS
        """
        if not self.metrics:
            print("No hay métricas para generar la tabla. Ejecute calculate_all_metrics() primero.")
            return

        # Inicializar DataFrame
        comparison_df = pd.DataFrame()

        # Añadir degree centrality
        if 'centrality' in self.metrics and 'degree' in self.metrics['centrality']:
            comparison_df['degree_centrality'] = pd.Series(self.metrics['centrality']['degree'])

        # Añadir closeness centrality
        if 'centrality' in self.metrics and 'closeness' in self.metrics['centrality']:
            comparison_df['closeness_centrality'] = pd.Series(self.metrics['centrality']['closeness'])

        # Añadir betweenness centrality
        if 'centrality' in self.metrics and 'betweenness' in self.metrics['centrality']:
            comparison_df['betweenness_centrality'] = pd.Series(self.metrics['centrality']['betweenness'])

        # Añadir PageRank
        if 'pagerank' in self.metrics:
            comparison_df['pagerank'] = pd.Series(self.metrics['pagerank'])

        # Añadir HITS
        if 'hits' in self.metrics:
            comparison_df['hub_score'] = pd.Series(self.metrics['hits']['hubs'])
            comparison_df['authority_score'] = pd.Series(self.metrics['hits']['authorities'])

        # Añadir ID del nodo como columna
        comparison_df['node'] = comparison_df.index

        # Añadir nombres de nodos si están disponibles
        if self.graph and 'label' in self.graph.nodes[list(self.graph.nodes)[0]]:
            node_labels = {node: data.get('label', node) for node, data in self.graph.nodes(data=True)}
            comparison_df['name'] = comparison_df['node'].map(node_labels)

            # Reordenar columnas para que node y name sean las primeras
            columns = ['node', 'name'] + [col for col in comparison_df.columns if col not in ['node', 'name']]
            comparison_df = comparison_df[columns]

        return comparison_df

    def export_comparison_table(self, output_file='data/metrics/metrics_comparison.csv'):
        """
        Exporta la tabla comparativa a un archivo CSV

        Args:
            output_file (str): Ruta del archivo de salida
        """
        comparison_df = self.create_comparison_table()

        # Crear directorio si no existe
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Exportar a CSV
        comparison_df.to_csv(output_file, index=False)
        print(f"Tabla comparativa exportada a {output_file}")

        return comparison_df
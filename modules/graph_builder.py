import networkx as nx
from pyvis.network import Network

LAMBDA_SIGN = 'λ'


def nodes_to_G(graph, G):
    for node in graph.keys():
        title = 'Смежные вершины:'
        if graph[node]:
            for edge in graph[node]:
                if f'\n{edge[1]}' not in title:
                    title += f'\n{edge[1]}'
        else:
            title += '\nотсутствуют'

        if node == LAMBDA_SIGN:
            value = 50
            shape = 'circle'
            G.add_node(f' {node} ', shape=shape, value=value, title=title)
        else:
            value = 10
            shape = 'box'
            G.add_node(node, shape=shape, value=value, title=title)


def edges_to_G(graph, G):
    for node in graph.keys():
        for edge in graph[node]:
            prefix = f' {node} ' if node == LAMBDA_SIGN else node
            postfix = f' {edge[1]} ' if edge[1] == LAMBDA_SIGN else edge[1]

            title = f'{prefix} + ({", ".join(edge[0])}) + {postfix} = {edge[2]}' if edge[0] \
                else f'{prefix} + {postfix} = {edge[2]}'

            G.add_edge(prefix, postfix, title=title)


def G_to_html(G, html_path):
    nt = Network(directed=True, cdn_resources='remote')
    nt.from_nx(G)
    nt.set_options("""
        var options = {
            "configure": {    
                "enabled": false
            },
            "nodes": {
                "scaling": {
                    "min": 10,
                    "max": 50,
                    "label": {
                        "enabled": true,
                        "min": 10,
                        "max": 50
                    }
                }
            },
            "edges": {
                "color": {
                    "inherit": true
                },
                "smooth": {
                    "enabled": true,
                    "type": "dynamic"
                }
            },
            "interaction": {
                "dragNodes": true,
                "hideEdgesOnDrag": false,
                "hideNodesOnDrag": false
            },
            "physics": {
                "enabled": true,
                "stabilization": {
                    "enabled": true,
                    "fit": true,
                    "iterations": 1000,
                    "onlyDynamicEdges": false,
                    "updateInterval": 50
                }
            }
        }
        """)
    nt.write_html(html_path)


def build_G(graph, html_path):
    G = nx.MultiDiGraph()
    nodes_to_G(graph, G)
    edges_to_G(graph, G)
    G_to_html(G, html_path)

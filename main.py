import os
import webbrowser

from modules import markov_algo as algo, html_editor as he, graph_builder as gb

GRAPH_PATH = os.path.join(os.getcwd(), 'graph.html')


def parse_input():
    codes = input('Введите коды через пробел: ').split()
    while len(codes) < 1 or len(set(codes)) < len(codes):
        print('Неверные входные данные!')
        codes = input('Введите коды через пробел: ').split()

    return codes


if __name__ == '__main__':
    codes = parse_input()

    graph, loop_decodings = algo.run(codes)
    gb.build_G(graph, GRAPH_PATH)
    he.make_changes(GRAPH_PATH, codes, graph, loop_decodings)

    webbrowser.open(GRAPH_PATH)

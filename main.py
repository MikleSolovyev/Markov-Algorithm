import os

from modules import markov_algo as algo, html_editor as he, graph_builder as gb

CODES_PATH = os.path.join(os.getcwd(), 'codes.txt')
GRAPHS_DIR_PATH = os.path.join(os.getcwd(), 'graphs')
GRAPH_PREFIX_NAME = 'graph'


def parse_input():
    codes_path = input(r'Введите путь до файла с кодами (пустой ввод - ./codes.txt): ')
    if not codes_path:
        codes_path = CODES_PATH
    while not os.path.exists(codes_path):
        print('Нету файла по такому пути!')
        codes_path = input(r'Введите путь до файла с кодами (пустой ввод - ./codes.txt): ')
        if not codes_path:
            codes_path = CODES_PATH

    return codes_path


if __name__ == '__main__':
    codes_path = parse_input()

    if not os.path.exists(GRAPHS_DIR_PATH):
        os.mkdir(GRAPHS_DIR_PATH)

    with open(codes_path, 'r') as file:
        line_index = 0
        for line in file:
            line_index += 1

            codes = line.split()
            if len(codes) < 1 or len(set(codes)) < len(codes):
                print(f'Строка с кодами под номером {line_index} содержит неправильную последовательность кодов!')
                continue

            graph_path = os.path.join(GRAPHS_DIR_PATH, f'{GRAPH_PREFIX_NAME}_{line_index}.html')
            graph, loop_decodings = algo.run(codes)
            gb.build_G(graph, graph_path)
            he.make_changes(graph_path, codes, graph, loop_decodings)

LAMBDA_SIGN = 'λ'


def find_nodes(codes):
    begins = set()
    ends = set()

    # находим все начала и концы кодов, не являющиеся кодами
    for i in range(len(codes)):
        for j in range(1, len(codes[i])):
            node_begin = codes[i][:j]
            if node_begin not in codes:
                begins.add(node_begin)

            node_end = codes[i][-j:]
            if node_end not in codes:
                ends.add(node_end)

    # находим вершины графа - пересечения множеств начал и концов кодов
    graph = dict.fromkeys([LAMBDA_SIGN] + list(begins.intersection(ends)))

    return graph


def find_edges(codes, graph, max_len):
    # рекурсивный перебор всех последовательностей вида префикс-код1-код2-...-постфикс
    def recursive_enum(prefix, middle, postfix):
        seq = f'{prefix}{"".join(middle)}{postfix}'.replace(LAMBDA_SIGN, '')

        if len(seq) > max_len:
            return

        if seq in codes and not (prefix == LAMBDA_SIGN and len(middle) == 1 and postfix == LAMBDA_SIGN):
            graph[prefix].append([middle, postfix, seq])

        for code in codes:
            new_middle = middle[:]
            new_middle.append(code)
            recursive_enum(prefix, new_middle, postfix)

    for prefix in graph.keys():
        graph[prefix] = []
        for postfix in graph.keys():
            recursive_enum(prefix, [], postfix)


def find_lambda_loops(graph):
    # поиск в глубину
    def dfs(node, path):
        if path and node == LAMBDA_SIGN:
            lambda_loops.append(path[:])
            return

        if visited.get(node, False):
            return

        visited[node] = True
        next_node_list = graph[node]
        for next_node in next_node_list:
            path.append(next_node)
            dfs(next_node[1], path)
            path.pop()

        visited[node] = False

    lambda_loops = []
    visited = {}
    dfs(LAMBDA_SIGN, [])

    return lambda_loops


def find_loop_decodings(lambda_loops):
    loop_decodings = {}

    for loop in lambda_loops:
        loop_nodes = [LAMBDA_SIGN]
        decode1 = ''
        decode2 = ''

        for i in range(len(loop)):
            loop_nodes.append(loop[i][1])

            if i % 2 == 0:
                for code in loop[i][0]:
                    decode1 += f'({code})'
                decode2 += f'({loop[i][2]})'
            else:
                for code in loop[i][0]:
                    decode2 += f'({code})'
                decode1 += f'({loop[i][2]})'

        loop_decodings[tuple(loop_nodes)] = [decode1, decode2]

    return loop_decodings


def run(codes):
    # находим все узлы графа
    graph = find_nodes(codes)

    max_len = len(max(codes, key=len))
    # находим все дуги графа
    find_edges(codes, graph, max_len)

    # находим все циклы через вершину λ
    lambda_loops = find_lambda_loops(graph)

    # находим неоднозначно декодируемые кодовые последовательности
    loop_decodings = find_loop_decodings(lambda_loops)

    return graph, loop_decodings

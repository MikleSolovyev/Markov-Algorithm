from bs4 import BeautifulSoup


def delete_tags(soup):
    for tag in soup.select('center'):
        tag.decompose()

    soup.find('div', attrs={'style': 'width: 100%'}).unwrap()


def change_styles(soup):
    style_attr = soup.find('style', attrs={'type': 'text/css'})
    style_attr.string = '''#mynetwork {
                 width: 70%;
                 height: 90%;
                 background-color: #ffffff;
                 border: 1px solid lightgray;
                 position: fixed;
                 left: 0;
                 bottom: 0;
                 margin: 0;
                 padding: 0;
             }'''


def results_to_html(codes, graph, loop_decodings):
    codes = ', '.join(codes)
    nodes = ', '.join(graph.keys())
    all_loops = []

    if loop_decodings:
        for loop in loop_decodings.keys():
            all_loops.append(f'<h5>{" -> ".join(loop)}:</h5>'
                             f'<p>{loop_decodings[loop][0].replace("(", "").replace(")", "")} = '
                             f'{loop_decodings[loop][0]} = '
                             f'{loop_decodings[loop][1]}</p>')

        all_loops = ''.join(all_loops)
        res = 'однозначно не декодируется'
    else:
        all_loops = "<p>отсутствуют</p>"
        res = 'однозначно декодируется'

    right_div = f'<div style="position: fixed; width: 30%; height: 90%; bottom: 0; right: 0; border: 1px solid lightgray; overflow: auto; text-align: center">' \
                f'<h3>Исходные коды:</h3>' \
                f'<p>{codes}</p>' \
                f'<h3>Вершины графа:</h3>' \
                f'<p>{nodes}</p>' \
                f'<h3>Ориентированные циклы через вершину λ:</h3>' \
                f'<div>{all_loops}</div>' \
                f'<h3>Вывод:</h3>' \
                f'<p>{res}</p>' \
                f'</div>'

    return right_div


def add_tags(soup, right_div):
    new_title = f'<title>Алгоритм Маркова</title>'
    soup.head.append(BeautifulSoup(new_title, 'html.parser'))

    top_div = f'<div style="position: fixed; width: 100%; height: 10%; top: 0; border: 1px solid lightgray; display: flex; align-items:center; justify-content:center">' \
              f'<h1>Алгоритм Маркова</h1>' \
              f'</div>'
    soup.body.insert(1, BeautifulSoup(top_div, 'html.parser'))

    header = f'<div style="position: fixed; top: 10%; left: 0">' \
             f'<h2 align="left">Граф:</h2>' \
             f'</div>'
    soup.body.append(BeautifulSoup(header, 'html.parser'))

    soup.body.insert(2, BeautifulSoup(right_div, 'html.parser'))


def make_changes(html_path, codes, graph, loop_decodings):
    with open(file=html_path, mode='r+', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        delete_tags(soup)
        change_styles(soup)
        right_div = results_to_html(codes, graph, loop_decodings)
        add_tags(soup, right_div)

        file.seek(0)
        file.truncate(0)
        file.write(str(soup.prettify()))

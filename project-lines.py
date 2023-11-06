def app():
    lines = [
        len(open('app.py', 'r').readlines()),
        len(open('config.py', 'r').readlines()),
        len(open('database.py', 'r').readlines()),
        len(open('markups.py', 'r').readlines()),
    ]
    lines.append(sum([i for i in lines]))
    print(
    """
    app.py lines ~ {0}
    config.py lines ~ {1}
    database.py lines ~ {2}
    markups.py lines ~ {3}

    Total lines ~ {4}
    """.format(*lines)
    )

def beta():
    lines = [
        len(open('beta.py', 'r').readlines()),
        len(open('config.py', 'r').readlines()),
        len(open('database.py', 'r').readlines()),
        len(open('markups.py', 'r').readlines()),
    ]
    lines.append(sum([i for i in lines]))
    print(
    """
    beta.py lines ~ {0}
    config.py lines ~ {1}
    database.py lines ~ {2}
    markups.py lines ~ {3}
    
    Total lines ~ {4}
    """.format(*lines)
    )


if __name__ == '__main__':
    app()
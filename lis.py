import operator as op


Symbol = str
List = list
Number = (int, float)


def tokenize(program):
    return program.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(program):
    return parse_tokens(tokenize(program))[0]


def close_bracket_index(tokens, index=0, opening=0, closing=0):
    if index != 0 and opening == closing:
        return index - 1

    if tokens[0] == '(':
        return close_bracket_index(tokens[1:], index=index+1, opening=opening+1, closing=closing)
    elif tokens[0] == ')':
        return close_bracket_index(tokens[1:], index=index+1, opening=opening, closing=closing+1)
    else:
        return close_bracket_index(tokens[1:], index=index+1, opening=opening, closing=closing)


def parse_tokens(tokens):
    if len(tokens) == 1:
        return [atom(tokens[0])]

    if tokens[0] == '(':
        close_index = close_bracket_index(tokens)
        first = [parse_tokens(tokens[1:close_index])]

        if (close_index + 1) == len(tokens):  # if no expressions left
            return first
        else:
            return first + parse_tokens(tokens[close_index+1:])
    else:
        return parse_tokens(tokens[:1]) + parse_tokens(tokens[1:])


def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token


env = {
    '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
    '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
    'abs': abs,
}


def run(x):
    if isinstance(x, Number):
        return x
    else:
        proc = env[x[0]]
        params = [run(p) for p in x[1:]]
        return proc(*params)

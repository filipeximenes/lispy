
def tokenize(program):
    return program.replace('(', ' ( ').replace(')', ' ) ').split()


def recursive_parse(program):
    return recursive_parse_tokens(tokenize(program))[0]


def close_bracket_index(tokens, index=0, opening=0, closing=0):
    if index != 0 and opening == closing:
        return index - 1

    if tokens[0] == '(':
        return close_bracket_index(tokens[1:], index=index+1, opening=opening+1, closing=closing)
    elif tokens[0] == ')':
        return close_bracket_index(tokens[1:], index=index+1, opening=opening, closing=closing+1)
    else:
        return close_bracket_index(tokens[1:], index=index+1, opening=opening, closing=closing)


def recursive_parse_tokens(tokens):
    if not tokens:
        return

    if len(tokens) == 1:
        return tokens

    if tokens[0] == '(':
        close_index = close_bracket_index(tokens)
        if len(tokens) > close_index:
            first = [recursive_parse_tokens(tokens[1:close_index])]
            second = recursive_parse_tokens(tokens[close_index+1:])
            if second:
                return first + second
            else:
                return first
        else:
            return [recursive_parse_tokens(tokens[1:close_index])]
    else:
        return recursive_parse_tokens(tokens[:1]) + recursive_parse_tokens(tokens[1:])

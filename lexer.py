from oper import *
from string import ascii_letters, digits, printable, whitespace
from typing import List, Literal

uanry_pm_preced = set(all_ops).difference(r_brackets).union([None])

id_chars = set(ascii_letters + digits + '_')
num_chars = set(digits + '.')
op_chars = set(r''.join([ops for ops in all_ops]))
ws_chars = set(whitespace + '\0')

states = {
    'id',
    'num', # number
    'ch', # number in ascii character
    'op', # operator
    'ws', # white space
    'end'
}

number_hex = '0x'
number_bin = '0b'
hex_chars = set(digits + 'ABCDEFabcdef')
bin_chars = set('01')

esc_table = {
    'a': '\a',
    'b': '\b',
    'n': '\n',
    'r': '\r',
    't': '\t',
    'v': '\v',
    '\\': '\\',
    '\'': '\''
}
esc_chars = set(esc_table)

token_types = {
    'id',
    'num', # number
    'op', # operator
}

class Token:
    def __init__(self, raw, tok_type: Literal['id', 'num', 'op']) -> None:
        self.raw = raw
        self.type = tok_type
    
    def __repr__(self) -> str:
        return f'T({self.type}:{repr(self.raw)})'

def parse_token(raw_str: str, is_debug=False) -> List[str]:
    is_comment = False
    ch_escaping = False
    st = 'ws'
    q = ''
    output: List[Token] = []
    raw_str = raw_str.strip() + '\0'
    for n, c in enumerate(raw_str):
        if is_debug:
            print(st, repr(c), sep='\t')
        
        if c == '#':
            is_comment = True
            st == 'ws'
        if is_comment:
            if c == '\n':
                is_comment = False
            continue
        
        if st == 'ws':
            if c in ws_chars:
                pass
            elif c in num_chars:
                st = 'num'
                q = c
            elif c == '\'':
                st = 'ch'
                q = ''
            elif c in id_chars:
                st = 'id'
                q = c
            elif c in op_chars:
                st = 'op'
                last = output[-1] if len(output) else None
                # handle unary + -
                if (c == '-' or c == '+') and last.raw in uanry_pm_preced:
                    q = '!' + c
                # handle function call
                elif (c == '('
                        and (last.type != 'op' or last.raw in r_brackets)):
                    q = function_call_l_parenth
                elif c == ')' and last.raw == '$(':
                    # add the inferred null
                    output.append(Token('null', 'id'))
                    q = c
                else:
                    q = c

        elif st == 'id':
            if c in ws_chars:
                output.append(Token(q, st))
                if c == '\0':
                    break
                st = 'ws'
                q = ''
            elif c in id_chars:
                q += c
            elif c == '\'':
                st = 'ch'
                q = ''
            elif c in op_chars:
                output.append(Token(q, st))
                st = 'op'
                q = c
                # handle function call
                if c == '(':
                    q = function_call_l_parenth
                else:
                    q = c
        
        elif st == 'num':
            if c in ws_chars:
                if q.startswith((number_bin, number_hex)):
                    q = str(int(q, base=0))
                output.append(Token(q, st))
                if c == '\0':
                    break
                st = 'ws'
                q = ''
            elif c in num_chars:
                if c == '.' and '.' in q:
                    raise ValueError(f'Bad charactor for number {q}: {c}')
                else:
                    q += c
            elif c in id_chars:
                if (q + c == number_hex
                        or (q + c)[:2] == number_hex and c in hex_chars
                        or q + c == number_bin):
                    q += c
                else:
                    raise ValueError(f'Bad charactor for number {q}: {c}')
            elif c == '\'':
                raise ValueError(f'Bad charactor at for number {q}: {c}')
            elif op_chars:
                if q.startswith((number_bin, number_hex)):
                    q = str(int(q, base=0))
                output.append(Token(q, st))
                st = 'op'
                q = c
        
        elif st == 'ch':
            if len(q) == 0:
                if ch_escaping:
                    if c == '\\':
                        q = c
                    elif c in esc_chars:
                        q = esc_table[c]
                    else:
                        raise ValueError(f'Bad escape charactor: {repr(c)}')
                    ch_escaping = False
                else:
                    if c == '\\':
                        ch_escaping = True
                    elif c in printable:
                        q = c
                    else:
                        raise ValueError(f'Bad ascii charactor: {repr(c)}')
            elif len(q) == 1:
                if c in ws_chars:
                    if c == '\0':
                        break
                    st = 'ws'
                    q = ''
                elif c in num_chars:
                    st = 'num'
                    q = c
                elif c == '\'':
                    output.append(Token(ord(q), 'num'))
                elif c in id_chars:
                    st = 'id'
                    q = c
                elif op_chars:
                    st = 'op'
                    q = c

        elif st == 'op':
            if c in ws_chars:
                output.append(Token(q, st))
                if c == '\0':
                    break
                st = 'ws'
                q = ''
            elif c in num_chars:
                output.append(Token(q, st))
                st = 'num'
                q = c
            elif c == '\'':
                output.append(Token(q, st))
                st = 'ch'
                q = ''
            elif c in id_chars:
                output.append(Token(q, st))
                st = 'id'
                q = c
            elif op_chars:
                if (q + c) in all_ops:
                    q += c
                else:
                    output.append(Token(q, st))
                    # handle unary + -
                    if (c == '-' or c == '+') and q not in r_brackets:
                        q = '!' + c
                    # handle function call
                    elif c == '(' and q in r_brackets:
                        q = function_call_l_parenth
                    elif c == ')' and q == '$(':
                        # add the inferred null
                        output.append(Token('null', 'id'))
                        q = c
                    else:
                        q = c
        if is_debug:
            print(repr(q), output, sep='\t')
    return output

    
if __name__ == '__main__':
    print(parse_token('+3 + 4 * -2 / (1-5) ^ 2 ^ 3'))
    print(parse_token('sin(max(2, 3) / 3 * pi)'))
    print(parse_token('add = p : { @p + $p ;}'))

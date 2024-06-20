from oper import *
from typing import List, Literal

uanry_pm_preced = set(all_ops).difference(r_brackets).union([None])

id_chars = set('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_')
lit_chars = set('0123456789.')
op_chars = set(r''.join([ops for ops in all_ops]))
ws_chars = set(' \t\r\n\0')

states = {
    'id',
    'lit', # literal
    'op', # operator
    'ws', # white space
}

token_types = {
    'id',
    'lit', # literal
    'op', # operator
}

class Token:
    def __init__(self, raw, tok_type: Literal['id', 'lit', 'op']) -> None:
        self.raw = raw
        self.type = tok_type
    
    def __repr__(self) -> str:
        return f'T({self.type}:{repr(self.raw)})'

def parse_token(raw_str: str, is_debug=False) -> List[str]:
    is_comment = False
    st = 'ws'
    q = ''
    output: List[Token] = []
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
            elif c in lit_chars:
                st = 'lit'
                q = c
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
                elif c == '(' and (last.type != 'op' or last.raw in r_brackets):
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
                st = 'ws'
                q = ''
            elif c in id_chars or c in lit_chars:
                q += c
            elif c in op_chars:
                output.append(Token(q, st))
                st = 'op'
                q = c
                # handle function call
                if c == '(':
                    q = function_call_l_parenth
                else:
                    q = c
        
        elif st == 'lit':
            if c in ws_chars:
                output.append(Token(q, st))
                st = 'ws'
                q = ''
            elif c in id_chars:
                raise ValueError(f'bad charactor at index {n}: {c}')
            elif c in lit_chars:
                if c == '.' and '.' in q:
                    raise ValueError(f'bad charactor at index {n}: {c}')
                else:
                    q += c
            elif op_chars:
                output.append(Token(q, st))
                st = 'op'
                q = c
        
        elif st == 'op':
            if c in ws_chars:
                output.append(Token(q, st))
                st = 'ws'
                q = ''
            elif c in id_chars:
                output.append(Token(q, st))
                st = 'id'
                q = c
            elif c in lit_chars:
                output.append(Token(q, st))
                st = 'lit'
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
    if len(q):
        output.append(Token(q, st))
    if is_debug:
        print(st, repr('<end>'), sep='\t')
        print(repr(q), output, sep='\t')
    return output

    
if __name__ == '__main__':
    print(parse_token('+3 + 4 * -2 / (1-5) ^ 2 ^ 3'))
    print(parse_token('sin(max(2, 3) / 3 * pi)'))
    print(parse_token('add = p : { @p + $p ;}'))
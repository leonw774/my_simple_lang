from typing import List

from lexer import Token
from oper import *

def shunting_yard(
        tokens: List[Token],
        is_debug=False
    ) -> List[str]:
    """Parse token sequence into postfix notation"""

    output = []
    op_stack = []
    def get_top():
        return op_stack[-1] if len(op_stack) > 0 else None
    for t in tokens:
        if is_debug:
            print(repr(t))
        if t.type == 'op':
            t_precedence = op_precedence[t.raw]
            is_t_left_asso = t.raw not in right_associative_ops
            top = get_top()

            def is_top_lower(top, t):
                if top is not None:
                    top_precedence = op_precedence[top.raw]
                    return (
                        top_precedence < t_precedence
                        or (top_precedence == t_precedence and is_t_left_asso)
                    )
                return False

            while is_top_lower(top, t) and top.raw not in l_brackets:
                # print('top', top)
                output.append(top)
                op_stack.pop()
                top = get_top()
            if t.raw not in r_brackets:
                op_stack.append(t)
            else:
                # pop until left bracket is meet
                while top.raw not in l_brackets:
                    output.append(top)
                    op_stack.pop()
                    top = get_top()
                # pop out the left bracket
                l_bracket = op_stack.pop()
                top = get_top()
                # if the l_brackets is function call
                if l_bracket.raw == function_caller:
                    output.append(l_bracket)
        else:
            output.append(t)
        
        if is_debug:
            print('stack:\t', op_stack)
            print('out:\t', output)
    # end for
    # empty the stack
    output += op_stack[::-1]
    if is_debug:
        print('final:\t', output)
    return output

if __name__ == '__main__':
    print(shunting_yard(
        ['!+', '3', '+', '4', '*', '!-', '2', '/', '(', '1', '-', '5', ')', '^', '2', '^', '3', ';'],
    ))

    print(shunting_yard(
        ['sin', '(', 'max', '(', '2', ',', '3', ')', '/', '3', '*', 'pi', ')', ';'],
        {'sin', 'max'}
    ))

    print(shunting_yard(
        ['add', '=', 'p', ':', '{', '@', 'p', '+', '$', 'p', ';', '}']
    ))
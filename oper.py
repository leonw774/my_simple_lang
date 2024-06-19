
operator_hierarchies = [
    # parenthesis, function call parenthesis, code block
    ('(', ')', '!(', '{', '}'),
    # unary plus and minus, logic not, get left of pair, get right of pair
    ('!+', '!-', '!', '@', '$'),
    # power
    ('^',),
    # multiplication, division, remainder
    ('*', '/', '%'),
    # addition, subtraction
    ('+', '-'),
    # write a byte to stdout and return null, read a byte from stdin (not implemented yet)
    ('<<', '>>'),
    # inequality comparisons
    ('<', '<=', '>', '>='),
    # equal, not equal
    ('==', '!='),
    # logic and
    ('&',),
    # logic or 
    ('|',),
    # make pairing
    (',',),
    # function declarator
    # arg_id : { expressions }
    (':',),
    # if operation
    # `a ? b` evaluates `b` when `a` evaluates to true, otherwise null
    ('?',),
    # assignment
    ('=',),
    # expression connector
    (';',)
]

op_precedence = {
    op: p
    for p, ops in enumerate(operator_hierarchies)
    for op in ops
}

right_associative_ops = {'!+', '!-', '!', '^', '@', '$', ':', '=', ','}

unary_ops = {'!+', '!-', '!', '@', '$', '<<', '>>'}

l_brackets = {'(', '!(', '{'}
r_brackets = {')', '}'}

function_caller = '!('
function_declarator = ':'
assignment = '='
branch_operator = '?'
expression_connector = ';'
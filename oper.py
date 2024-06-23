
operator_hierarchies = [
    # function code maker
    ('{', '}'),
    # parenthesis / function call, function caller
    ('(', ')', '$'),
    # unary plus and minus, logic not, get left of pair, get right of pair
    ('!+', '!-', '!', '`', '~'),
    # power
    ('^',),
    # multiplication, division, remainder
    ('*', '/', '%'),
    # addition, subtraction
    ('+', '-'),
    # write a byte to stdout and return null
    ('<<', ),
    # inequality comparisons
    ('<', '<=', '>', '>='),
    # equal, not equal
    ('==', '!='),
    # logic and
    ('&',),
    # logic or 
    ('|',),
    # pair maker
    (',',),
    # function argument adder
    # arg_id : { function codes }
    (':',),
    # if operation
    # `a ? b` evaluates `b` when `a` evaluates to true, otherwise null
    ('?',),
    # assignment
    ('=',),
    # expression connector
    (';',)
]

all_ops = {
    op
    for ops in operator_hierarchies
    for op in ops
}

op_precedences = {
    op: p
    for p, ops in enumerate(operator_hierarchies)
    for op in ops
}
# add temperary operator '$('
# it means the parenthesis is part of a function call
op_precedences['$('] = op_precedences['(']
# add function code indicator '@'
op_precedences['@'] = op_precedences['{']

right_associative_ops = {'!+', '!-', '!', '^', '`', '~', ':', '=', ','}

unary_ops = {'@', '!+', '!-', '!', '`', '~', '<<', '>>'}

l_brackets = {'(', '{', '$('}
r_brackets = {')', '}'}

function_call_l_parenth = '$('
function_maker = '@'
function_caller = '$'
argument_setter = ':'
assignment = '='
if_operator = '?'
expression_connector = ';'
import sys
from typing import List, Callable
from copy import copy 

from lexer import Token
from oper import *
from eval_objs import *

def do_call(func_obj: FuncObj, arg_obj: GeneralObj) -> GeneralObj:
    if func_obj.arg_id is not None:
        init_id_obj_table = {func_obj.arg_id: arg_obj}
        init_id_obj_table.update(func_obj.id_obj_table)
    else:
        init_id_obj_table = func_obj.id_obj_table.copy()
    return eval_node(
        func_obj.code_root_node,
        init_id_obj_table=init_id_obj_table
    )

def do_write_byte(num_obj: NumObj) -> NullObj:
    assert num_obj.value.denominator == 1
    v = int(num_obj.value)
    assert 0 <= v <= 255
    sys.stdout.buffer.write(bytes((v,)))
    sys.stdout.flush()
    return NullObj()

op_func_configs = {
    '$': ((FuncObj, GeneralObj), do_call),
    '!+': ((NumObj,),   lambda x: NumObj(x.value)),
    '!-': ((NumObj,),   lambda x: NumObj(-x.value)),
    '!': ((NumObj,),    lambda x: NumObj(x.value == 0)),
    '`': ((PairObj,),   lambda x: x.left),
    '~': ((PairObj,),   lambda x: x.right),
    '^': ((NumObj, NumObj), lambda x, y: NumObj(x.value ** y.value)),
    '*': ((NumObj, NumObj), lambda x, y: NumObj(x.value * y.value)),
    '/': ((NumObj, NumObj), lambda x, y: NumObj(x.value / y.value)),
    '%': ((NumObj, NumObj), lambda x, y: NumObj(x.value % y.value)),
    '+': ((NumObj, NumObj), lambda x, y: NumObj(x.value + y.value)),
    '-': ((NumObj, NumObj), lambda x, y: NumObj(x.value - y.value)),
    '<<': ((NumObj,),   do_write_byte),
    '>>': ((NumObj,),   lambda x: NotImplementedError()),
    '<': ((NumObj, NumObj), lambda x, y: NumObj(x.value < y.value)),
    '>': ((NumObj, NumObj), lambda x, y: NumObj(x.value > y.value)),
    '<=': ((NumObj, NumObj),    lambda x, y: NumObj(x.value <= y.value)),
    '>=': ((NumObj, NumObj),    lambda x, y: NumObj(x.value >= y.value)),
    '==': ((GeneralObj, GeneralObj),    lambda x, y: NumObj(type(x) == type(y) and x == y)),
    '!=': ((GeneralObj, GeneralObj),    lambda x, y: NumObj(type(x) != type(y) or x != y)),
    '&': ((GeneralObj, GeneralObj), lambda x, y: NumObj(bool(x) and bool(y))),
    '|': ((GeneralObj, GeneralObj), lambda x, y: NumObj(bool(x) or bool(y))),
    ',': ((GeneralObj, GeneralObj), lambda x, y: PairObj(x, y)),
    ';': ((GeneralObj, GeneralObj), lambda x, y: y),
}

def op_func_builder(arg_types: tuple, real_func: Callable):
    def f(args):
        assert len(args) == len(arg_types), \
            f'Bad argument number: want {len(arg_types)} but get {len(args)}'
        for arg, arg_type in zip(args, arg_types):
            assert isinstance(arg, arg_type), \
                f'argument: {arg} is not of type {arg_type.__name__}'
        return real_func(*args)
    return f

op_funcs = {
    op: op_func_builder(*op_func_config)
    for op, op_func_config in op_func_configs.items()
}


def eval_postfix(postfix_token: List[Token], is_debug=False) -> GeneralObj:
    tree_root = postfix_to_tree(postfix_token, is_debug=is_debug)
    if is_debug:
        print(TreeNode.dump(tree_root))
    global g_is_debug
    g_is_debug = is_debug
    return eval_node(tree_root)

def postfix_to_tree(postfix: List[str], is_debug=False) -> TreeNode:
    stack = list()
    for t in postfix:
        if is_debug:
            print(t, stack)
        if t.type == 'op':
            r_node = stack.pop() if t.raw not in unary_ops else None
            try:
                l_node = stack.pop()
            except IndexError as e:
                print(f'token {t} has too few children')
                raise e
            stack.append(TreeNode(
                tok=t.raw, node_type=t.type,
                left=l_node, right=r_node
            ))
        else:
            stack.append(TreeNode(tok=t.raw, node_type=t.type))
    assert len(stack) == 1, \
        f'bad grammer: there are nodes remained in stack {stack}'
    return stack[0]

class NodeEvalDict:
    def __init__(self) -> None:
        self.table = dict()
    
    def __getitem__(self, node: TreeNode) -> Optional[GeneralObj]:
        return self.table.get(id(node), None)
    
    def __setitem__(self, node: TreeNode, value: GeneralObj) -> None:
        self.table[id(node)] = value

def eval_node(
        root_node: TreeNode,
        init_id_obj_table = None) -> GeneralObj:
    id_obj_table = {'null': NullObj()}
    if init_id_obj_table is not None:
        id_obj_table.update(init_id_obj_table)
    if g_is_debug:
        print('initial id_obj_table:', id_obj_table)

    node_eval_to = NodeEvalDict()

    node_stack: List[TreeNode] = [root_node]
    while len(node_stack):
        if g_is_debug:
            print('stack', node_stack)
        node = node_stack[-1]
        if node.type == 'op':
            if node.tok in unary_ops:
                if node.tok == function_maker:
                    node_eval_to[node] = FuncObj(
                        code_root_node = node.left,
                        id_obj_table=id_obj_table,
                        arg_id=None
                    )
                    if g_is_debug:
                        print('op', node, 'eval to:', node_eval_to[node])
                elif node_eval_to[node.left] is None:
                    node_stack.append(node.left)
                    continue
                else:
                    node_op_func = op_funcs[node.tok]
                    args = (node_eval_to[node.left], )
                    if g_is_debug:
                        print('op:', node, 'args:', args)
                    node_eval_to[node] = node_op_func(args)
                    if g_is_debug:
                        print('eval to:', node_eval_to[node])
            else:
                if node.tok == argument_setter:
                    assert node.left.type == 'id', \
                        'Left side of argument setter should be identifier'
                    if node_eval_to[node.right] is None:
                        node_stack.append(node.right)
                        continue
                    else:
                        assert isinstance(node_eval_to[node.right], FuncObj), \
                            'Right side of argument setter should be function block'
                        node_eval_to[node] = copy(node_eval_to[node.right])
                        node_eval_to[node].arg_id = node.left.tok

                elif node.tok == assignment:
                    assert node.left is not None and node.left.type == 'id', \
                        f'Left side of assignment should be identifier. Get {node.left}'
                    if node_eval_to[node.right] is None:
                        node_stack.append(node.right)
                        continue
                    else:
                        id_obj_table[node.left.tok] = node_eval_to[node.right]
                        node_eval_to[node] = node_eval_to[node.right]
                        if g_is_debug:
                            print('update id-obj table:', id_obj_table)

                elif node.tok == if_operator:
                    # eval left first
                    if node_eval_to[node.left] is None:
                        node_stack.append(node.left)
                        continue
                    else:
                        if bool(node_eval_to[node.left]):
                            if node_eval_to[node.right] is None:
                                node_stack.append(node.right)
                                continue
                            else:
                                node_eval_to[node] = node_eval_to[node.right]
                        else:
                            node_eval_to[node] = node_eval_to[node.left]
                        if g_is_debug:
                            print('op', node, 'eval to:', node_eval_to[node])

                elif node_eval_to[node.left] is None and node_eval_to[node.right] is None:
                    node_stack.append(node.right)
                    node_stack.append(node.left)
                    continue

                else:
                    node_op_func = op_funcs[node.tok]
                    args = (node_eval_to[node.left], node_eval_to[node.right])
                    if g_is_debug:
                        print('op:', node, 'args:', args)
                    node_eval_to[node] = node_op_func(args)
                    if g_is_debug:
                        print('eval to:', node_eval_to[node])

        elif node.type == 'id':
            obj = id_obj_table.setdefault(node.tok, NullObj())
            if g_is_debug:
                print('update id-obj table:', id_obj_table)
            node_eval_to[node] = obj

        elif node.type == 'lit':
            node_eval_to[node] = NumObj(node.tok)

        else:
            raise ValueError(f'bad node type: {node.type}')
        node_stack.pop()
    # end while
    return node_eval_to[root_node]
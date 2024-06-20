from fractions import Fraction
from decimal import Decimal
from typing import Optional, Union, Literal

class GeneralObj:
    pass

class TreeNode:
    def __init__(self, tok: str, node_type: Literal['op', 'id', 'lit'],
                 left = None, right = None) -> None:
        self.tok = tok
        self.type = node_type
        self.left: Optional[TreeNode] = left
        self.right: Optional[TreeNode] = right
        self.eval_to: Optional[GeneralObj] = None

    def __repr__(self):
        return f'N({self.type}:{repr(self.tok)})'

    @classmethod
    def dump(cls, root_node, indent = 2) -> str:
        res_str = ''
        res_str += repr(root_node) + '\n'
        queue = []
        queue.append((root_node.right, indent))
        queue.append((root_node.left, indent))
        while len(queue) > 0:
            node, depth = queue.pop()
            if node is not None:
                res_str += ' ' * depth + repr(node) + '\n'
                queue.append((node.right, depth + indent))
                queue.append((node.left, depth + indent))
        return res_str

class NullObj(GeneralObj):
    def __init__(self) -> None:
        self.value = None
    
    def __bool__(self) -> bool:
        return False
    
    def __repr__(self) -> str:
        return 'NullObj'

    def __eq__(self, other) -> bool:
        return self.value == other.value

class NumObj(GeneralObj):
    def __init__(self, init_value: Union[float, Decimal, str]) -> None:
        self.value = Fraction(init_value)
    
    def __bool__(self) -> bool:
        return self.value != 0

    def __repr__(self) -> str:
        return (
            repr(int(self.value))
            if self.value.denominator == 1 else
            repr(float(self.value))
        )

    def __eq__(self, other) -> bool:
        return self.value == other.value

class FuncObj(GeneralObj):
    def __init__(
            self,
            code_root_node: TreeNode,
            id_obj_table: dict,
            arg_id: Optional[str] = None) -> None:
        self.arg_id = arg_id
        self.code_root_node = code_root_node
        # the reference of the id-obj table at the same scope of the function
        # so that it can so recursion and access variable from outside
        self.id_obj_table = id_obj_table
    
    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f'[function {self.arg_id} : code root {self.code_root_node}]'
    
    def __eq__(self, other) -> bool:
        return self.code_root_node == other.code_root_node

class PairObj(GeneralObj):
    def __init__(self, init_left: GeneralObj, init_right: GeneralObj) -> None:
        self.left = init_left
        self.right = init_right
    
    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f'({self.left}, {self.right})'

    def __eq__(self, other) -> bool:
        return self.left == other.left and self.right == other.right 

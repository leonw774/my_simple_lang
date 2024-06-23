from argparse import ArgumentParser
from lexer import parse_token
from postfixer import shunting_yard
from evaler import eval_postfix, GeneralObj

def interpret_code(raw_str: str, is_debug: bool = False) -> GeneralObj:
    tokens = parse_token(raw_str, is_debug=is_debug)
    postfix = shunting_yard(tokens, is_debug=is_debug)
    eval_result = eval_postfix(postfix, is_debug=is_debug)
    if is_debug:
        print('eval_result:', eval_result)
    return eval_result

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input_file_path', nargs='?', const='', default='')
    parser.add_argument('--code', '-c', dest='raw_str', default='')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    raw_str = None
    if args.input_file_path != '':
        with open(args.input_file_path, 'r', encoding='utf8') as f:
            raw_str = f.read()
    elif args.raw_str != '':
        raw_str = args.raw_str
    if raw_str is None:
        ValueError('code is empty')
        exit()
    interpret_code(raw_str, args.debug)

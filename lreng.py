from argparse import ArgumentParser
from lexer import parse_token
from postfixer import shunting_yard
from evaler import eval_postfix

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
        exit()
    tokens = parse_token(raw_str, is_debug=args.debug)
    postfix = shunting_yard(tokens, is_debug=args.debug)
    eval_result = eval_postfix(postfix, is_debug=args.debug)
    if args.debug:
        print('eval_result:', eval_result)

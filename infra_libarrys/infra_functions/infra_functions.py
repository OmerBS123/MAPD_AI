from collections import defaultdict

from infra_libarrys.consts_and_enums.parser_func_consts import ParserFlag


def parse_args(file_path):
    parser_dict = defaultdict(list)
    with open(file_path) as txt_file:
        for line in txt_file:
            flag_char = get_flag_char(line)
            parse_func = ParserFlag.PARSER_FLAG_DICT[flag_char]
            parse_func(line, parser_dict)
    return parser_dict


def get_flag_char(line):
    before_idx = line.find('#')
    return line[before_idx + 1]

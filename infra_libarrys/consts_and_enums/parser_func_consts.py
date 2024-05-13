from infra_libarrys.infra_functions import parser_functions


class ParserFlag:
    PARSER_FLAG_DICT = \
        {
            "X": parser_functions.parse_x_flag,
            "Y": parser_functions.parse_y_flag,
            "B": parser_functions.parse_b_flag,
            "F": parser_functions.parse_f_flag,
            "P": parser_functions.parse_p_flag,
            "A": parser_functions.parse_agent_flag,
            "H": parser_functions.parse_agent_flag,
            "I": parser_functions.parse_agent_flag,
            "G": parser_functions.parse_agent_flag,
            "Z": parser_functions.parse_agent_flag,
            "S": parser_functions.parse_agent_flag,
            "W": parser_functions.parse_agent_flag}

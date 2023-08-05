import re


def remove_all_tabs(text_to_format):
    return re.sub('\t', '', text_to_format)


def ident_in_select_from_clause(text_to_format):
    return re.sub('[\n]?,[\s]?', '\n\t, ', text_to_format)

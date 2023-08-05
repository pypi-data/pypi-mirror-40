import clauses
import functions
import identation
import os


def read_file(path):
    file = open(path, 'r')
    file_content = file.read()
    file.close()

    return file_content


def write_file(path, content):
    file = open(path, 'w')
    file.write(content)
    file.close

    return True


def format_string(file_content):
    file_content = identation.remove_all_tabs(file_content)
    file_content = functions.format_sql_functions(file_content)
    file_content = clauses.format_break_line_before_tokens(file_content)
    file_content = clauses.format_new_line_tokens(file_content)
    file_content = clauses.format_same_line_tokens(file_content)
    file_content = identation.ident_in_select_from_clause(file_content)

    return file_content

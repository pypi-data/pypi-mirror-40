import formatter.identation as id
import pytest


def test_remove_all_tabs_one_tab():
    assert id.remove_all_tabs('\t') == ''


def test_remove_all_tabs_multiple_tabs():
    assert id.remove_all_tabs('\t\t\t') == ''


def test_remove_all_tabs_tab_around_text():
    assert id.remove_all_tabs('teste\t teste \tteste') == 'teste teste teste'


def test_remove_all_tabs_tab_around_tokens():
    input_string = 'teste\t\n teste \tteste'
    expected_string = 'teste\n teste teste'

    assert id.remove_all_tabs(input_string) == expected_string


def test_ident_in_select_from_clause():
    input_string = 'SELECT\n\t  campo1,campo2,campo3'
    expected_string = 'SELECT\n\t  campo1\n\t, campo2\n\t, campo3'

    assert id.ident_in_select_from_clause(input_string) == expected_string

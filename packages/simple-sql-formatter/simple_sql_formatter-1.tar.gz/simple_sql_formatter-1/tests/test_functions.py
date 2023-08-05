import formatter.functions as sf


def test_format_sql_functions_with_spaces():
    assert sf.format_sql_functions('round (') == 'ROUND('


def test_format_sql_functions_without_spaces():
    assert sf.format_sql_functions('round(') == 'ROUND('


def test_format_sql_functions_with_break_line():
    assert sf.format_sql_functions('round\n(') == 'ROUND('


def test_format_sql_functions_multiple_break_lines():
    assert sf.format_sql_functions('round\n\n\t(') == 'ROUND('


def test_format_sql_functions_case_insensitive():
    assert sf.format_sql_functions('RouNd(') == 'ROUND('

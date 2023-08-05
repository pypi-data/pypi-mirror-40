import formatter.formatter as fm
import pytest
import os

dirname = os.path.dirname(__file__)
dirname = os.path.join(dirname, 'data_test/')

# @pytest.mark.skip(reason='in development')
def test_format_file_simple():
    filename = os.path.join(dirname, 'simple_input_string.sql')
    simple_input_string = fm.read_file(filename)
    result_string = fm.format_string(simple_input_string)

    filename = os.path.join(dirname, 'simple_output_string.sql')
    fm.write_file(filename, result_string)


# @pytest.mark.skip(reason='in development')
def test_format_file_complex():
    filename = os.path.join(dirname, 'complex_input_string.sql')
    complex_input_string = fm.read_file(filename)
    result_string = fm.format_string(complex_input_string)

    filename = os.path.join(dirname, 'complex_output_string.sql')
    fm.write_file(filename, result_string)

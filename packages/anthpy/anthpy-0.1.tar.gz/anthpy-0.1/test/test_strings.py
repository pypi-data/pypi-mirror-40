import pytest
import anthpy.strings


@pytest.mark.parametrize("input_str,expected", [
    ("/path/to/file.txt", ["/path/to", "file", ".txt"]),
    ("file.txt", ["", "file", ".txt"]),
    ("/path/file", ["/path", "file", ""]),
    ("", ["", "", ""]),
])
def test_file_parts(input_str, expected):
    assert expected == anthpy.strings.file_parts(input_str)

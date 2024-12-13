import pytest
from translator import Translator

def test_parse_constant():
    t = Translator()
    assert t.parse_constant("number", 42) == "set number = 42;"
    assert t.parse_constant("array", [1, 2, 3]) == "set array = [ 1, 2, 3 ];"

def test_parse_expression():
    t = Translator()
    t.constants = {"number": 42}
    assert t.parse_expression("{number + 10}") == 52
    assert t.parse_expression("{number * 2}") == 84

def test_translate():
    t = Translator()
    toml_data = {
        "number": 42,
        "array": [1, 2, 3],
        "expression": "{number + 10}"
    }
    result = t.translate(toml_data)
    assert "set number = 42;" in result
    assert "set array = [ 1, 2, 3 ];" in result
    assert "# Evaluated expression {number + 10} = 52" in result
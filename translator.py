import sys
import re
import toml

class Translator:
    def __init__(self):
        self.constants = {}

    def parse_constant(self, name, value):
        """Обработка объявления константы."""
        if not re.match(r"^[a-zA-Z]+$", name):
            raise ValueError(f"Invalid constant name: {name}")
        if isinstance(value, (int, float, list)):
            self.constants[name] = value
            return f"set {name} = {self.format_value(value)};"
        else:
            raise ValueError(f"Unsupported value type for constant: {value}")

    def parse_expression(self, expression):
        """Обработка выражений."""
        pattern = r"^\{([a-zA-Z]+)\s*([\+\-\*/])\s*([0-9]+)\}$"
        match = re.match(pattern, expression)
        if not match:
            raise ValueError(f"Invalid expression syntax: {expression}")

        name, operator, number = match.groups()
        number = int(number)
        if name not in self.constants:
            raise ValueError(f"Undefined constant: {name}")

        # Выполняем вычисление
        if operator == "+":
            result = self.constants[name] + number
        elif operator == "-":
            result = self.constants[name] - number
        elif operator == "*":
            result = self.constants[name] * number
        elif operator == "/":
            result = self.constants[name] / number
        else:
            raise ValueError(f"Unsupported operator: {operator}")

        return result

    def format_value(self, value):
        """Форматирование значения для языка."""
        if isinstance(value, list):
            return f"[ {', '.join(map(str, value))} ]"
        return str(value)

    def translate(self, toml_data):
        """Трансляция TOML в учебный конфигурационный язык."""
        output = []
        for key, value in toml_data.items():
            if isinstance(value, dict):
                raise ValueError(f"Nested tables are not supported: {key}")
            elif isinstance(value, (int, float, list)):
                output.append(self.parse_constant(key, value))
            elif isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                result = self.parse_expression(value)
                output.append(f"# Evaluated expression {value} = {result}")
            else:
                raise ValueError(f"Unsupported type for key {key}: {value}")
        return "\n".join(output)
import sys
import toml
from translator import Translator




def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <output_file>")
        sys.exit(1)

    output_file = sys.argv[1]
    translator = Translator()

    try:
        toml_input = sys.stdin.read()
        toml_data = toml.loads(toml_input)

        result = translator.translate(toml_data)

        with open(output_file, 'w') as f:
            f.write(result)

        print(f"Translation successful! Output written to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


main()
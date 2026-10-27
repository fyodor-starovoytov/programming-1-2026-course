from pathlib import Path

class InputFile:
    """The input file is held in InputFile class and can be modified through it"""
    def __init__(self, path, filename):

        existing_path = Path.home() / path / filename
        if existing_path.exists():
            self.path = existing_path
        else:
            self.path = Path(path / filename)

        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                self.lines = [line.strip().lower() for line in file if line.strip()]
        except FileNotFoundError as e:
            print(f"Error: File not found -> {self.path}")
            self.lines = []
        except IsADirectoryError:
            print(f"Error: Expected a file, but found a directory -> {self.path}")
            self.lines = []
        
    def __str__(self) -> str:
        return f'{self.lines}'

    def __repr__(self):
        return self.lines

    def line_count(self) -> int:
        """Returns the number of lines in the variable"""
        return len(self.lines)

    def get_lines(self) -> list:
        """Returns the lines in the variable"""
        return self.lines

    def new_lines(self, lines: list):
        """Sets the new lines in variable, not the variable"""
        self.lines = lines

    def save_file(self):
        """Creates a copy of the input file in the original directory and saves it"""
        new_file_path = self.path.parent / f"{self.path.stem}_obfuscated.txt"
        to_return = ""
        with open(new_file_path, 'w', encoding='utf-8') as file:
            for line in self.lines:
                to_return += f"{line}\n"
            file.writelines(to_return)
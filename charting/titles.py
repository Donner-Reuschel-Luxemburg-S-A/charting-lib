import ast
import os
import json


def find_title_in_main(node):
    """ Recursively search for the 'title' assignment within the main function. """
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.Assign):
            for target in child.targets:
                if isinstance(target, ast.Name) and target.id == 'title':
                    if isinstance(child.value, ast.Str):  # Python 3.7 and below
                        return child.value.s
                    elif isinstance(child.value, ast.Constant):  # Python 3.8 and above
                        return child.value.value
        result = find_title_in_main(child)
        if result:
            return result


def parse_python_file(filepath):
    """ Parse a Python file to find the title in the main function. """
    with open(filepath, 'r', encoding='utf8') as file:
        tree = ast.parse(file.read(), filename=filepath)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'main':
            title = find_title_in_main(node)
            return title


def parse_directory(directory):
    """ Walk through the directory and parse each Python file. """
    titles = {}
    no_title_files = []  # List to keep track of files with no title found

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                title = parse_python_file(filepath)
                if title:
                    titles[title] = ""
                else:
                    no_title_files.append(filepath)  # Add filepath to list if no title is found

    return titles, no_title_files


def main():
    directory = 'C:\\Users\\ssymhoven\\Projekte\\charting-lib\\charting\\charts\\production'  # Path to the directory
    titles, no_title_files = parse_directory(directory)
    with open('titles.json', 'w', encoding='utf8') as json_file:
        json.dump(titles, json_file, indent=4)

    if no_title_files:
        print("No title found in the following files:")
        for file in no_title_files:
            print(file)


if __name__ == '__main__':
    main()

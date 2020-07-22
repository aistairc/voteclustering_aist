from eralchemy import render_er
import re
import os

def find_filepath_from_directory(directory, filename):
    regex = re.compile(r'(%s)$' % filename)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if regex.match(file):
                return os.path.join(root, file)


def_file_path = find_filepath_from_directory('.', 'table_definition.er')
def_file_directory = os.path.dirname(def_file_path)
render_er(def_file_path, os.path.join(def_file_directory, "table_definition.png"))


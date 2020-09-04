from fnmatch import fnmatch
from deb_pkg_tools.package import parse_deb822
from pathlib import Path
import subprocess
import os


def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.
    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # filter by file type
            if fnmatch(filename, '*.deb'):
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.
    return file_paths  # Self-explanatory.


def main():
    deb_folder = str(Path('deb'))
    arr = get_filepaths(deb_folder)
    for filename in arr:
        try:
            full_name = f'./{filename}'
            process = subprocess.check_output(['dpkg', '-f', full_name]).decode('utf-8')
            components_d = parse_deb822(process)
            components_str = f'{components_d["Package"]}_{components_d["Version"]}_{components_d["Architecture"]}'
            if components_str not in filename:
                print(f'File: "./{filename}" does not match with "{components_str}"')
        except:
            pass


if __name__ == '__main__':
    main()

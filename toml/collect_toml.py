#!/bin/python3

import os
import argparse
import shutil
import logging

from util import list_toml, setup_logger

logger = logging.getLogger()

def clear_toml(root):
    count = 0
    for toml_file in list_toml(root):
        os.remove(os.path.join(root, toml_file))
        count += 1
    return count

if __name__ == "__main__":
    CURR_DIR = os.path.abspath(".")

    parser = argparse.ArgumentParser(description="Search a directory recursively for toml files and copy them")

    parser.add_argument("--search-dir", metavar="search directory", type = str, help = "Set search root dir")
    parser.add_argument("--output-dir", metavar="output directory", type = str, help = "Set output dir", default = CURR_DIR)

    args = parser.parse_args()

    name_dict = dict()
    name_list = list()
    count = 0
    clear_count = clear_toml(args.output_dir)

    if args.search_dir:
        for toml_file in list_toml(args.search_dir):
            name = toml_file.split("/")[-1]
            if not name in name_dict:
                name_dict[name] = 1
            else:
                name_dict[name] += 1
            new_name = "{0}_{1:03}.toml".format(name.split(".")[0], name_dict[name])
            dest = os.path.join(args.output_dir, new_name)
            name_list.append((toml_file, dest))
            print(toml_file)

        for (src, dest) in name_list:
            shutil.copyfile(src, dest)
        print(f"Cleared {clear_count} files from '{args.output_dir}'")
        print(f"Copied {len(name_list)} files to '{args.output_dir}'")
    else:
        parser.print_usage()
        exit(1)

#!/bin/python3

import os
import argparse
import shutil


CURR_DIR = os.path.abspath(".")

parser = argparse.ArgumentParser(description="Search a directory recursively for toml files and copy them")

parser.add_argument("--search-dir", metavar="search directory", type = str, help = "Set search root dir")
parser.add_argument("--output-dir", metavar="output directory", type = str, help = "Set output dir", default = CURR_DIR)

args = parser.parse_args()

name_dict = dict()
count = 0

if args.search_dir:
    for root, dirs, files in os.walk(args.search_dir):
        for name in files:
            if name.endswith(".toml"):
                src = os.path.join(root, name)

                if not name in name_dict:
                    name_dict[name] = 1
                else:
                    name_dict[name] += 1
                new_name = "{0}_{1:03}.toml".format(name.split(".")[0], name_dict[name])
                dest = os.path.join(args.output_dir, new_name)

                shutil.copyfile(src, dest)
                print(dest)
                count += 1
    print(f"Copied {count} files")
else:
    parser.print_usage()
    exit(1)


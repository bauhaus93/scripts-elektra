#!/bin/python3

import os
import subprocess
import argparse
import logging
import time

from util import setup_logger, list_toml

logger = logging.getLogger()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def test_file(file_path, parser_path, silent = True):
    with open(file_path, "r") as f:
        try:
            if silent:
                result = subprocess.run(f"{parser_path}", stdin = f, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
            else:
                result = subprocess.run(f"{parser_path}", stdin = f)
            result.check_returncode()
            return True
        except subprocess.CalledProcessError as e:
            return False

def add_fail(file_path):
    with open("fail.txt", "a+") as f:
        f.write(file_path + "\n")

def clear_fail():
    if os.path.exists("fail.text"):
        os.remove("fail.txt")

def time_str(start):
    diff = time.time() - start
    if diff < 1.0:
        return "{}ms".format(int(diff * 1000))
    elif diff < 60.0:
        return "{:.2}s".format(diff)
    else:
        return "{}m {}s".format(int(diff) / 60, int(diff) % 60)

CURR_DIR = os.path.abspath(".")
PARSER = os.path.join(CURR_DIR, "toml_parser")

CURR_DIR = os.path.abspath(".")

parser = argparse.ArgumentParser(description="Test parser agains toml files")

parser.add_argument("--parser-dir", metavar="parser directory", type = str, help = "Set parser dir", default = CURR_DIR)
parser.add_argument("--toml-dir", metavar="toml directory", type = str, help = "Set toml dir")

args = parser.parse_args()

if __name__ == "__main__":
    setup_logger()
    count = 0
    success = 0

    clear_fail()

    if args.toml_dir:
        parser_path = os.path.join(args.parser_dir, "toml_parser")
        if os.path.exists(parser_path):
            start = time.time()
            for toml_file in list_toml(args.toml_dir):
                if test_file(toml_file, parser_path):
                    success += 1
                    logger.info(f"{bcolors.OKGREEN}{bcolors.BOLD}Success{bcolors.ENDC}: {toml_file}")
                else:
                    logger.info(f"{bcolors.FAIL}{bcolors.BOLD}Failure{bcolors.ENDC}: {toml_file}")
                    add_fail(toml_file)
                count += 1
            logger.info("====================================");
            logger.info("Finished in {}".format(time_str(start)))
            if success == count:
                color = f"{bcolors.OKGREEN}{bcolors.BOLD}"
            else:
                color = f"{bcolors.FAIL}{bcolors.BOLD}"
            logger.info(f"Result: {color}{success}/{count}{bcolors.ENDC} OK")
            logger.info("====================================");
        else:
            logger.error(f"Could not find parser in {args.parser_dir}")
            exit(1)

    else:
        parser.print_usage()
        exit(1)

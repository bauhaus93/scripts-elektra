import logging
import os

def setup_logger():
    FORMAT = r"[%(asctime)-15s] %(levelname)s - %(message)s"
    DATE_FORMAT = r"%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level = logging.INFO, format = FORMAT, datefmt = DATE_FORMAT)

def list_toml(root):
    for root, dirs, files in os.walk(root):
        for name in files:
            if name.endswith(".toml"):
                yield os.path.abspath(os.path.join(root, name))


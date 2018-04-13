#!/bin/env python3
# coding: utf-8
import yaml
import os
import sys


def main():
    file_path = sys.argv[1]
    with open(file_path, "r") as f:
        data = yaml.load(f)
    count_1 = len(data["GENE"]["1ST"])
    count_2 = len(data["GENE"]["2ND"])
    count_all = count_1 + count_2
    file_abs = os.path.abspath(file_path)
    file_name = os.path.basename(file_abs)
    f_title, f_ext = os.path.splitext(file_name)
    print("=== {} all gene count ===".format(f_title))
    print("1st count : {}".format(count_1))
    print("2nd count : {}".format(count_2))
    print("all count : {}".format(count_all))


if __name__ == "__main__":
    main()

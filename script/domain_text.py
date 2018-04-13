# coding: utf-8
import sys


def main():
    with open(sys.argv[1], "r") as f:
        data = f.read()
    l_row = data.split("\n")
    l_domain = []
    for row in l_row:
        if row == "":
            continue
        if row[:4] == "NAME":
            l_domain.append(row[6:])
    with open(sys.argv[2], "w") as f:
        f.write("\n".join(l_domain))


if __name__ == "__main__":
    main()

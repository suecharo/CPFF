#!/bin/env python3
# coding: utf-8
import requests
import sys


def main():
    with open(sys.argv[1], "r") as f:
        data = f.read()
    l_tmp = data.split("\n")
    if len(l_tmp) == 0:
        print("Your input file is null.")
        sys.exit(1)
    l_domain = []
    for row in l_tmp[1:]:
        if row == "":
            continue
        l_ele = row.split("\t")
        l_domain.append(l_ele[0])

    print("=== Number of domains ===")
    print(len(l_domain))
    print("=== Domain list ===")
    print(" ".join(l_domain))

    print("=== Convert start ===")
    count = 0
    for domain in l_domain:
        count += 1
        print("{} : {}".format(str(count), domain))
        endpoint = "/family/{}/hmm".format(domain)
        url = "http://pfam.xfam.org" + endpoint
        ret = requests.get(url)
        text = ret.text
        with open("./{}/{}.hmm".format(sys.argv[2], domain), "w") as f:
            f.write(text)
    print("=== Convert finish ===")


if __name__ == "__main__":
    main()

#!/bin/env python3
# coding: utf-8
import requests
import sys


def main():
    with open(sys.argv[1], "r") as f:
        data = f.read()
    l_tmp = data.split("\n")
    l_domain = []
    for domain in l_tmp:
        if domain == "":
            continue
        l_domain.append(str(domain))

    print("=== Number of domains ===")
    print(len(l_domain))
    print("=== Domain list ===")
    print(" ".join(l_domain))

    print("=== Convert start ===")
    count = 0
    with open(sys.argv[2], "w") as f:
        for domain in l_domain:
            count += 1
            print("{} : {}".format(str(count), domain))
            endpoint = "/family/{}/hmm".format(domain)
            url = "http://pfam.xfam.org" + endpoint
            ret = requests.get(url)
            text = ret.text
            f.write(text)
    print("=== Convert finish ===")


if __name__ == "__main__":
    main()

# coding: utf-8


def main():
    with open("./KPHMMER_domains.txt", "r") as f:
        data_kphmmer = set(f.read().split("\n"))
    with open("./Pfam-A_domains.txt", "r") as f:
        data_pfam = set(f.read().split("\n"))
    print(len(data_kphmmer & data_pfam))
    with open("dup.txt", "w") as f:
        f.write("\n".join(list(data_kphmmer & data_pfam)))

if __name__ == "__main__":
    main()

#!/bin/env python
# coding: utf-8
from KPHMMER.util import dump_log
import traceback
import sys

class KphmmerStat:
    def __init__(self, tsv_path, yml_path):
        self.tsv_path = tsv_path
        self.yml_path = yml_path
        self.l_domain_gene = []

    def run(self):
        dump_log("Start KPHMMER stat")
        dump_log("=== Your Input ===")
        dump_log("TSV Path : {}".format(self.tsv_path))
        dump_log("YML Path : {}".format(self.yml_path))
        try:
            self.read_tsv_data()
        except:
            traceback.print_exc()
            sys.exit(1)
        print(self.l_domain_gene)

    def read_tsv_data(self):
        with open(self.tsv_path, "r") as f:
            d_tsv = f.read()
        l_row = d_tsv.split("\n")
        for row in l_row:
            l_ele = row.split()
            if len(row.split()) >= 4:
                self.l_domain_gene.append([l_ele[0], l_ele[3]])
        if len(self.l_domain_gene) >= 11:
            self.l_domain_gene = self.l_domain_gene[3:-7]

        return True

#
#
#
#
#
#
#
#
#
#
#
# def get_domain_gene_name(tsv_hmmer_output):
#
#
#
# def count_gene_domain(l_domain_gene):
#     gene_domain = defaultdict(list)
#     for [domain, gene] in l_domain_gene:
#         gene_domain[gene].append(domain)
#
#     return gene_domain
#
#
# def split_l_gene(motif_yaml_path, l_gene):
#     with open(motif_yaml_path, "r") as f:
#         data_yml = f.read()
#     d_yml = yaml.load(data_yml)
#     gene_1 = set(d_yml["GENE"]["1ST"])
#     gene_2 = set(d_yml["GENE"]["2ND"])
#
#     count_1 = 0
#     count_2 = 0
#
#     for gene in l_gene:
#         if gene in gene_1:
#             count_1 += 1
#         elif gene in gene_2:
#             count_2 += 1
#         else:
#             print(gene)
#
#     l_count = [len(gene_1), count_1, len(gene_2), count_2]
#
#     return l_count
#
#
# def main():
#     print("=== HMMER output analysis start ===")
#     print("=== Your input ===")
#     hmm_output_path = os.path.abspath(sys.argv[1])
#     motif_yaml_path = os.path.abspath(sys.argv[2])
#     print("HMMER output tsv file path : {}".format(hmm_output_path))
#     print("Domain yaml file : {}".format(motif_yaml_path))
#     print("\n")
#
#     l_domain_gene = get_domain_gene_name(tsv_hmmer_output)
#     gene_domain = count_gene_domain(l_domain_gene)
#
#
#     with open(hmm_output_path, "r") as f:
#         tsv_hmmer_output = f.read()
#     l_domain_gene = get_domain_gene_name(tsv_hmmer_output)
#     gene_domain = count_gene_domain(l_domain_gene)
#
#     print("=== Found Gene list and domain ===")
#     for key, value in gene_domain.items():
#         print("{} : {}".format(key, value))
#
#     l_gene = list(gene_domain.keys())
#     l_count = split_l_gene(motif_yaml_path, l_gene)
#
#     TP = l_count[3]
#     FP = l_count[1]
#     FN = l_count[2] - l_count[3]
#     TN = l_count[0] - l_count[1]
#
#     print("\n")
#     print("=== 2 * 2 contingency table ===")
#     print("|-----------|-------|-------|")
#     print("|-----------|   2nd |   1st |")
#     print("|-----------|-------|-------|")
#     print("| Found     | {:>5} | {:>5} |".format(str(TP), str(FP)))
#     print("| Not Found | {:>5} | {:>5} |".format(str(FN), str(TN)))
#     print("|-----------|-------|-------|")
#     print("Precision : {}".format(TP / (TP + FP)))
#     print("Recall : {}".format(TP / (TP + FN)))


def main():
    my_kphmmer_stat = KphmmerStat()
    my_kphmmer_stat.run(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()

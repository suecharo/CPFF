#!/bin/env python
# coding: utf-8
"""
KPHMMER でそれぞれの API を叩いた回数を表示するバージョン
$ python3 KPHMMER_API-access.py で普通の使い方
"""
import sys
import traceback
from collections import defaultdict

from KPHMMER import (Analysis, Config, Convert, Query, Search,
                     determine_submethod, get_args)

from .util import check_status_code, dump_log, get_kegg, get_pfam


class QueryCount(Query):
    def __init__(self, args=None):
        super().__init__()
        self.kegg_count = 0

    def _search_pathway(self):
        dump_log("Start searching pathway")
        for organism in self.l_organism_code:
            endpoint = "/list/pathway/{}".format(organism)
            status_code, text = get_kegg(endpoint)
            self.kegg_count += 1
            msg = "Query organism code {} is wrong.".format(organism)
            if check_status_code(status_code, msg):
                self.d_organism[organism] = dict()
                self.d_organism[organism]["pathway"] = []
                for row in text.split("\n"):
                    ele = row.split("\t")[0]
                    pathway_id = ele[-5:]
                    if pathway_id != "":
                        self.d_organism[organism]["pathway"].append(pathway_id)

        return True

    def _find_gene(self):
        dump_log("Start finding genes")
        for organism, value in self.d_organism.items():
            endpoint = "/link/{}/pathway".format(organism)
            status_code, text = get_kegg(endpoint)
            self.kegg_count += 1
            msg = "This endpoint {} is Nothing.".format(endpoint)
            d_path_to_gene = defaultdict(list)
            if check_status_code(status_code, msg):
                for row in text.split("\n"):
                    l_ele = row.split("\t")
                    if len(l_ele) < 2:
                        continue
                    d_path_to_gene[l_ele[0]].append(l_ele[1])

            s_1st_gene = set()
            s_2nd_gene = set()
            for name in ["1st", "2nd"]:
                for pathway_id in value["{}_pathway".format(name)]:
                    l_gene_id = d_path_to_gene[pathway_id]
                    for gene_id in l_gene_id:
                        if name == "1st":
                            s_1st_gene.add(gene_id)
                        elif name == "2nd":
                            s_2nd_gene.add(gene_id)
            s_duplicate = s_1st_gene & s_2nd_gene

            len_1 = len(s_1st_gene)
            len_2 = len(s_2nd_gene)
            len_dup = len(s_duplicate)
            dump_log("{0}'s 1st gene count : {1}".format(organism, len_1))
            dump_log("{0}'s 2nd gene count : {1}".format(organism, len_2))
            msg = "{0}'s duplicate gene count : {1}".format(organism, len_dup)
            dump_log(msg)

            if self.d_config["CONFIG"]["INSERT_DUPLICATE"] == "1st":
                s_2nd_gene = s_2nd_gene - s_duplicate
            elif self.d_config["CONFIG"]["INSERT_DUPLICATE"] == "2nd":
                s_1st_gene = s_1st_gene - s_duplicate
            else:
                msg = "Please check your config.yml-INSERT_DUPLICATE"
                raise ValueError(msg)

            self.d_organism[organism]["1st_gene"] = list(s_1st_gene)
            self.d_organism[organism]["2nd_gene"] = list(s_2nd_gene)
            self.d_organism[organism]["duplicate_gene"] = list(s_duplicate)

        return True

    def _find_domain(self):
        dump_log("Start finding pathways")
        for organism, value in self.d_organism.items():
            dump_log("Organism : {}".format(organism))
            self.d_organism[organism]["d_domain"] = dict()
            all_gene = value["1st_gene"] + value["2nd_gene"]
            group_num = 10
            dump_log("Number of genes : {}".format(len(all_gene)))
            count = 0
            for i in range(0, len(all_gene), group_num):
                count += 10
                dump_log("{} / {}".format(count, len(all_gene)))
                chunk = all_gene[i:i + group_num]
                endpoint = "/get/{}".format("+".join(chunk))
                status_code, text = get_kegg(endpoint)
                self.kegg_count += 1
                msg = "This endpoint {} is Nothing.".format(endpoint)
                if check_status_code(status_code, msg):
                    l_text = text.split("//")
                    for j in range(len(chunk)):
                        gene = chunk[j]
                        ele_text = l_text[j]
                        l_domain = []
                        b_domain = False
                        for row in ele_text.split("\n"):
                            if len(row) < 5:
                                continue
                            if b_domain is True:
                                if row[0] != " ":
                                    break
                                else:
                                    l_row = row.split(" ")
                            else:
                                if row[:5] == "MOTIF":
                                    b_domain = True
                                    l_row = row.split(" ")
                                else:
                                    continue
                            for ele in l_row:
                                if ele in ["MOTIF", "", "Pfam:"]:
                                    continue
                                else:
                                    l_domain.append(ele)
                        self.d_organism[organism]["d_domain"][gene] = l_domain

        return True


class ConvertCount(Convert):
    def __init__(self, args=None):
        super().__init__()
        self.kegg_count = 0

    def _dump_fasta(self):
        dump_log("Start dumping fasta files")
        for organism, value in self.d_domain.items():
            dump_log("Organism : {}".format(organism))
            gene_1st = value["gene_1st"]
            gene_2nd = value["gene_2nd"]
            l_fasta_1st = []
            l_fasta_2nd = []
            l_fasta_all = []
            group_num = 10
            len_gene = len(gene_1st) + len(gene_2nd)
            dump_log("Number of genes : {}".format(len_gene))
            count = 0
            for i in range(0, len(gene_1st), group_num):
                count += 10
                dump_log("{} / {}".format(count, len_gene))
                chunk = gene_1st[i:i + group_num]
                endpoint = "/get/{}/aaseq".format("+".join(chunk))
                status_code, text = get_kegg(endpoint)
                self.kegg_count += 1
                msg = "This endpoint {} is Nothing.".format(endpoint)
                if check_status_code(status_code, msg):
                    l_fasta = []
                    l_content = []
                    for row in text.split("\n"):
                        if len(row) == 0:
                            continue
                        if row[0] == ">":
                            if len(l_content) != 0:
                                amino = "".join(l_content)
                                l_fasta.append(amino)
                                l_content = []
                                l_fasta.append(row)
                            else:
                                l_fasta.append(row)
                        else:
                            l_content.append(row)
                    else:
                        if len(l_content) != 0:
                            amino = "".join(l_content)
                            l_fasta.append(amino)
                    l_fasta_1st.extend(l_fasta)
                    l_fasta_all.extend(l_fasta)

            count = len(gene_1st)
            for i in range(0, len(gene_2nd), group_num):
                count += 10
                dump_log("{} / {}".format(count, len_gene))
                chunk = gene_2nd[i:i + group_num]
                endpoint = "/get/{}/aaseq".format("+".join(chunk))
                status_code, text = get_kegg(endpoint)
                self.kegg_count += 1
                msg = "This endpoint {} is Nothing.".format(endpoint)
                if check_status_code(status_code, msg):
                    l_fasta = []
                    l_content = []
                    for row in text.split("\n"):
                        if len(row) == 0:
                            continue
                        if row[0] == ">":
                            if len(l_content) != 0:
                                amino = "".join(l_content)
                                l_fasta.append(amino)
                                l_content = []
                                l_fasta.append(row)
                            else:
                                l_fasta.append(row)
                        else:
                            l_content.append(row)
                    else:
                        if len(l_content) != 0:
                            amino = "".join(l_content)
                            l_fasta.append(amino)
                    l_fasta_2nd.extend(l_fasta)
                    l_fasta_all.extend(l_fasta)

            fasta_1st = "\n".join(l_fasta_1st)
            fasta_2nd = "\n".join(l_fasta_2nd)
            fasta_all = "\n".join(l_fasta_all)
            for (fa, name) in [[fasta_1st, "1st"], [fasta_2nd, "2nd"],
                               [fasta_all, "all"]]:
                file_name = "{}_{}.fasta".format(organism, name)
                file_path = self.output.joinpath(file_name)
                with file_path.open(mode="w") as f:
                    f.write(fa)

        return True


class AnalysisCount(Analysis):
    def __init__(self, args=None):
        super().__init__()
        self.pfam_count = 0

    def _dump_hmm(self):
        dump_log("Start dumping hmm files")
        for category in ["1st", "2nd"]:
            dump_log("Start {} category".format(category))
            if category == "1st":
                use_dict = self.d_count_1st
            elif category == "2nd":
                use_dict = self.d_count_2nd
            dir_name = "{}_{}".format("_".join(self.d_domain.keys()), category)
            dir_path = self.output.joinpath(dir_name)
            dir_path.mkdir(parents=True)
            dump_log("Number of domains : {}".format(len(use_dict.keys())))
            count = 0
            for domain in use_dict.keys():
                count += 1
                dump_log("{} : {}".format(count, domain))
                endpoint = "/family/{}/hmm".format(domain)
                status_code, text = get_pfam(endpoint)
                self.pfam_count += 1
                msg = "input domain {} is not found.".format(domain)
                if check_status_code(status_code, msg):
                    file_path = dir_path.joinpath("{}.hmm".format(domain))
                    with file_path.open(mode="w") as f:
                        f.write(text)

        return True


def main():
    args = get_args()
    submethod = determine_submethod(args)
    if submethod is False:
        get_args(usage=True)

    try:
        if submethod == "query":
            my_submethod = Query(args)
            kegg = "KEGG API access count : {}".format(my_submethod.kegg_count)
            dump_log(kegg)
        elif submethod == "search":
            my_submethod = Search(args)
        elif submethod == "analysis":
            my_submethod = Analysis(args)
            pfam = "Pfam API access count : {}".format(my_submethod.pfam_count)
            dump_log(pfam)
        elif submethod == "convert":
            my_submethod = Convert(args)
            kegg = "KEGG API access count : {}".format(my_submethod.kegg_count)
            dump_log(kegg)
        elif submethod == "config":
            my_submethod = Config(args)
        my_submethod.run()
    except:
        traceback.print_exc()
        sys.exit(1)

    return True


if __name__ == "__main__":
    main()

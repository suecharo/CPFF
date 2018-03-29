#!/usr/bin/env python
# coding: utf-8
from pathlib import Path

import yaml

from .util import check_status_code, dump_log, get_kegg


class Convert:
    def __init__(self, args):
        self.l_domain_file = args.convert_domain_file
        self.output = Path.cwd().joinpath(args.output).resolve()
        if self.output.is_dir() is False:
            self.output.mkdir(parents=True)

        self.d_domain = dict()

    def run(self):
        dump_log("=== Starting Convert method ===")
        self._comfirm_domain_file()
        self._read_domain()
        self._dump_fasta()
        dump_log("=== Convert method finished ===")

        return True

    def _comfirm_domain_file(self):
        """
        Configirm existence of l_domain_file and obtain absolute path.
        """
        dump_log("Start Comfirming domain file ")
        l_domain = []
        for domain in self.l_domain_file:
            domain = Path(domain)
            if domain.is_absolute is False:
                domain = Path.cwd().joinpath(domain).resolve()
            if domain.suffix != ".yml":
                msg = "Your input {} is not yaml file".format(domain)
                raise ValueError(msg)
            if domain.exists is False:
                msg = "Your input {} is not found".format(domain)
                raise ValueError(msg)
            l_domain.append(domain)

        self.l_domain_file = l_domain

        return True

    def _read_domain(self):
        """
        d_domain
        sco :
            category_1st : ["1.1", "1.2"]
            category_2nd : ["1.3", "1.4"]
            duplicate : 2nd
            gene_1st : [...]
            gene_2nd : [...]
            domain :
                sco:SC00063 : [hoge]
                ...
        sma :
            ...
        """
        dump_log("Start reading domains")
        for domain in self.l_domain_file:
            with domain.open(mode="r") as f:
                data = yaml.load(f)
            organism = data["CONFIG"]["ORGANISM"]
            category_1st = data["CONFIG"]["1ST_CATEGORY"]
            category_2nd = data["CONFIG"]["2ND_CATEGORY"]
            duplicate = data["CONFIG"]["INSERT_DUPLICATE"]
            gene_1st = data["GENE"]["1ST"]
            gene_2nd = data["GENE"]["2ND"]
            domain = data["DOMAIN"]
            self.d_domain[organism] = dict()
            self.d_domain[organism]["category_1st"] = category_1st
            self.d_domain[organism]["category_2nd"] = category_2nd
            self.d_domain[organism]["duplicate"] = duplicate
            self.d_domain[organism]["gene_1st"] = gene_1st
            self.d_domain[organism]["gene_2nd"] = gene_2nd
            self.d_domain[organism]["domain"] = domain

        return True

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

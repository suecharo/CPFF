#!/usr/bin/env python
# coding: utf-8
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import yaml

from .analysis import Analysis
from .config_file_manager import ConfigFileManager
from .util import check_status_code, dump_log, get_kegg


class Query:
    def __init__(self, args):
        self.args = args

        self.l_organism_code = args.organism_code
        self.output = Path.cwd().joinpath(args.output).resolve()
        if self.output.is_dir() is False:
            self.output.mkdir(parents=True)
        self.with_analysis = args.with_analysis

        self.d_organism = dict()

        my_config_file_manager = ConfigFileManager()
        self.d_config = my_config_file_manager.read_config()
        self.l_1st_pathway_id = []
        self.l_2nd_pathway_id = []
        for category_num in self.d_config["CONFIG"]["1ST_CATEGORY"]:
            l_ids = self.d_config["PATHWAY_ID"][category_num]
            self.l_1st_pathway_id.extend(l_ids)
        for category_num in self.d_config["CONFIG"]["2ND_CATEGORY"]:
            l_ids = self.d_config["PATHWAY_ID"][category_num]
            self.l_2nd_pathway_id.extend(l_ids)

        self.l_domain_file = []

    def run(self):
        dump_log("=== Starting Query method ===")
        dump_log("Your query : {}".format(self.l_organism_code))
        self._search_pathway()
        self._format_pathway()
        self._find_gene()
        self._find_domain()
        self._dump_domain_file()
        dump_log("=== Query method finished ===")
        if self.with_analysis is True:
            my_analysis = Analysis()
            my_analysis.l_domain_file = self.l_domain_file
            my_analysis.output = self.output
            my_analysis.run()

        return True

    def _search_pathway(self):
        """
        Search for the pathway that each creature has.
        Here the pathway is a str type number like "00010".
        self.d_organism :
            hsa :
                pathway : create here
            sco :
                ...
        """
        dump_log("Start searching pathway")
        for organism in self.l_organism_code:
            endpoint = "/list/pathway/{}".format(organism)
            status_code, text = get_kegg(endpoint)
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

    def _format_pathway(self):
        """
        Information obtained from config.yml is divided into l_1st and l_2nd.
        The pathway not specified in config.yml is excluded.
        self.d_organism :
            hsa :
                pathway :
                1st_pathway : create here
                2nd_pathway : create here
            sco :
                ...
        """
        dump_log("Start formatting pathways")
        for organism, value in self.d_organism.items():
            l_1st = list(set(self.l_1st_pathway_id) & set(value["pathway"]))
            l_2nd = list(set(self.l_2nd_pathway_id) & set(value["pathway"]))
            l_1st = ["path:{0}{1}".format(organism, p_id) for p_id in l_1st]
            l_2nd = ["path:{0}{1}".format(organism, p_id) for p_id in l_2nd]
            self.d_organism[organism]["1st_pathway"] = l_1st
            self.d_organism[organism]["2nd_pathway"] = l_2nd
            len_1 = len(l_1st)
            len_2 = len(l_2nd)
            dump_log("{0}'s 1st pathway count : {1}".format(organism, len_1))
            dump_log("{0}'s 2nd pathway count : {1}".format(organism, len_2))

        return True

    def _find_gene(self):
        """
        Search for genes contained in each pathway.
        The duplicated gene enters the one specified by config.yml.
        self.d_organism :
            hsa :
                pathway :
                1st_pathway :
                2nd_pathway :
                1st_gene : create here
                2nd_gene : create here
                duplicate_gene : create here
            sco :
                ...
        """
        dump_log("Start finding genes")
        for organism, value in self.d_organism.items():
            endpoint = "/link/{}/pathway".format(organism)
            status_code, text = get_kegg(endpoint)
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
        """
        Find pfam domain.
        self.d_organism :
            hsa :
                pathway :
                1st_pathway :
                2nd_pathway :
                1st_gene :
                2nd_gene :
                duplicate_gene :
                d_domain : create now
                    gene_id : domain list
            sco :
                ...
        """
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

    def _dump_domain_file(self):
        """
        Output gene and pfam as ${output_dir}/${organism}.yml
        CONFIG :
            ORGANISM : sco
            1ST_LIST :
                - 1.1
                - 1.2
                - ...
            2ND_LIST :
                - 1.9
                - ...
            INSERT_DUPLICATE : "2nd"
            CREATE_DATE : 2018/02/01 00:00:00
        PATHWAY :
            1ST :
                - sco19291
                - ...
            2ND :
                - ...
        GENE :
            1ST :
                - SCO1931
                - SCO2382
                - ...
            2ND :
                - SCO7290
                - ...
        DOMAIN :
            SCO1931 : ['Rieske', 'Phage_holin_3_6', 'Bac_export_2']
            ...
        """
        dump_log("Start dumping domain files")
        for organism, value in self.d_organism.items():
            d_write = dict()
            d_write["CONFIG"] = dict()
            d_write["CONFIG"]["ORGANISM"] = organism
            d_write["CONFIG"]["1ST_CATEGORY"] = \
                self.d_config["CONFIG"]["1ST_CATEGORY"]
            d_write["CONFIG"]["2ND_CATEGORY"] = \
                self.d_config["CONFIG"]["2ND_CATEGORY"]
            d_write["CONFIG"]["INSERT_DUPLICATE"] = \
                self.d_config["CONFIG"]["INSERT_DUPLICATE"]
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            d_write["CONFIG"]["CREATE_DATE"] = now
            d_write["PATHWAY"] = dict()
            p_1st = [organism + p_id for p_id in value["1st_pathway"]]
            p_2nd = [organism + p_id for p_id in value["2nd_pathway"]]
            d_write["PATHWAY"]["1ST"] = p_1st
            d_write["PATHWAY"]["2ND"] = p_2nd
            d_write["GENE"] = dict()
            d_write["GENE"]["1ST"] = value["1st_gene"]
            d_write["GENE"]["2ND"] = value["2nd_gene"]
            d_write["DOMAIN"] = value["d_domain"]

            file_name = "{}.yml".format(organism)
            file_path = self.output.joinpath(file_name)
            with file_path.open(mode="w") as f:
                credit = "# Created by KPHMMER " +\
                         "<https://github.com/suecharo/KPHMMER>\n"
                f.write(credit)
                f.write(yaml.dump(d_write))
            self.l_domain_file.append(file_path)

        return True

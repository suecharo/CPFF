#!/usr/bin/env python
# coding: utf-8
from pathlib import Path

import numpy
import yaml
from scipy import stats

from .config_file_manager import ConfigFileManager
from .util import check_status_code, dump_log, get_pfam


class Analysis:
    def __init__(self, args=None):
        if args is not None:
            self.l_domain_file = args.analysis_domain_file
            self.output = Path.cwd().joinpath(args.output).resolve()
            if self.output.is_dir() is False:
                self.output.mkdir(parents=True)

        self.d_domain = dict()
        self.d_count = dict()
        self.g_count_1 = 0
        self.g_count_2 = 0
        self.d_count_1st = dict()
        self.d_count_2nd = dict()

        my_config_file_manager = ConfigFileManager()
        self.d_config = my_config_file_manager.read_config()

    def run(self):
        dump_log("=== Starting Analysis method ===")
        self._comfirm_domain_file()
        self._read_domain()
        self._count_domain()
        self._stat_domain()
        self._dump_tsv()
        self._dump_hmm()
        dump_log("=== Analysis method finished ===")

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

    def _count_domain(self):
        """
        d_domain
        sco :
            category_1st : ["1.1", "1.2"]
            category_2nd : ["1.3", "1.4"]
            duplicate : 2nd
            gene_1st : [...]
            gene_2nd : [...]
            domain :
                sco:SC00063 : [ROK, Beta-lactamase2]
                ...
        sma :
            ...

        d_count
        ROK :
            1st_count : 10
            2nd_count : 5
            1st_frequency : 0.5000
            2nd_frequency : 0.5000
        Beta-lactamase2
        """
        dump_log("Start counting domain")
        for organism, value in self.d_domain.items():
            for gene_id in value["gene_1st"]:
                self.g_count_1 += 1
                l_domain = value["domain"][gene_id]
                for domain in l_domain:
                    if domain not in self.d_count.keys():
                        self.d_count[domain] = dict()
                        self.d_count[domain]["1st_count"] = 1
                        self.d_count[domain]["2nd_count"] = 0
                    else:
                        self.d_count[domain]["1st_count"] += 1

            for gene_id in value["gene_2nd"]:
                self.g_count_2 += 1
                l_domain = value["domain"][gene_id]
                for domain in l_domain:
                    if domain not in self.d_count.keys():
                        self.d_count[domain] = dict()
                        self.d_count[domain]["1st_count"] = 0
                        self.d_count[domain]["2nd_count"] = 1
                    else:
                        self.d_count[domain]["2nd_count"] += 1

        return True

    def _stat_domain(self):
        """
        Perform a chi-square test.
        The significance level is 5%.
        If a value less than to the expected value 5 exists, it is excluded
        Perform residual analysis and divide into 1st and 2nd.
        """
        dump_log("Start calculating domain stats")
        for domain, value in self.d_count.items():
            count_1 = value["1st_count"]
            count_2 = value["2nd_count"]
            count_no_1 = self.g_count_1 - count_1
            count_no_2 = self.g_count_2 - count_2
            data = \
                numpy.array([[count_1, count_2], [count_no_1, count_no_2]])
            x2, p, dof, exp = stats.chi2_contingency(data)
            self.d_count[domain]["p_value"] = p
            if p < self.d_config["CONFIG"]["THRESHOLD_P_VALUE"]:
                l_exp = list(exp.ravel())
                b_check = False
                for num_exp in l_exp:
                    if num_exp <= self.d_config["CONFIG"]["COCHRAN_RULE"]:
                        b_check = True
                        break
                if b_check:
                    continue
                res = data - exp
                res_var = numpy.zeros(res.shape)
                it = numpy.nditer(data, flags=["multi_index"])
                d_sum = data.sum()
                while not it.finished:
                    var = (1 - (data[:, it.multi_index[1]].sum() / d_sum)) * \
                          (1 - (data[it.multi_index[0], :].sum() / d_sum))
                    res_var[it.multi_index[0], it.multi_index[1]] = var
                    it.iternext()
                stdres = res / numpy.sqrt(exp * res_var)
                if stdres[0][0] >= 1.96:
                    self.d_count_1st[domain] = dict()
                    self.d_count_1st[domain]["1st_count"] = count_1
                    self.d_count_1st[domain]["2nd_count"] = count_2
                    self.d_count_1st[domain]["p_value"] = p
                if stdres[0][1] >= 1.96:
                    self.d_count_2nd[domain] = dict()
                    self.d_count_2nd[domain]["1st_count"] = count_1
                    self.d_count_2nd[domain]["2nd_count"] = count_2
                    self.d_count_2nd[domain]["p_value"] = p

        return True

    def _dump_tsv(self):
        dump_log("Start dumping tsv files")
        header = "Pfam_domain\t" +\
            "1st_count({})\t".format(self.g_count_1) +\
            "2nd_count({})\t".format(self.g_count_2) +\
            "p_value\n"
        for category in ["all", "1st", "2nd"]:
            if category == "all":
                use_dict = self.d_count
            elif category == "1st":
                use_dict = self.d_count_1st
            elif category == "2nd":
                use_dict = self.d_count_2nd
            file_name = "{0}_{1}.tsv".format("_".join(self.d_domain.keys()),
                                             category)
            file_path = self.output.joinpath(file_name)
            with file_path.open(mode="w") as f:
                f.write(header)
                for domain, value in use_dict.items():
                    l_write = [domain]
                    l_write.append(value["1st_count"])
                    l_write.append(value["2nd_count"])
                    l_write.append(value["p_value"])
                    items = "\t".join(map(str, l_write)) + "\n"
                    f.write(items)

        return True

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
                msg = "input domain {} is not found.".format(domain)
                if check_status_code(status_code, msg):
                    file_path = dir_path.joinpath("{}.hmm".format(domain))
                    with file_path.open(mode="w") as f:
                        f.write(text)

        return True

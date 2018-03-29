#!/usr/bin
# coding: utf-8
from pathlib import Path

import yaml

HELP_MESSAGE = "help_message.yml"
CONFIG = "config.yml"
CONFIG_DIST = "config.yml-dist"


class ConfigFileManager:
    def __init__(self):
        self.file = Path(__file__)
        self.config_dir_path = self.file.parents[0].joinpath("config_files")

    def get_help_message_path(self):
        help_message_path = self.config_dir_path.joinpath(HELP_MESSAGE)
        if help_message_path.exists() is False:
            raise OSError("Help Message file is not found.")

        return help_message_path

    def get_config_file_path(self):
        config_file_path = self.config_dir_path.joinpath(CONFIG)
        if config_file_path.exists() is False:
            raise OSError("Config file is not found.")

        return config_file_path

    def read_config(self):
        # d_config["CONFIG"]["1ST_CATEGORY"]
        # d_config["CONFIG"]["2ND_CATEGORY"]
        # d_config["CONFIG"]["INSERT_DUPLICATE"]
        # d_config["CONFIG"]["KEGG_URL_BASE"]
        # d_config["CONFIG"]["PFAM_URL_BASE"]
        # d_config["CONFIG"]["WAIT_TIME"]
        # for category_num in d_config["CONFIG"]["1ST_CATEGORY"]:
        #     l_1st_pathway_id.extend(d_config["PATHWAY_ID"][category_num])
        # for category_num in d_config["CONFIG"]["2ND_CATEGORY"]:
        #     l_2nd_pathway_id.extend(d_config["PATHWAY_ID"][category_num])

        config_file_path = self.get_config_file_path()
        with open(config_file_path, "r") as f:
            d_config = yaml.load(f)

        return d_config

    def print_config(self):
        d_config = self.read_config()
        l_1st_category = d_config["CONFIG"]["1ST_CATEGORY"]
        l_2nd_category = d_config["CONFIG"]["2ND_CATEGORY"]
        insert_duplicate = d_config["CONFIG"]["INSERT_DUPLICATE"]
        print("1st category : {}".format(l_1st_category))
        print("2nd category : {}".format(l_2nd_category))
        print("Insert duplicate : {}".format(insert_duplicate))

        return True

    def set_value(self, l_1st_category_num=None,
                  l_2nd_category_num=None,
                  insert_duplicate=None):
        config_file_path = self.get_config_file_path()
        d_config = self.read_config()

        if l_1st_category_num is not None:
            d_config["CONFIG"]["1ST_CATEGORY"] = l_1st_category_num
        if l_2nd_category_num is not None:
            d_config["CONFIG"]["2ND_CATEGORY"] = l_2nd_category_num
        if insert_duplicate is not None:
            d_config["CONFIG"]["INSERT_DUPLICATE"] = insert_duplicate

        with config_file_path.open(mode="w") as f:
            f.write(yaml.dump(d_config))

        self.print_config()

        return True

    def set_default(self):
        config_dist_file_path = self.config_dir_path.joinpath(CONFIG_DIST)
        if config_dist_file_path.exists() is False:
            raise OSError("Config dist file is not found.")
        with config_dist_file_path.open() as f:
            d_config_dist = yaml.load(f)

        l_1st = d_config_dist["CONFIG"]["1ST_CATEGORY"]
        l_2nd = d_config_dist["CONFIG"]["2ND_CATEGORY"]
        ins_dup = d_config_dist["CONFIG"]["INSERT_DUPLICATE"]

        self.set_value(l_1st_category_num=l_1st, l_2nd_category_num=l_2nd,
                       insert_duplicate=ins_dup)

        return True

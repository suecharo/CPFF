#!/usr/bin/env python
# coding: utf-8
"""
Parse the input.
"""
import argparse
import sys

import yaml

from .config_file_manager import ConfigFileManager


def get_args(usage=False):
    """
    Parse the input and return args.
    It also displays a help message.
    """
    config_file_manager = ConfigFileManager()
    help_message_path = config_file_manager.get_help_message_path()
    with open(help_message_path, "r") as f:
        d_help_message = yaml.load(f)

    desc_argparser = d_help_message["DESCRIPTION"]["ARGPARSER"]
    desc_subparser = d_help_message["DESCRIPTION"]["SUBPARSER"]
    desc_query = d_help_message["DESCRIPTION"]["QUERY"]
    desc_search = d_help_message["DESCRIPTION"]["SEARCH"]
    desc_analysis = d_help_message["DESCRIPTION"]["ANALYSIS"]
    desc_convert = d_help_message["DESCRIPTION"]["CONVERT"]
    desc_config = d_help_message["DESCRIPTION"]["CONFIG"]
    help_sub_query = d_help_message["SUBPARSER"]["QUERY"]
    help_sub_search = d_help_message["SUBPARSER"]["SEARCH"]
    help_sub_analysis = d_help_message["SUBPARSER"]["ANALYSIS"]
    help_sub_convert = d_help_message["SUBPARSER"]["CONVERT"]
    help_sub_config = d_help_message["SUBPARSER"]["CONFIG"]
    help_query_organism = d_help_message["QUERY"]["ORGANISM"]
    help_query_output = d_help_message["QUERY"]["OUTPUT"]
    help_query_analysis = d_help_message["QUERY"]["ANALYSIS"]
    help_search_query = d_help_message["SEARCH"]["QUERY"]
    help_search_all = d_help_message["SEARCH"]["ALL"]
    help_analysis_domain = d_help_message["ANALYSIS"]["DOMAIN"]
    help_analysis_output = d_help_message["ANALYSIS"]["OUTPUT"]
    help_convert_domain = d_help_message["CONVERT"]["DOMAIN"]
    help_convert_output = d_help_message["CONVERT"]["OUTPUT"]
    help_config_default = d_help_message["CONFIG"]["DEFAULT"]
    help_config_1st = d_help_message["CONFIG"]["1ST"]
    help_config_2nd = d_help_message["CONFIG"]["2ND"]
    help_config_duplicate = d_help_message["CONFIG"]["DUPLICATE"]

    parser = argparse.ArgumentParser(description=desc_argparser)
    subparser = parser.add_subparsers(help=desc_subparser)

    query_parser = subparser.add_parser("query",
                                        description=desc_query,
                                        help=help_sub_query)
    query_parser.add_argument("organism_code",
                              nargs="+",
                              type=str,
                              help=help_query_organism,
                              metavar="CODE")
    query_parser.add_argument("-o",
                              "--output",
                              nargs="?",
                              default=".",
                              type=str,
                              help=help_query_output)
    query_parser.add_argument("-a",
                              "--with-analysis",
                              action="store_true",
                              help=help_query_analysis)

    search_parser = subparser.add_parser("search",
                                         description=desc_search,
                                         help=help_sub_search)
    search_group = search_parser.add_mutually_exclusive_group(required=True)
    search_group.add_argument("search_query",
                              nargs="?",
                              const=None,
                              type=str,
                              help=help_search_query,
                              metavar="STRING")
    search_group.add_argument("-a",
                              "--show-all",
                              action="store_true",
                              help=help_search_all)

    analysis_parser = subparser.add_parser("analysis",
                                           description=desc_analysis,
                                           help=help_sub_analysis)
    analysis_parser.add_argument("analysis_domain_file",
                                 nargs="+",
                                 type=str,
                                 help=help_analysis_domain,
                                 metavar="DOMAIN")
    analysis_parser.add_argument("-o",
                                 "--output",
                                 nargs="?",
                                 default=".",
                                 type=str,
                                 help=help_analysis_output,
                                 metavar="OUTPUT")

    convert_parser = subparser.add_parser("convert",
                                          description=desc_convert,
                                          help=help_sub_convert)
    convert_parser.add_argument("convert_domain_file",
                                nargs="+",
                                type=str,
                                help=help_convert_domain,
                                metavar="DOMAIN")
    convert_parser.add_argument("-o",
                                "--output",
                                nargs="?",
                                default=".",
                                type=str,
                                help=help_convert_output,
                                metavar="OUTPUT")

    config_parser = subparser.add_parser("config",
                                         description=desc_config,
                                         help=help_sub_config)
    config_parser.add_argument("-s",
                               "--set-default",
                               action="store_true",
                               help=help_config_default)
    config_parser.add_argument("-1",
                               "--category-1st",
                               nargs="+",
                               type=str,
                               help=help_config_1st)
    config_parser.add_argument("-2",
                               "--category-2nd",
                               nargs="+",
                               type=str,
                               help=help_config_2nd)
    config_parser.add_argument("-d",
                               "--duplicate",
                               nargs="?",
                               choices=["1st", "2nd"],
                               help=help_config_duplicate)

    if usage is True:
        print(parser.format_help())
        sys.exit(1)
    else:
        args = parser.parse_args()
        return args


def determine_submethod(args):
    """
    Determine the submethod.
    """
    submethod = False
    if "organism_code" in args:
        submethod = "query"
    elif "search_query" in args:
        submethod = "search"
    elif "analysis_domain_file" in args:
        submethod = "analysis"
    elif "convert_domain_file" in args:
        submethod = "convert"
    elif "duplicate" in args:
        submethod = "config"

    return submethod

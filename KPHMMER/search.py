#!/usr/bin/env python
# coding: utf-8
from .util import check_status_code, dump_log, get_kegg


class Search:
    def __init__(self, args):
        self.search_query = args.search_query
        self.b_show_all = args.show_all

    def run(self):
        dump_log("=== Starting Search method ===")
        if self.b_show_all is True:
            self._show_all()
        else:
            self._ordinaly_search()
        dump_log("=== Search method finished ===")

        return True

    def _show_all(self):
        dump_log("Start showing all items")
        endpoint = "/list/organism"
        status_code, text = get_kegg(endpoint)
        msg = "method is show all."
        if check_status_code(status_code, msg):
            print(text)

        return True

    def _ordinaly_search(self):
        dump_log("Start ordinaly search method")
        endpoint = "/find/genome/{}".format(self.search_query)
        status_code, text = get_kegg(endpoint)
        msg = "Your query [{}] is wrong.".format(self.search_query)
        if check_status_code(status_code, msg):
            print(text)

        return True

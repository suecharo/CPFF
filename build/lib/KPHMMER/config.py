#!/usr/bin/env python
# coding: utf-8
from .config_file_manager import ConfigFileManager
from .util import dump_log


class Config:
    def __init__(self, args):
        self.ins_dup = args.duplicate
        self.l_1st = args.category_1st
        self.l_2nd = args.category_2nd
        self.b_set_default = args.set_default
        self.b_check = False
        if self.b_set_default is True:
            if any([self.ins_dup, self.l_1st, self.l_2nd]):
                msg = "argument -s can not be used with other options"
                raise ValueError(msg)
        else:
            if any([self.ins_dup, self.l_1st, self.l_2nd]) is False:
                self.b_check = True

    def run(self):
        dump_log("=== Starting Config method ===")
        if self.b_check is True:
            self._print_config()
        else:
            if self.b_set_default is True:
                self._set_default()
            else:
                self._set_value()
        dump_log("=== Config method finished ===")

        return True

    def _print_config(self):
        dump_log("Start printing config state")
        my_config_file_manager = ConfigFileManager()
        my_config_file_manager.print_config()

        return True

    def _set_default(self):
        dump_log("Start set default values")
        my_config_file_manager = ConfigFileManager()
        my_config_file_manager.set_default()

        return True

    def _set_value(self):
        dump_log("Start set values")
        my_config_file_manager = ConfigFileManager()
        my_config_file_manager.set_value(l_1st_category_num=self.l_1st,
                                         l_2nd_category_num=self.l_2nd,
                                         insert_duplicate=self.ins_dup)

        return True

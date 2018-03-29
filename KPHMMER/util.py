#!/usr/bin/env python
# coding: utf-8
import time
from datetime import datetime

import requests

from .config_file_manager import ConfigFileManager


def dump_log(msg):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print("[{}] {}".format(now, msg), flush=True)

    return True


def get_kegg(endpoint):
    my_config_file_manager = ConfigFileManager()
    d_config = my_config_file_manager.read_config()
    time.sleep(d_config["CONFIG"]["WAIT_TIME"])
    url = d_config["CONFIG"]["KEGG_URL_BASE"] + endpoint
    ret = requests.get(url)
    status_code = ret.status_code
    text = ret.text

    return status_code, text


def get_pfam(endpoint):
    my_config_file_manager = ConfigFileManager()
    d_config = my_config_file_manager.read_config()
    time.sleep(d_config["CONFIG"]["WAIT_TIME"])
    url = d_config["CONFIG"]["PFAM_URL_BASE"] + endpoint
    ret = requests.get(url)
    status_code = ret.status_code
    text = ret.text

    return status_code, text


def check_status_code(status_code, msg):
    if status_code == 200:
        return True
    elif status_code == 400:
        raise ConnectionError(msg)
    elif status_code == 404:
        raise ValueError(msg)
    else:
        raise ConnectionError("status code is {}".format(status_code))

    return True

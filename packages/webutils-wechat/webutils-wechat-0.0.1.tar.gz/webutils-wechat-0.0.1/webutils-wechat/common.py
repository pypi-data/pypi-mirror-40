# -*- coding: utf-8 -*-

import os
import time


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sentinel = object


def now_ts():
    return int(time.time())


def nop():
    return

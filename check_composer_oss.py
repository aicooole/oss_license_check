#!/usr/bin/python

from helper import *

(MyHelper()
    .check_params()
    .get_composer_data()
    .get_license_info()
    .make_authors_file()
    .test_debug())

#!/usr/bin/ python
# -*- coding: utf-8 -*-
# Author YangHengyu
# creation date 2018-05-25

import codecs
import json
import random
import time
import os

import datetime

import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import config

HERE = os.path.abspath(os.path.dirname(__file__))


class AutoLearn:
    def __init__(self, account, password, subject):
        self._name = "AutoLearn"
        self.browser = self.enable_flash()
        self.account = account
        self.password = password
        self.subject = subject

        self.learning_status = {}

    


if __name__ == '__main__':
    auto_learn = AutoLearn(config.USER_NAME, config.PASSWORD, config.SUBJECT)
    auto_learn.go_login_page()
    auto_learn.login()
    time.sleep(2)
    auto_learn.courses_study()
    # auto_learn.write_comments()






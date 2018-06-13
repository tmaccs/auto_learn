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

    def go_login_page(self):
        browser = self.browser
        browser.get(config.START_URL)
        login_button = browser.find_element_by_class_name('login')
        login_button.click()
        time.sleep(2)

    def login(self):
        # found login elements
        input_username = self.browser.find_element_by_id("myusername")
        input_password = self.browser.find_element_by_id("mypassword")

        input_btn = self.browser.find_element_by_id("btnlogininput")

        time.sleep(1)
        input_username.click()
        input_username.clear()
        input_username.send_keys(self.account)

        input_password.click()
        input_password.clear()
        input_password.send_keys(self.password)

        time.sleep(1)
        input_btn.click()

        print '登录成功'

    def get_learning_status(self):
        self.learning_status[u'网上选课'] = 1

    def course_selection(self):
        go_course_center_btn = self.browser.find_element_by_xpath('//*[@id="ext-gen1140"]/div/a')
        on_search_subject = self.browser.find_element_by_id("txtkeyword")

        go_course_center_btn.click()
        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.element_to_be_clickable((By.ID, "txtkeyword")))

        # 搜索对应科目的课程
        on_search_subject.click()
        on_search_subject.clear()
        on_search_subject.send_keys(self.subject)
        self.browser.find_element_by_name(u'确定').click()
        time.sleep(1)

    def courses_study(self):
        n = 0

        self.browser.find_element_by_xpath('//*[@id="ext-gen1142"]/div/a').click()
        self.browser.find_element_by_id('button-1034-btnInnerEl').click()

        browser = self.browser
        self.browser.get(config.STUDY_URL)
        time.sleep(1)

        # 切换到新页面
        current_handle = self.browser.current_window_handle

        for handle in self.browser.window_handles:
            if handle != current_handle:
                self.browser.switch_to.window(handle)

        # 点击课程学习按钮
        study_btn = self.browser.find_element_by_xpath('//*[@id="UpdatePanel1"]//td[4]/p[1]/a')
        study_btn.click()
        time.sleep(1)

        # 可能提示其他窗口有正在学习
        try:
            alert = self.browser.switch_to.alert
            # print alert.text
            alert.accept()
        except Exception as e:
            try:
                self.browser.switch_to.alert.accept()
            except Exception:
                time.sleep(1)
            print '时间：', datetime.datetime.now(), e
            time.sleep(1)

        time.sleep(2)
        self.write_comments()

        # 每15分钟会弹窗提示是否继续学习
        while n < 3300:
            # 每60秒检查一次有没有弹窗
            time.sleep(60)
            # 如果15分钟的警告框出来了，点击确定继续并且睡眠14分钟
            try:
                alert = self.browser.switch_to.alert
                print alert.text
                time.sleep(2)
                alert.accept()
                if alert.text == u'该课程已完成并获取学时！':
                    break
                time.sleep(600)
                n += 600
            except Exception as e:
                print '时间：', datetime.datetime.now(), e
                n += 60

        try:
            sys.exit(0)
        except:
            print('Program is dead.')
        finally:
            print('auto_learn_well_down')

    # 填写学习记录
    def write_comments(self):
        # 切换到弹窗iframe
        iframe = self.browser.find_element_by_id('lhgfrm_lhgdgId')
        self.browser.switch_to.frame(iframe)
        study_record_btn = self.browser.find_element_by_xpath('//*[@id="play"]/div[3]/div[1]/a[2]')
        study_record_btn.click()
        time.sleep(2)

        content_point_area = self.browser.find_element_by_id('txtareainnertContents')
        experience_area = self.browser.find_element_by_id('txtareaExperience')

        content_point = self.gen_comments('content_point')
        experience = self.gen_comments('experience')

        content_point_area.click()
        content_point_area.clear()
        content_point_area.send_keys(content_point)
        time.sleep(2)

        experience_area.click()
        experience_area.clear()
        experience_area.send_keys(experience)
        time.sleep(2)

        self.browser.find_element_by_id('btnaddRecord').click()
        time.sleep(5)
        self.browser.switch_to.alert.accept()

    def write_reading_notes(self):
        # current_handle = self.browser.current_window_handle
        #
        # for handle in self.browser.window_handles:
        #     if handle != current_handle:
        #         self.browser.switch_to.window(handle)

        # 点击读书评价
        self.browser.find_element_by_xpath('//*[@id="ext-gen1142"]/div/a').click()
        reading_note_frame = self.browser.find_element_by_id('fnode3')
        self.browser.switch_to.frame(reading_note_frame)
        # 点击新建
        self.browser.find_element_by_id('Paneldefault_panel_list_Grid_list_ctl00_CreatReadAss_btn-btnInnerEl').click()

    @staticmethod
    def enable_flash():
        # 设置默认启用flash
        chrome_options = Options()
        prefs = {
            "profile.managed_default_content_settings.images": 1,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        }

        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)

        return driver

    @staticmethod
    def gen_comments(comment_type='experience'):
        file_name = HERE + '/comments.json'
        try:
            with codecs.open(file_name, 'r', encoding='utf-8') as file:
                comments = json.loads(file.read())
        except Exception as e:
            print e
            raise

        comments_num = len(comments[comment_type])
        print comments_num
        i = random.randint(0, comments_num-1)

        return comments[comment_type][i]


if __name__ == '__main__':
    auto_learn = AutoLearn(config.USER_NAME, config.PASSWORD, config.SUBJECT)
    auto_learn.go_login_page()
    auto_learn.login()
    time.sleep(2)
    auto_learn.courses_study()
    # auto_learn.write_comments()






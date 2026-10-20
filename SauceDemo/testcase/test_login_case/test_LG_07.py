"""
用例名：用户名为空
编号：LG-07
预置条件：已打开登录页
测试步骤：
1.不填用户名；
2.密码输入 secret_sauce；
3.点击 Login
预期结果：
提示：Epic sadface: Username is required
"""
import logging

from playwright.sync_api import expect

from model.business.login import *
from model.business.productpage import *


def test_lg_07(page_start):
    url = Const.url
    page, pa = page_start(url)

    # # 预置条件
    logging.info('确认已处于登录页面')
    pa.check_text(title_page.type_name)

    # # 测试步骤
    logging.info('不输入账号，输入密码')
    pa.input_massage(pass_word, Const.password)

    logging.info('点击登录')
    pa.find_ele(login_button).click()

    # # 预期结果
    logging.info('检测页面提示文本是否出现')
    nou = pa.find_ele(no_username)
    expect(nou).to_be_visible()

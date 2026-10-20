"""
用例名：用户名密码都为空
编号：LG-09
预置条件：已打开登录页
测试步骤：
1.点击 Login
预期结果：
登录成功，跳转商品列表页
"""
import logging

from playwright.sync_api import expect

from model.business.login import *
from model.business.productpage import *


def test_lg_09(page_start):
    url = Const.url
    page, pa = page_start(url)

    # # 预置条件
    logging.info('确认已处于登录页面')
    pa.check_text(title_page.type_name)

    # # 测试步骤
    logging.info('点击登录')
    pa.find_ele(login_button).click()

    # # 预期结果
    logging.info('检测页面提示文本是否出现')
    nou = pa.find_ele(no_userpass)
    expect(nou).to_be_visible()

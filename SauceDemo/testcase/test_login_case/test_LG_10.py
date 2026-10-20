"""
用例名：用户名正确密码错误
编号：LG-10
预置条件：已打开登录页
测试步骤：
1.用户名输入 standard_user；
2.密码输入 123456；
3.点击 Login
预期结果：
提示：Username and password do not match any user in this service
"""
import logging

from playwright.sync_api import expect

from model.business.login import *
from model.business.productpage import *


def test_lg_10(page_start):
    url = Const.url
    page, pa = page_start(url)

    # # 预置条件
    logging.info('确认已处于登录页面')
    pa.check_text(title_page.type_name)

    # # 测试步骤
    logging.info('输入账号密码')
    pa.input_massage(user_name, Const.standard_user)
    pa.input_massage(pass_word, Const.error_user)

    logging.info('点击登录')
    pa.find_ele(login_button).click()

    # # 预期结果
    logging.info('检测页面提示文本是否出现')
    nou = pa.find_ele(password_ERR)
    expect(nou).to_be_visible()

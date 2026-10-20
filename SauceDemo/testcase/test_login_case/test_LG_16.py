"""
用例名：登录后退出登录
编号：LG-16
预置条件：已登录成功进入商品页
测试步骤：
1.点击左上角汉堡菜单
2.点击 Logout
预期结果：
成功返回登录页，账号信息清空
"""
import logging

from playwright.sync_api import expect

from model.business.login import *
from model.business.productpage import *


def test_lg_16(page_start):
    url = Const.url
    page, pa = page_start(url)

    # # 预置条件
    pa.normal_login()

    logging.info('检测页面是否出现打开菜单按钮')
    om = pa.find_ele(open_menu)
    expect(om).to_be_visible()

    # # 测试步骤
    logging.info('打开菜单')
    om.click()
    logging.info('点击退出')
    lo = pa.find_ele(logout)
    expect(lo).to_be_visible()
    lo.click()

    # # 预期结果
    logging.info('校验是否返回登录页面')
    un_input = pa.find_ele(user_name)
    expect(un_input).to_be_visible()
    logging.info('校验账号是否展示为空')
    un_text = un_input.input_value()
    assert un_text == ""
    pwd_input = pa.find_ele(pass_word)
    pwd_text = pwd_input.input_value()
    assert pwd_text == ""


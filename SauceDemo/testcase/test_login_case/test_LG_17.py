"""
用例名：登录成功刷新页面
编号：LG-17
预置条件：已登录成功进入商品页
测试步骤：
1.刷新页面
预期结果：
仍保持登录状态，未跳回登录页
"""
import logging

from playwright.sync_api import expect

from model.business.login import *
from model.business.productpage import *


def test_lg_17(page_start):
    url = Const.url
    page, pa = page_start(url)

    # # 预置条件
    pa.normal_login()

    logging.info('检测页面是否出现打开菜单按钮')
    om = pa.find_ele(open_menu)
    expect(om).to_be_visible()

    # # 测试步骤
    logging.info('刷新页面')
    page.reload()

    # # 预期结果
    logging.info('校验是否返回登录页面')
    un_input = pa.find_ele(user_name)
    expect(un_input).not_to_be_visible()

    logging.info('校验是否处于登陆后页面')
    pa.check_text(Const.successful_login_text)
    pa.check_img(img_sauce_labs_backpack)


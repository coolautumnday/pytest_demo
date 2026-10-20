"""
用例名：添加单个商品
编号：CT-01
预置条件：已登录进入商品列表页
测试步骤：
1.在任一商品点击 Add to cart；
预期结果：
按钮变为 Remove，购物车角标显示 1
"""
import logging

from playwright.sync_api import expect
from model.business.login import *
from model.business.productpage import *


def test_ct_01(page_start):
    url = Const.url
    page, pa = page_start(url)

    # # 预置条件
    pa.normal_login()
    # # 测试步骤
    logging.info('找到页面第一个Add to cart并点击')
    atc = pa.find_ele(add_to_cart).first
    atc.click()


    # # 预期结果，检测页面是否出现成功登录后文本
    logging.info('出现Remove')
    remove_text = pa.find_ele(remove_button)
    expect(remove_text).to_be_visible()
    logging.info('Remove角标是否正确')
    corner_mark_ = pa.find_ele(cart_1)
    expect(corner_mark_).to_be_visible()
    corner_mark_1 = corner_mark_.locator('[data-test="shopping-cart-badge"]').inner_text()
    assert corner_mark_1 == '1'



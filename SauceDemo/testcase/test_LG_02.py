"""
用例名：锁定账号登录
编号：LG-02
预置条件：已打开登录页
测试步骤：
1.用户名输入 locked_out_user；
2.密码输入 secret_sauce；
3.点击 Login
预期结果：
登录失败，提示：Epic sadface: Sorry, this user has been locked out.
"""
import logging

from playwright.sync_api import expect

from mode.business.login import *
from mode.business.productpage import *


def test_lg_02(page_start):
    url = Const.url
    page, pa = page_start(url)

    logging.info('预置条件')
    pa.check_text(title_page.type_name)

    # # 测试步骤
    logging.info('输入账号密码')
    pa.input_massage(user_name, Const.locked_out_user)
    pa.input_massage(pass_word, Const.password)

    logging.info('点击登录')
    pa.find_ele(login_button).click()

    # # 预期结果，检测页面文本是否出现
    logging.info('检测页面文本是否出现')
    texts = 'Epic sadface: Sorry, this user has been locked out.'
    pa.check_text(texts)
    logging.info('校验图片未加载')
    img_e = pa.find_ele(img_sauce_labs_backpack)
    expect(img_e).not_to_be_visible()

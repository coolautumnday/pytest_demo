"""
用例名：密码框掩码显示
编号：LG-15
预置条件：已打开登录页
测试步骤：
1.用户名输入 standard_user；
2.在密码框输入任意内容；
预期结果：
密码以 • 掩码显示，不可明文
"""
import logging

from playwright.sync_api import expect

from model.business.login import *
from model.business.productpage import *


def test_lg_15(page_start):
    url = Const.url
    page, pa = page_start(url)

    # # 预置条件
    logging.info('确认已处于登录页面')
    pa.check_text(title_page.type_name)

    # # 测试步骤
    logging.info('输入账号密码')
    pa.input_massage(user_name, Const.standard_user)
    pa.input_massage(pass_word, Const.error_password)

    # # 预期结果
    logging.info('检测页面密码是否掩码')
    pwd_input = pa.find_ele(pass_word)
    logging.info('确保密码有信息输入')
    expect(pwd_input).to_have_value(Const.error_password)
    logging.info('校验页面密码展示文本为空')
    pwd_text = pwd_input.inner_text()
    assert pwd_text == ""
    expect(pwd_input).to_have_text("")
    expect(pwd_input).not_to_have_text(Const.error_password)

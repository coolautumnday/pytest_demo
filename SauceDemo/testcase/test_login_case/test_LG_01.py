"""
用例名：正确账号密码登录
编号：LG-01
预置条件：已打开登录页
测试步骤：
1.用户名输入 standard_user；
2.密码输入 secret_sauce；
3.点击 Login
预期结果：
登录成功，跳转商品列表页
"""
import logging

from model.business.login import *
from model.business.productpage import *


def test_lg_01(page_start):
    url = Const.url
    page, pa = page_start(url)

    # # 预置条件
    logging.info('确认已处于登录页面')
    pa.check_text(title_page.type_name)

    # # 测试步骤
    logging.info('输入账号密码')
    pa.input_massage(user_name, Const.standard_user)
    pa.input_massage(pass_word, Const.password)

    logging.info('点击登录')
    pa.find_ele(login_button).click()

    # # 预期结果
    logging.info('检测页面是否出现成功登录后文本')
    pa.check_text(Const.successful_login_text)
    logging.info('校验图片是否正常加载')
    pa.check_img(img_sauce_labs_backpack)

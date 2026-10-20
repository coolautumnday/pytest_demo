"""
用例名：error_user 登录
编号：LG-05
预置条件：已打开登录页
测试步骤：
1.用户名输入 error_user；
2.密码输入 secret_sauce；
3.点击 Login
预期结果：
登录成功，后续操作易报错
"""
import logging

from model.business.login import *
from model.business.productpage import *


def test_lg_05(page_start):
    url = Const.url
    page, pa = page_start(url)

    # # 预置条件
    logging.info('确认已处于登录页面')
    pa.check_text(title_page.type_name)

    # # 测试步骤
    logging.info('输入账号密码')
    pa.input_massage(user_name, Const.error_user)
    pa.input_massage(pass_word, Const.password)

    logging.info('点击登录')
    pa.find_ele(login_button).click()

    # # 预期结果
    logging.info('检测页面是否出现成功登录后文本')
    pa.check_text(Const.successful_login_text)

    logging.info('点击添加购物车')
    pa.find_ele(add_to_cart).first.click()

    logging.info('点击Remove')
    rem_but = pa.find_ele(remove_button)
    rem_but.click()

    # # error账号预计不消失
    logging.info('校验remove button是否消失')
    pa.check_text(remove_button.type_value['name'])
    # pa.check_text(remove_button.type_value['name'], expected=False)

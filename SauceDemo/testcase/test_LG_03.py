"""
用例名：problem_user 登录
编号：LG-03
预置条件：已打开登录页
测试步骤：
1.用户名输入 problem_user；
2.密码输入 secret_sauce；
3.点击 Login
预期结果：
登录成功，但页面存在图片错乱等预置缺陷
"""
import logging

from mode.business.login import *
from mode.business.productpage import *


def test_lg_03(page_start):
    url = Const.url
    page, pa = page_start(url)

    logging.info('预置条件')
    pa.check_text(title_page.type_name)
    # # 测试步骤
    logging.info('输入账号密码')
    pa.input_massage(user_name, Const.problem_user)
    pa.input_massage(pass_word, Const.password)

    logging.info('点击登录')
    pa.find_ele(login_button).click()

    # # 预期结果，检测页面文本是否出现
    logging.info('检测页面文本是否出现')
    texts = ['Products', 'Sauce Labs Backpack', 'Add to cart']
    pa.check_text(texts)
    logging.info('校验图片是否正常加载')
    img_e = pa.find_ele(img_sauce_labs_backpack)
    img_width = img_e.evaluate("img => img.naturalWidth")
    assert img_width == 0, "图片加载要求加载失败，宽度为0"

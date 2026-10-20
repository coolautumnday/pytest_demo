"""
用例名：visual_user 登录
编号：LG-06
预置条件：已打开登录页
测试步骤：
1.用户名输入 visual_user；
2.密码输入 secret_sauce；
3.点击 Login
预期结果：
登录成功，UI布局/颜色错位
"""
import logging

from aw.public.public_aw import match_img
from model.business.login import *
from model.business.productpage import *


def test_lg_06(page_start):
    url = Const.url
    page, pa = page_start(url)

    # # 预置条件
    logging.info('确认已处于登录页面')
    pa.check_text(title_page.type_name)

    # # 测试步骤
    logging.info('输入账号密码')
    pa.input_massage(user_name, Const.visual_user)
    pa.input_massage(pass_word, Const.password)

    logging.info('点击登录')
    pa.find_ele(login_button).click()

    # # 预期结果
    logging.info('检测页面是否出现成功登录后文本')
    pa.check_text(Const.successful_login_text)

    logging.info('页面UI布局展示错误')
    # loc = pa.find_ele(product_img_1)
    # loc.screenshot(path="./tmp/backpack.png")
    # 依旧没有等待渲染完成就截图

    pa.check_img(product_img_1)
    pa.screenshot_by_ele(product_img_1)
    # # asdfdsa {'x': 111, 'y': 155, 'width': 261.53125, 'height': 238}
    logging.info('开始对比页面图片')
    match_value = match_img(product_img_1, dif=20, exceptde=False)
    assert match_value

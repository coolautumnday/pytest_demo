"""
用例名：performance_glitch_user 登录
编号：LG-03
预置条件：已打开登录页
测试步骤：
1.用户名输入 performance_glitch_user；
2.密码输入 secret_sauce；
3.点击 Login
预期结果：
登录成功，但页面加载明显缓慢
"""
import logging
import time
from playwright.sync_api import expect
from mode.business.productpage import *
from mode.business.login import *

def test_lg_04(page_start):
    url = Const.url
    page, pa = page_start(url)

    logging.info('预置条件')
    pa.check_text(title_page.type_name)

    # # 测试步骤
    logging.info('输入账号密码')
    pa.input_massage(user_name, Const.performance_glitch_user)
    pa.input_massage(pass_word, Const.password)
    logging.info('开始计时')

    start_time = time.time()
    logging.info('点击登录')
    pa.find_ele(login_button).click()

    logging.info('校验登录状态')
    suc_title = pa.find_ele(suc_page_title)
    expect(suc_title).to_be_visible(timeout=20000)
    logging.info('結束计时')
    end_time = time.time()

    tims = (end_time - start_time)
    assert tims >3
from Model.model_saucedemo import *
from aw.public.SauceDemo_aw import *

def test_deletecart(get_pa):
    url = 'https://www.saucedemo.com'
    page, pa = get_pa(url)
    # # 登录页面
    pa.input_message(user_name, 'standard_user',timeout=10000)
    pa.input_message(password)
    pa.get_ElementControl(login_button).click()

    pa.get_ElementControl(login_seccess).wait_for()

    # # 点击addtocart
    check_remove = pa.get_ElementControl(remove_button)
    # # 清空remove，并点击第一个加入购物车
    for i in range(10):
        if not check_remove.first.is_visible():
            break
        check_remove.first.click()

    pa.get_ElementControl(add_to_cart).first.click()
    pa.check_is_visible(check_remove, fail_msg='点击添加购物车后Remove元素未显示出来')

    cart_badge = pa.get_ElementControl(cart_car_1)

    cart_badge.click()

    Y_cart = pa.get_ElementControl(cart_page)
    expect(Y_cart).to_be_visible()

    # # 校验页面显示金额
    cart_money = pa.get_ElementControl(cart_money_1)
    pa.check_is_visible(cart_money, '购物车显示金额错误')
    # # 点击remove
    pa.get_ElementControl(remove_button).click()
    # # 还处于you cart页面
    expect(Y_cart).to_be_visible()
    # # 条数已经消失
    pa.check_is_visible(cart_money, False,'购物车显示金额错误')
    # # 点击checkout
    pa.get_ElementControl(check_out_button).click()
    # # 等待跳转
    Y_information = pa.get_ElementControl(information)
    Y_information.wait_for()
    pa.check_is_visible(Y_information)
    # # 进入结账页面
    pa.input_message(check_out_Fname)
    pa.input_message(check_out_Lname)
    pa.input_message(check_out_Code)
    pa.get_ElementControl(continue_button).click()

    # # 校验结账金额
    cart_money = pa.get_ElementControl(checkout_money_1)
    expect(cart_money).to_contain_text(cart_money_0.type_name)
    pa.check_is_visible(cart_money, '结账页面显示金额错误')


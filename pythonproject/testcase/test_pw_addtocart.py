from playwright.sync_api import expect
from Model.model_saucedemo import *

def test_addtocart(get_pa):
    url = 'https://www.saucedemo.com'
    page, pa = get_pa(url)
    # # 登录页面
    pa.input_message(user_name, timeout=10000)
    pa.input_message(password, 'secret_sauce')
    page.get_by_role("button", name="Login").click()

    page.get_by_text("Swag Labs").wait_for()

    # # 点击addtocart
    check_remove = page.get_by_role("button", name="Remove")
    # # 清空remove，并点击第一个加入购物车
    for i in range(10):
        if not check_remove.first.is_visible():
            break
        check_remove.first.click()

    page.get_by_role("button", name="Add to cart").first.click()
    pa.check_is_visible(check_remove, fail_msg='点击添加购物车后Remove元素未显示出来')

    cart_num = page.get_by_label("Cart, empty").locator('//*[@id="shopping_cart_container"]/a/span')

    pa.check_is_visible(cart_num, fail_msg='点击添加购物车后右上方购物车未显示标签元素未显示出来')

    cart_badge = page.locator('//*[@data-test="shopping-cart-badge"]')
    expect(cart_badge).to_have_text("1")




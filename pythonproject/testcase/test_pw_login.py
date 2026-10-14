from playwright.sync_api import expect

from Model.model_saucedemo import *


def test_login_demo(get_pa):
    url = 'https://www.saucedemo.com'
    page, pa = get_pa(url)
    # page_input_username = page.get_by_label('Username')
    # page_input_username.wait_for(timeout=10000)  # 等待用户名输入框加载完成
    # page_input_username.fill('standard_user')
    pa.input_message(user_name, timeout=10000)
    pa.input_message(password, 'secret_sauce')

    page.get_by_role("button", name="Login").click()

    page.get_by_text("Swag Labs").wait_for()
    add_nt = page.get_by_role('button', name='Add to cart').first

    expect(add_nt).to_be_enabled()

    add_nt.click()
    rem_nt = page.get_by_role('button', name='Remove')
    expect(rem_nt).to_be_visible()


import os.path

from model import Const
from basepage import BasePage

xpath = './model/image/'

class ProductPage(BasePage):
    pass
    def __init__(self, get_type=None, type_name=None, type_value=None, img_name=None) -> None:
        self.get_type = get_type
        self.type_name = type_name
        self.type_value = type_value
        if img_name is None:
            self.img_name = img_name
        else:
            self.img_name = os.path.join(xpath, img_name + '.png')

suc_page_title = ProductPage(
    get_type='attribute',
    type_value='data-test=title'
)

img_sauce_labs_backpack = ProductPage(
    get_type='alt',
    type_name='Sauce Labs Backpack',
    type_value='/assets/sauce-backpack-1200x1500-CjRW-Djj.jpg'
)

add_to_cart = ProductPage(
    get_type="role",
    type_name="button",
    type_value={'name':"Add to cart"}
)

remove_button = ProductPage(
    get_type="role",
    type_name="button",
    type_value={'name':"Remove"}
)

product_img_1 = ProductPage(
    get_type='alt',
    type_name='Sauce Labs Backpack',
    img_name='product_img_1'
)

open_menu = ProductPage(
    get_type='text',
    type_name='Open Menu'
)

logout = ProductPage(
    get_type='text',
    type_name='Logout'
)

cart_1 = ProductPage(
    get_type="label",
    type_name="Cart, 1 items",
    type_value='1'
)
from mode import Const
from basepage import BasePage

class ProductPage(BasePage):
    pass
    def __init__(self, get_type=None, type_name=None, type_value=None) -> None:
        self.get_type = get_type
        self.type_name = type_name
        self.type_value = type_value

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
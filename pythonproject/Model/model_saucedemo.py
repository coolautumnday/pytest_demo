
class Model_SauceDemo:
    def __init__(self, type_name=None, get_type=None, type_value=None):
        self.type_name = type_name
        self.get_type = get_type
        self.type_value = type_value


user_name = Model_SauceDemo(
    get_type="label",
    type_name="Username",
    type_value="standard_user"
)

password = Model_SauceDemo(
    get_type="label",
    type_name="Password",
    type_value="secret_sauce"
)

login_button = Model_SauceDemo(
    get_type="role",
    type_name="button",
    type_value={'name': 'Login'}
)

login_seccess = Model_SauceDemo(
    get_type="text",
    type_name="Swag Labs"
)

remove_button = Model_SauceDemo(
    get_type="role",
    type_name="button",
    type_value={'name':"Remove"}
)

add_to_cart = Model_SauceDemo(
    get_type="role",
    type_name="button",
    type_value={'name':"Add to cart"}
)

shopping_cart_badge = Model_SauceDemo(
    get_type="locator",
    type_value='//span[@data-test="shopping-cart-badge"]'
)

cart_money_1 = Model_SauceDemo(
    get_type='text',
    type_name='29.99'
)

cart_money_0 = Model_SauceDemo(
    get_type='text',
    type_name='0'
)

checkout_money_1 = Model_SauceDemo(
    get_type='text',
    type_name='Item total: $'
)

check_out_button = Model_SauceDemo(
    get_type='role',
    type_name='button',
    type_value={'name': 'checkout'}
)

check_out_Fname = Model_SauceDemo(
    get_type='label',
    type_name='First Name',
    type_value='test_name'
)

check_out_Lname = Model_SauceDemo(
    get_type='label',
    type_name='Last Name',
    type_value='test_name'
)

check_out_Code = Model_SauceDemo(
    get_type='label',
    type_name='Zip/Postal Code',
    type_value='test_Code'
)

continue_button = Model_SauceDemo(
    get_type='role',
    type_name='button',
    type_value={'name': 'Continue'}

)

information = Model_SauceDemo(
    get_type='text',
    type_name='Checkout: Your Information'
)

cart_ = Model_SauceDemo(
    get_type='locator',
    type_name='shopping_cart_badge'
)

cart_car_1 = Model_SauceDemo(
    get_type='label',
    type_name='Cart, 1 items'
)

cart_page = Model_SauceDemo(
    get_type='text',
    type_name='Your Cart'
)
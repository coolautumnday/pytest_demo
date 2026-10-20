from model import Const
from basepage import BasePage


class LoginPage(BasePage):
    def __init__(self, get_type=None, type_name=None, type_value=None):
        self.get_type = get_type
        self.type_name = type_name
        self.type_value = type_value

title_page = LoginPage(
    get_type='title',
    type_name='Swag Labs'
)

user_name = LoginPage(
    get_type='label',
    type_name='username',
    type_value=Const.standard_user
)

pass_word = LoginPage(
    get_type='label',
    type_name='password',
    type_value=Const.password
)

login_button = LoginPage(
    get_type='role',
    type_name='button',
    type_value={'name': 'Login'}
)


no_username = LoginPage(
    get_type='text',
    type_name='Epic sadface: Username is required'
)

no_password = LoginPage(
    get_type='text',
    type_name='Epic sadface: Password is required'
)

no_userpass = LoginPage(
    get_type='text',
    type_name='Epic sadface: Username is required'
)

password_ERR = LoginPage(
    get_type='text',
    type_name='Epic sadface: Username and password do not match any user in this service'
)

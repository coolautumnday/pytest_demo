
class Model_SauceDemo:
    def __init__(self, name=None, get_type=None, value=None):
        self.name = name
        self.get_type = get_type
        self.value = value


user_name = Model_SauceDemo(
    name="Username",
    get_type="label",
    value="standard_user"
)

password = Model_SauceDemo(
    name="Password",
    get_type="label",
    value="secret_sauce"
)
import logging
from playwright.sync_api import *
from typing import Union, List
from mode.business.login import LoginPage
from mode.business.productpage import ProductPage

logging.basicConfig(level=logging.INFO)


class Bus_aw():
    def __init__(self, page: Page):
        self.page = page

    def find_ele(self, ele):
        """
        :param ele: 待查找控件，认传参为model，不是的话则需传dict
        :return:
        """
        if isinstance(ele, LoginPage) or isinstance(ele, ProductPage):
            get_type = ele.get_type
            type_name = ele.type_name
            type_value = ele.type_value
        elif isinstance(ele, dict):  # # 防止传入非字典
            get_type = ele['get_type']
            type_name = ele['type_name']
            type_value = ele['type_value']
        else:
            # # 捕获ele是Locator等其他对象的情况，抛出提示
            raise TypeError(f"参数ele类型错误，当前类型：{type(ele)}，仅支持LoginPage实例或者dict")
        locator_map = {
            "label": lambda: self.page.get_by_label(type_name),
            "test_id": lambda: self.page.get_by_test_id(type_name),
            "text": lambda: self.page.get_by_text(type_name),
            "title": lambda: self.page.get_by_title(type_name),
            "alt": lambda: self.page.get_by_alt_text(type_name),
            "placeholder": lambda: self.page.get_by_placeholder(type_name),
            "role": lambda: self.page.get_by_role(type_name, **type_value),
            "css": lambda: self.page.locator(type_value),
            "locator": lambda: self.page.locator(type_value),
            "attribute": lambda: self.page.locator(type_value),
        }
        # # 判断key是否存在
        if get_type not in locator_map:
            raise ValueError(f"目前不支持的定位类型: {get_type}, 想要自己加")
        page_ele = locator_map[get_type]()
        return page_ele

    def input_massage(self, ele, input_text: str = None):
        """
        :param ele: 默认传参为model，不是的话则需传dict
        :param input_text: 输入文本
        :return:
        """
        fill_text = input_text if input_text is not None else ele.type_value
        page_ele = self.find_ele(ele)
        page_ele.clear()
        page_ele.fill(fill_text)
        logging.info(f"输入成功：{fill_text}")

    def check_text(self, text: Union[str, List[str]], expected: bool = True, fuzz: bool = True,
                   timeout: float = 5000):
        """
        校验文本元素可见/隐藏
        :param text: 需检测文本，str/list
        :param expected: True页面存在；False页面不存在
        :param fuzz: True模糊包含；False精确完全匹配
        :param timeout: 断言超时ms
        """
        text_list: List[str] = [text] if isinstance(text, str) else text
        for target_text in text_list:
            if not isinstance(target_text, str):
                raise TypeError(f" {target_text}类型错误，输入list中要为str ")

            ele_text = {"get_type": "text", "type_name": target_text, "type_value": None, "exact": not fuzz}
            locator: Locator = self.find_ele(ele_text)
            if expected:
                expect(locator.first).to_be_visible()
            else:
                expect(locator.first).not_to_be_attached()
            return bool(locator.count())
        return None

    def check_img(self, ele):
        img_ele = self.find_ele(ele)
        expect(img_ele).to_be_visible()
        # # 校验图片scr（完整链接/正则匹配包含部分地址）
        src = ele.type_value
        expect(img_ele).to_have_attribute("src", src)

        # # 判断图片宽度，小于等于0则加载失败或图裂
        return img_ele.evaluate("img => img.naturalWidth")

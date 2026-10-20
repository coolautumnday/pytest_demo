import logging
import os
import time
from time import sleep
from typing import Union, List, Optional, Dict

from playwright.sync_api import *

from model.business.login import *
from model.business.productpage import *

logging.basicConfig(level=logging.INFO)


class Bus_aw():
    def __init__(self, page: Page):
        self.page = page
        self.screenshot_default_dir = "./tmp"

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

    def normal_login(self) -> None:
        """
        正常登录并处于登录状态
        :param pa: page_start返回值
        :return:
        """
        logging.info('正常登录并处于登录状态')
        self.check_text(title_page.type_name)
        self.input_massage(user_name, Const.standard_user)
        self.input_massage(pass_word, Const.password)
        self.find_ele(login_button).click()
        self.check_text(Const.successful_login_text)
        self.check_img(img_sauce_labs_backpack)

    def check_text(self, text: Union[str, List[str]], expected: bool = True, fuzz: bool = True):
        """
        校验文本元素可见/隐藏
        :param text: 需检测文本，str/list
        :param expected: True页面存在；False页面不存在
        :param fuzz: True模糊包含；False精确完全匹配
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

    def check_img(self, ele, expected: bool = True):
        """
        校验图片信息可见
        :param ele: 检测图片控件信息
        :param expected: true图片存在，False图片不存在
        """
        img_ele = self.find_ele(ele)
        # # 滑动查找图片
        img_ele.scroll_into_view_if_needed()
        expect(img_ele).to_be_visible()
        # # 校验图片scr（完整链接/正则匹配包含部分地址）
        src = ele.type_value
        if src:
            if expected:
                expect(img_ele).to_have_attribute("src", src)
            else:
                expect(img_ele).not_to_have_attribute("src", src)
        # # 循环等待图片加载完成，直到naturalWidth>0，但并不代表图片渲染完成，
        img_ele.page.wait_for_function("ele => ele.naturalWidth > 0", arg=img_ele.element_handle(), timeout=5000)

        # 图片naturalW已经>0之后，再等待浏览器渲染帧
        self.page.evaluate("() => new Promise(resolve => requestAnimationFrame(()=>requestAnimationFrame(resolve)))")
        # print("css宽高：", img_ele.bounding_box())
        # nat_width = img_ele.evaluate("el=>el.naturalWidth")
        # nat_height = img_ele.evaluate("el=>el.naturalHeight")
        # print(f"图片真实宽高 naturalW:{nat_width}, naturalH:{nat_height}")

        # # 判断图片宽度，小于等于0则加载失败或图裂
        return img_ele.evaluate("img => img.naturalWidth")

    def get_pos_by_ele(self, ele) -> Optional[Dict]:
        """
        获取元素坐标 bounding_box
        :param ele: LoginPage/ProductPage实例 或者 dict定位器
        :return: dict {"x":float,"y":float,"width":float,"height":float} / None 元素不可见返回None
        """
        pos_ele = self.find_ele(ele)
        expect(pos_ele).to_be_visible()
        pos_e = pos_ele.bounding_box()
        if pos_e is None:
            logging.warning("获取元素bounding_box返回None，元素可能不在视口内")
        return pos_e

    def screenshot_by_ele(self, ele, file_name: str = None, is_pos: bool = False):
        """
        根据元素直接截图，默认保存 ./tmp/
        :param ele: 元素对象 LoginPage/ProductPage/tuple坐标(左上角xy坐标加上宽和高组成) / dict定位,
        :param file_name: 截图文件名，不传自动生成时间戳名字
        :return: 截图完整路径
        """
        if not os.path.exists(self.screenshot_default_dir):
            os.makedirs(self.screenshot_default_dir)
        # 自动生成文件名
        if not file_name:
            # file_name = f"ele_screenshot_{int(time.time() * 1000)}.png"
            file_name = f"ele_tmp.png"
        save_path = os.path.join(self.screenshot_default_dir, file_name)
        if isinstance(ele, tuple):
            pos_e = {'x': ele[0], 'y': ele[1], 'width': ele[2], 'height': ele[3]}
        else:
            page_ele = self.find_ele(ele)
            print("匹配元素数量：", page_ele.count())
            # 滚动到元素，保证可见
            page_ele.scroll_into_view_if_needed()
            page_ele.wait_for()
            expect(page_ele).to_be_visible()

            # # 循环等待图片加载完成，直到naturalWidth>0，但并不代表图片渲染完成，
            page_ele.page.wait_for_function("ele => ele.naturalWidth > 0", arg=page_ele.element_handle(), timeout=5000)
            # #  读取offsetHeight强制浏览器reflow
            page_ele.evaluate("el => el.offsetHeight")
            # # 图片naturalW已经>0之后，再等待浏览器渲染帧
            self.page.evaluate(
                "() => new Promise(resolve => requestAnimationFrame(()=>requestAnimationFrame(resolve)))")
            pos_e = self.get_pos_by_ele(ele)
            sleep(3)
        if is_pos:
            # # 获取截图坐标区域
            if not pos_e:
                raise RuntimeError("无法获取元素坐标，不能执行区域截图")
            # page截图 + clip 按坐标裁剪
            self.page.screenshot(path=save_path, clip=pos_e)
        else:
            page_ele.screenshot(path=save_path)
        logging.info(f"坐标裁剪截图已保存: {save_path}")
        return save_path



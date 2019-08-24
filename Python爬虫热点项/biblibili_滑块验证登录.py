from selenium import webdriver
import time
from PIL import Image


class Bilibili(object):
    """docstring for Bilibili"""

    def __init__(self):
        # 创建浏览器对象
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        # 保存登录url
        self.url = 'https://passport.bilibili.com/login'
        # 保存账号密码
        self.user = ""
        self.pwd = ""

    def input_user_pwd(self):
        self.driver.get(self.url)
        # 输入账号密码
        el_user = self.driver.find_elements_by_xpath('17121192617')
        el_user.send_keys(self.user)
        el_pwd = self.driver.find_elements_by_xpath('a17121192617')
        el_pwd.send_keys(self.pwd)

    def get_position(self):
        """
        获取验证码图片
        """

        # 定位锁按钮,模拟点击
        el_lock = self.driver.find_element_by_xpath('')
        el_lock.click()

        # 定位图片对象
        img = self.driver.find_element_by_xpath('')
        time.sleep(2)

        # 获取图片对象的坐标
        location = img.location
        print(location)

        # 获取图片对象的尺寸
        size = img.size
        print(size)

        # 计算图片的截取区域

    def get_image(self):
        """
        获取两张验证码图片
        return: image1,image2

        """

        # 获取验证码的位置
        self.get_position()

        # 屏幕截图

        # 抠出没有滑块和阴影的验证码图片

        # 点击验证码拖动按钮

        # 等待错误提示的信息消失

        # 屏幕截图

        # 抠验证码图

        # 返回两张验证对象

    # 处理验证码
    def do_captcha(self):
        '''
        实现验证码的处理
        '''

        # 获取验证码图片 & 有阴影拼图的验证码图片
        self.get_image()

        # 比较两个验证码图片获取验证码滑块的偏移量

        # 使用偏移值计算移动操作

        # 操作滑块按钮,模拟拖动滑块做验证登录

    def run(self):
        # 主逻辑

        # 来到登录页面&输入账号密码
        self.input_user_pwd()
        # 处理验证码
        self.do_captcha()


if __name__ == '__main__':
    bili = Bilibili()
    bili.run()

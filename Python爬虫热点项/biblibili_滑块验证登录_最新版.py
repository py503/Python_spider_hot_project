from selenium import webdriver
# 鼠标动作键
from selenium.webdriver.common.action_chains import ActionChains
import time
from PIL import Image
from io import BytesIO


class Bilibili(object):
    """docstring for Bilibili"""

    def __init__(self):
        # 创建浏览器对象
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        # 保存登录url
        self.url = 'https://passport.bilibili.com/login'
        # 保存账号密码
        self.user = "17121192617"
        self.pwd = "a17121192617"

    def input_user_pwd(self):
        self.driver.get(self.url)
        # 输入账号密码
        el_user = self.driver.find_element_by_xpath(
            '//*[@id="login-username"]')
        el_user.send_keys(self.user)
        el_pwd = self.driver.find_element_by_xpath('//*[@id="login-passwd"]')
        el_pwd.send_keys(self.pwd)

    def click_login(self):
        self.driver.find_element_by_xpath(
            '//*[@class="btn btn-login"]').click()

    def get_position(self):
        """
        获取验证码图片的四条边
        """

        # # 定位锁按钮,模拟点击
        # el_lock = self.driver.find_element_by_xpath('')
        # el_lock.click()

        # 定位图片对象
        # 等待显示图片出来
        time.sleep(3)

        # img1 = self.driver.find_element_by_xpath(
        # '//canvas[@class="geetest_canvas_bg geetest_absolute"]')
        img1 = self.driver.find_element_by_xpath(
            '//canvas[@class="geetest_canvas_slice geetest_absolute"]')
        # img1 = self.driver.find_element_by_xpath(
        #     '/html/body/div[2]/div[2]/div[6]/div/div[1]/div[1]/div/a/div[1]/div/canvas[1]')
        # screentshot = img1.screenshot_as_png()
        # screentshot = Image.open(BytesIO(screentshot))
        # with open('Full_image.png', 'wb')as f:
        #     captcha1.save(f)
        # self.driver.get_screenshot_as_png("Full_screen.png")
        # print(screentshot)
        # # 获取图片对象的坐标
        location = img1.location
        print(location)

        # 获取图片对象的尺寸,两图片大小一样
        size = img1.size
        print(size)

        # # 计算图片的截取区域
        # left, top, right, button = 2 * location["x"], 2 * location["y"], 2 * (location["x"] + size[
        #     "width"]), 2 * (location["y"] + size["height"])
        left, top, right, button = location["x"], location["y"], (location["x"] + size[
            "width"]), (location["y"] + size["height"])

        # # 返回
        print(left, top, right, button)
        return left, top, right, button

    def get_screenshot(self):
        """
        获取屏幕截图
        """
        # 截图
        time.sleep(0)
        screentshot = self.driver.get_screenshot_as_png()
        # 使用PIL将截图创建成图片对象,该对象可以获取图片的相关信息
        screentshot = Image.open(BytesIO(screentshot))
        return screentshot

    def update_style(self):
        '''
            修改图片的style属性，显示无缺口的图片,完整验证码图片
        '''
        js = 'document.querySelectorAll("canvas")[3].style="display:block"'
        self.driver.execute_script(js)
        time.sleep(2)

    def get_image(self):
        """
        获取两张验证码图片
        return: image1,image2

        """
        # 获取验证码的位置
        position = self.get_position()
        # 屏幕截图(有滑块图片)
        time.sleep(0)
        # 抠出没有滑块和阴影的验证码图片
        captcha1 = self.get_screenshot().crop(position)  # 抠出图片,返回captcha1对象

        # 屏幕截图(有滑块图片),调用修改style属性方法
        self.update_style()
        # 从屏幕截图中抠出无缺口的验证码图片
        captcha2 = self.get_screenshot().crop(position)  # 抠出图片,返回captcha1对象

        # 保存图片
        with open('captcha1.png', 'wb')as f:
            captcha1.save(f)

        with open('captcha2.png', 'wb')as f:
            captcha2.save(f)

        # 返回两张验证对象
        return captcha1, captcha2

    def is_pixel_equal(self, image1, image2, x, y):

        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        # print(pixel1, pixel2)

        # 设定一个比较值
        threshold = 60  # 看需求
        # 比较
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        """
        核对两个验证码的相同位置的像素, 找出像素偏差值大的位置,返回其x值, 该值为验证码
        拖动的位移
        :param image1: 有阴影拼图的验证码图片
        :param image2: 没有阴影拼图的验证码图片
        :return: 比对之后的偏移值
        """

        # 选点设定一个比较基准
        left = int(image2.size[0] / 4.2)

        # print(imgage2.size)
        # 遍历x轴的点到最后
        for i in range(left, image2.size[0]):
            for j in range(image1.size[1]):
                # 获取一个坐标点,然后在两张图上核对该坐标点的颜色差距,
                # 判断颜色差距是否过大, 过大则该x值为偏移值, 返回该值, 否则继续
                if not self.is_pixel_equal(image2, image1, i, j):
                    left = i
                    # 缺口有点偏 移要算在里面,大概是10,我选8
                    print(left - 2)
                    return left - 2
        return left - 2

    def get_track(self, offset):
        """
        通过偏移总量,模拟人类操作计算每次偏移量
        :param offset: 
        :return:
        """
        # 存储步代
        track = []
        # 当前位移
        current = 0
        # 中间点,用于切换加速度
        mid = offset * 3 / 5
        t = 0.3
        v = 0

        while current < offset:
            if current < round(mid):
                a = 2
            else:
                a = -3

            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track

    def operate_button(self, track):
        time.sleep(1)
        # 点击拖动按钮
        el_button = self.driver.find_element_by_xpath(
            '//div[@class="geetest_slider_button"]')
        ActionChains(self.driver).click_and_hold(el_button).perform()
        # 移动滑块
        for i in track:
            ActionChains(self.driver).move_by_offset(
                xoffset=i, yoffset=0).perform()

            # 先加速后减速效果也不是很好。
            # 每移动一次随机停顿0-1/100秒之间骗过了极验，通过率很高
        #     time.sleep(random.random() / 100)
        # time.sleep(random.random())
        # # 按逆向轨迹移动
        # for i in back_tracks:
        #     time.sleep(random.random() / 100)
        #     ActionChains(self.driver).move_by_offset(
        #         xoffset=i, yoffset=0).perform()

        # 模拟人手抖动
        # 模拟人,来回移动鼠标,回来开始位置
        # ActionChains(self.driver).move_by_offset(
        #     xoffset=5, yoffset=0).perform()
        # ActionChains(self.driver).move_by_offset(
        #     xoffset=5, yoffset=0).perform()
        # time.sleep(0.5)

        # 松开按钮
        ActionChains(self.driver).release().perform()

    # 处理验证码
    def do_captcha(self):
        '''
        实现验证码的处理
        '''

        # 有阴影拼图的验证码图片img1 & 获取没有阴影验证码图片img2
        img1, img2 = self.get_image()

        # 比较两个验证码图片获取验证码滑块的偏移量
        offset = self.get_gap(img1, img2)

        # 使用偏移值计算移动操作
        track = self.get_track(offset)

        # 操作滑块按钮,模拟拖动滑块做验证登录
        self.operate_button(track)

    def run(self):
        # 主逻辑

        # 来到登录页面&输入账号密码
        self.input_user_pwd()
        # 点击登录
        self.click_login()
        # 处理验证码
        self.do_captcha()


if __name__ == '__main__':
    bili = Bilibili()
    bili.run()

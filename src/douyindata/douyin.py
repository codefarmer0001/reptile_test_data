from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import undetected_chromedriver as uc
import random
import math
import re
# from urllib.parse import urlparse

# ./Google\ Chrome --user-data-dir="~/userdata" --remote-debugging-port=19222

class douyin:

    def __init__(self) -> None:
        self.move_mouse = True
        self.datas = []
        self.init_chrome()
        self.brower_website()
        pass

    def init_chrome(self):

        # 指定Chrome驱动器路径（注意修改为你实际的驱动器路径）
        driver_path = 'src/chrome/mac/arm/chromedriver'
        # 创建Chrome驱动器服务
        service = Service(driver_path)
        
        # 创建Chrome浏览器对象
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument('--disable-infobars')
        # chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        # chrome_options.add_argument(r"user-data-dir=/Users/mac/Library/Application Support/Google/Chrome/Default")
        # user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/598.45 (KHTML, like Gecko) Chrome/103.0.2647 Safari/537.36"
        # user_agent = random.choice(user_agents)
        # chrome_options.add_argument(f'user-agent={user_agent}')
        # chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:19222")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)


    def brower_website(self):
        self.driver.get('https://cc.hql21i.cc/?_did=5863d067a2c7ad9b5b44ae4137be95c04e68c525b7dd03a8e43e31e4312a911e5a0cefc4da4c6ad8ce1e374cbf69bfb323f61181c6206b0c73140cc177b05267')
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 8, poll_frequency=0.1)
        
        time.sleep(6)
        self.dismiss_dialog()

        # self.reptile_top_list()

        time.sleep(300000)
        

    # 列表数据
    def dismiss_dialog(self):
        enter_span = None
        # print(11111)
        try:
            enter_span = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, './/span[@class="enter"]'))
            )
        except Exception as e:
            pass
            # print(e)
        # print(enter_span)
        if enter_span:
            self.actions.move_to_element(enter_span).perform()
            self.driver.execute_script("arguments[0].click();", enter_span)

        self.close_dialog()
        # print(11111)

        notification_span = None
        # print(11111)
        try:
            notification_span = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, './/div[@class="notification-container"]'))
            )
        except Exception as e:
            pass
            # print(e)
        if notification_span:
            btn_div = notification_span.find_element(By.XPATH, './/div[@class="btn"]')
            print(btn_div)
            self.actions.move_to_element(btn_div).perform()
            # print('点击')
            self.driver.execute_script("arguments[0].click();", btn_div)

        # 
        self.reptile_list(0)

    def reptile_list(self, list_index):
        sixItem_container_div = None
        data = {}
        print(11111)
        try:
            sixItem_container_div = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, './/div[@class="sixItem-container"]'))
            )
        except Exception as e:
            pass
            # print(e)
        # print(enter_span)
        if sixItem_container_div:
            print(sixItem_container_div.get_attribute('innerHTML'))
            video_Item_div = sixItem_container_div.find_elements(By.XPATH, './/div[@class="Video-Item"]')
            if video_Item_div and list_index < len(video_Item_div):
                # for item in  video_Item_div:
                item = video_Item_div[list_index]
                print('\n')
                print(item.get_attribute('innerHTML'))
                van_image_div = item.find_element(By.XPATH, './/div[@class="van-image"]')
                image_tag = van_image_div.find_element(By.XPATH, './/img[@class="van-image__img"]')
                cover = image_tag.get_attribute('src')
                print(cover)
                data['cover'] = cover
                title_div = item.find_element(By.XPATH, './/div[@class="title"]')
                title = title_div.get_attribute('innerHTML')
                print(title)
                data['title'] = title
                video_info_div = item.find_element(By.XPATH, './/div[@class="video-info"]')
                span_divs = video_info_div.find_elements(By.TAG_NAME, 'span')
                views = 0
                popularity = 0
                if span_divs:
                    for index, span_item in enumerate(span_divs):
                        text = span_item.get_attribute('innerHTML')
                        if index == 0: 
                            popularity = text
                        else:
                            views = text
                print(views)
                data['views'] = views
                print(popularity)
                data['popularity'] = popularity
                duration_div = item.find_element(By.XPATH, './/div[@class="duration"]')
                duration = duration_div.get_attribute('innerHTML')
                print(duration)
                data['duration'] = duration
                user_info_div = item.find_element(By.XPATH, './/div[@class="user"]')
                img_tag = user_info_div.find_element(By.TAG_NAME, 'img')
                author_avatar = img_tag.get_attribute('src')
                print(author_avatar)
                data['author_avatar'] = author_avatar
                author_span_tag = user_info_div.find_element(By.TAG_NAME, 'span')
                author = author_span_tag.get_attribute('innerHTML')
                print(author)
                data['author'] = author
                self.actions.move_to_element(item).perform()
                self.driver.execute_script("arguments[0].click();", item)
                video_url, tags = self.reptile_detail()
                print(video_url)
                data['video_url'] = video_url
                print(tags)
                data['tags'] = tags
                time.sleep(3)
                self.datas.append(data)

                # self.datas.append(data)
                self.driver.refresh()
                if list_index < 5:
                    list_index += 1
                    print(list_index)
                    self.driver.refresh()
                    self.reptile_list(list_index)
                else:
                    print(self.datas)
                pass

    
    def close_dialog(self):
        close_span = None
        try:
            close_span = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, './/img[@class="close"]'))
            )
        except Exception as e:
            print(e)
        # print(close_span)
        if close_span:
            self.actions.move_to_element(close_span).perform()
            self.driver.execute_script("arguments[0].click();", close_span)
            self.close_dialog()


    # 内页数据
    def reptile_detail(self):
        # time.sleep(3)
        # self.driver.back()
        video_url = ''
        tags = []
        video_div = None
        try:
            video_div = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, './/video[@mediatype="video"]'))
            )
        except Exception as e:
            print(e)
        print(video_div)
        if video_div:
            video_url = video_div.get_attribute('src')
            print(video_url)

        tags_div = None
        try:
            tags_div = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, './/div[@class="tags"]'))
            )
        except Exception as e:
            print(e)
        print(tags_div)
        if tags_div:
            tags_span = tags_div.find_elements(By.TAG_NAME, 'span')
            if tags_span:
                for item in tags_span:
                    tag = item.get_attribute('innerHTML')
                    tags.append(tag)
                    # print(vide_url)

        self.driver.back()

        return video_url, tags


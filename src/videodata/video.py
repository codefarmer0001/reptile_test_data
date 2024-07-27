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
import uuid
# from urllib.parse import urlparse

# ./Google\ Chrome --user-data-dir="~/userdata" --remote-debugging-port=19222

class video:

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
        self.driver.get('https://x.mossav.one/vodtype/6.html')
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 8, poll_frequency=0.1)
        
        # time.sleep(6)
        self.reptile_list(0)

        # self.reptile_top_list()

        time.sleep(300000)


    def reptile_list(self, list_index):
        urls = {}

        video_div = None
        datas = []
        data_map = {}
        print(11111)

        try:
            video_div = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, './/div[@class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-5"]'))
            )
        except Exception as e:
            pass
            # print(e)
        # print(enter_span)
        if video_div:
            # print(video_div.get_attribute('innerHTML'))
            video_Item_div = video_div.find_elements(By.XPATH, '/div')
            if video_Item_div:
                for video_Item in video_Item_div:
                    uuid_string = str(uuid.uuid4())
                    print(uuid_string)
                    data = {}
                    video_info_div = video_Item.find_element(By.XPATH, './/div[@class="relative aspect-w-16 aspect-h-9 rounded overflow-hidden shadow-lg"]')
                    a_tags = video_info_div.find_elements(By.TAG_NAME, 'a')
                    if a_tags:
                        for index, item in enumerate(a_tags):
                            url = item.get_attribute('href')
                            urls[uuid_string] = url
                            if index == 0:
                                img_tag = item.find_element(By.TAG_NAME, 'img')
                                data['cover'] = img_tag
                            elif index == 1:
                                span_tag = item.find_element(By.TAG_NAME, 'span')
                                data['area'] = span_tag.get_attribute('innerHTML')
                            elif index == 2:
                                span_tag = item.find_element(By.TAG_NAME, 'span')
                                data['date'] = span_tag.get_attribute('innerHTML')
                    title_div = video_Item.find_element(By.XPATH, './/div[@class="text-nord4 group-hover:text-nord8"]')
                    title = title_div.get_attribute('innerHTML')
                    data['title'] = title

                    data_map[uuid_string] = data

                

        for id, url in urls.items():
            self.driver.get(url)
            detail_video_div = None
            try:
                detail_video_div = self.wait.until(
                    EC.visibility_of_element_located((By.ID, 'playleft'))
                )
            except Exception as e:
                pass

            if detail_video_div:
                iframe = detail_video_div.find_element(By.TAG_NAME, 'iframe')
                self.driver.switch_to.frame(iframe)
                video_tag = None
                try:
                    video_tag = self.wait.until(
                        EC.visibility_of_element_located((By.XPATH, './/video[@class="dplayer-video dplayer-video-current"]'))
                    )
                except Exception as e:
                    pass
                
                if video_tag:
                    video_url = video_tag.get_attribute('src')
                    data = data_map[id]
                    data['video_url'] = video_url
                    datas.append(data)
                    self.driver.switch_to.default_content()
            
        print(datas)



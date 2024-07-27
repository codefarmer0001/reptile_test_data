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


class comics:

    def __init__(self) -> None:
        self.move_mouse = True
        self.init_chrome()
        self.reptile_list()
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
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        # chrome_options.add_argument(r"user-data-dir=/Users/mac/Library/Application Support/Google/Chrome/Default")
        # user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/598.45 (KHTML, like Gecko) Chrome/103.0.2647 Safari/537.36"
        # user_agent = random.choice(user_agents)
        # chrome_options.add_argument(f'user-agent={user_agent}')
        # chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:19222")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)


    def reptile_list(self):
        self.driver.get('https://18comic.vip/albums?o=mv')
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 8, poll_frequency=0.1)
        self.real_person_verification()

        # self.reptile_top_list()

        time.sleep(300000)
        

    # 验证真人
    def real_person_verification(self):
        is_real_person_ver = None
        # print(11111)
        try:
            is_real_person_ver = self.wait.until(
                # EC.visibility_of_element_located((By.ID, 'CutF7'))
                # EC.visibility_of_element_located((By.ID, 'tVfr5'))
                EC.visibility_of_element_located((By.XPATH, './/h2[@class="h2"]'))
            )
        except Exception as e:
            print(e)
        print(is_real_person_ver)
        if is_real_person_ver:
            is_real_person_ver_txt = is_real_person_ver.get_attribute('innerHTML')
            print(is_real_person_ver_txt)
            if is_real_person_ver_txt and ('请完成以下操作，验证您是真人。' == is_real_person_ver_txt or '正在验证您是否是真人。这可能需要几秒钟时间。' == is_real_person_ver_txt or 'Verify you are human by completing the action below.' == is_real_person_ver_txt):
                
                real_person_ver = self.wait.until(
                    # EC.visibility_of_element_located((By.ID, 'Uiuv1'))
                    EC.visibility_of_element_located((By.ID, 'PYMIw2'))
                )
                print('\n')
                print(real_person_ver)
                if real_person_ver:
                    txt = real_person_ver.get_attribute('outerHTML')
                    print(txt)

                    # 创建 ActionChains 对象
                    
                    time.sleep(3)

                    # 移动到计算出的坐标并点击
                    if self.move_mouse:
                        self.move_mouse = False
                        location = real_person_ver.location

                        # 计算点击点的位置，例如点击元素的中心
                        x = location['x'] + 40 - random.randint(5, 20)
                        y = location['y'] + 75 - random.randint(5, 20)
                        print(f'元素位置：{x},{y}')

                        # 设置随机初始位置
                        initial_x = random.uniform(0, self.driver.execute_script("return window.innerWidth;"))
                        initial_y = random.uniform(0, self.driver.execute_script("return window.innerHeight;"))
                        print(f'鼠标初始化坐标{initial_x},{initial_y}')

                        self.move_mouse_naturally(0, 0, initial_x, initial_y, random.randint(10,30))
                        time.sleep(1)
                        self.move_mouse_naturally(initial_x, initial_y, x, y, random.randint(10,30))
                        # self.driver.refresh()
                        time.sleep(1)

                        self.actions.click().perform()

                    else:
                        self.actions.click().perform()

                    self.real_person_verification()
            else:
                pass
                print('验证完成1')
                self.reptile_top_list()
        else:
            print('验证完成2')
            self.reptile_top_list()
            pass

    def move_mouse_naturally(self, start_x, start_y, end_x, end_y, steps):
        
        for i in range(steps):
            remaining_steps = steps - i

            # 计算剩余距离
            remaining_distance_x = end_x - start_x
            remaining_distance_y = end_y - start_y

            # 平均分配剩余距离
            x_step = remaining_distance_x / remaining_steps
            y_step = remaining_distance_y / remaining_steps

            # 加入随机浮动，模拟人类不规则移动
            x = x_step + random.uniform(-0.5, 0.5)
            y = y_step + random.uniform(-0.5, 0.5)

            # 更新起点
            start_x += x
            start_y += y

            # 执行移动
            self.actions.move_by_offset(x, y).perform()

            # 随机暂停
            time.sleep(random.uniform(0.001, 0.003))

        # 确保最后一步到达终点
        final_x = end_x - start_x
        final_y = end_y - start_y
        self.actions.move_by_offset(final_x, final_y).perform()
        time.sleep(0.05)

        # 爬取主页列表数据
    def reptile_top_list(self):
        # 获取当前页面 URL
        # current_url = self.driver.current_url

        # # 解析 URL 并构造 base URL
        # parsed_url = urlparse(current_url)
        # base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.rsplit('/', 1)[0]}/"

        try:
            billboard_modal_div = self.wait.until(
                EC.visibility_of_element_located((By.ID, 'billboard-modal'))
            )
            if billboard_modal_div:
                chk_cover_button = billboard_modal_div.find_element(By.ID, 'chk_cover')
                print(chk_cover_button)
                self.actions.move_to_element(chk_cover_button).perform()
                self.driver.execute_script("arguments[0].click();", chk_cover_button)
        except Exception as e:
            pass


        try:
            guide_modal_div = self.wait.until(
                EC.visibility_of_element_located((By.ID, 'guide-modal'))
            )
            if guide_modal_div:
                chk_guide_button = guide_modal_div.find_element(By.ID, 'chk_guide')
                print(chk_guide_button)
                self.actions.move_to_element(chk_guide_button).perform()
                self.driver.execute_script("arguments[0].click();", chk_guide_button)
        except Exception as e:
            pass
            

        try:
            top_list_div = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, './/div[@class="col-xs-12 col-md-9 col-sm-8"]'))
            )
            print(top_list_div)

            datas = []

            list_div = top_list_div.find_elements(By.XPATH, './/div[@class="col-xs-6 col-sm-6 col-md-4 col-lg-3 list-col"]')
            url_map = {}
            data_map = {}
            print(len(list_div))
            i = 0
            for item in list_div:
                data_item = {}
                if i < 8:
                    i += 1
                    title_span = item.find_element(By.XPATH, './/span[@class="video-title title-truncate m-t-5"]')
                    title = title_span.get_attribute('innerHTML')
                    data_item['title'] = title
                    # print(title)
                    author_div = item.find_element(By.XPATH, './/div[@class="title-truncate hidden-xs"]')
                    author_a = author_div.find_element(By.TAG_NAME, 'a')
                    author = author_a.get_attribute('innerHTML')
                    data_item['author'] = author
                    # print(author)
                    image_view = item.find_element(By.TAG_NAME, 'img')
                    image_src = image_view.get_attribute('src')
                    data_item['cover'] = image_src
                    # print(image_src)
                    tag_a = item.find_element(By.TAG_NAME, 'a')
                    tag_a_href = tag_a.get_attribute('href')
                    pattern = r'/album/(\d+)/'

                    match = re.search(pattern, tag_a_href)
                    album_id = ''
                    if match:
                        album_id = match.group(1)
                        data_item['id'] = album_id
                        # print(f"Album ID: {album_id}")
                    else:
                        print("No match found")
                    url_map[album_id] = tag_a_href

                    data_map[album_id] = data_item
                    # datas.append(data_item)
                    # print('\n')

            for id, url in url_map.items():
                # print(url)
                tags, chapter, info = self.reptile_detail(url)
                data_item = data_map[id]
                data_item['tag'] = tags
                data_item['chapters'] = chapter
                data_item['intro'] = info

                datas.append(data_item)
            print(datas)
                    
        except Exception as e:
            print(e)
        pass


    def reptile_detail(self, url):
        try:
            
            self.driver.get(url)
            print(url)
            main_div = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, './/div[@class="panel panel-default visible-lg hidden-xs"]'))
            )
            print(main_div)
            chapters = []
            tags = []
            info = ""
            if main_div:
                tags_span = main_div.find_element(By.XPATH, './/span[@itemprop="genre"]')
                tags_a = tags_span.find_elements(By.TAG_NAME, 'a')
                
                for tags_a_item in tags_a:
                    # print(tags_a_item.get_attribute('innerHTML'))
                    tag = tags_a_item.get_attribute('innerHTML')
                    tags.append(tag)
                # print(tags_a)
                ul_chapters_tag = main_div.find_element(By.XPATH, './/ul[@class="btn-toolbar "]')
                a_chapters_tags = ul_chapters_tag.find_elements(By.TAG_NAME, 'a')
                
                for a_chapters_tags_item in a_chapters_tags:
                    li_chapters_tags = a_chapters_tags_item.find_element(By.TAG_NAME, 'li')
                    html_content = li_chapters_tags.get_attribute('innerHTML')
                    text = re.sub(r'<[^>]+>', '', html_content)
                    # print(text)
                    chapter = text
                    chapters.append(chapter)
                info_tags = main_div.find_elements(By.XPATH, './/div[@class="p-t-5 p-b-5"]')
                
                if len(info_tags) > 2:
                    info = info_tags[1].get_attribute('innerHTML')
            return tags, chapters, info
        except Exception as e:
            print(e)
            return '', [], []
            pass
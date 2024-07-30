from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import base64
import os
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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

        # 监听performance,用于抓取日志
        chrome_options.set_capability('goog:loggingPrefs', {"performance": "ALL"})

        # 配置日志
        logging_prefs = {
            'performance': 'ALL'
        }
        chrome_options.set_capability('goog:loggingPrefs', logging_prefs)

        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:19222")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        # 连接到 DevTools



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
            # print(sixItem_container_div.get_attribute('innerHTML'))
            video_Item_div = sixItem_container_div.find_elements(By.XPATH, './/div[@class="Video-Item"]')
            if video_Item_div and list_index < len(video_Item_div):
                # for item in  video_Item_div:
                item = video_Item_div[list_index]
                print('\n')
                # print(item.get_attribute('innerHTML'))
                van_image_div = item.find_element(By.XPATH, './/div[@class="van-image"]')
                image_tag = van_image_div.find_element(By.XPATH, './/img[@class="van-image__img"]')
                cover = image_tag.get_attribute('src')
                # print(cover)
                data['cover'] = cover
                
                title_div = item.find_element(By.XPATH, './/div[@class="title"]')
                title = title_div.get_attribute('innerHTML')
                # print(title)
                data['title'] = title

                base64_data = self.get_file_content_chrome(cover)
                # print(base64_data)
                dir = f'src/douyindata/{title}'
                self.create_directory_if_not_exists(dir)
                self.save_base64_as_file(base64_data, f'{dir}/cover.png')
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
                # print(views)
                data['views'] = views
                # print(popularity)
                data['popularity'] = popularity
                duration_div = item.find_element(By.XPATH, './/div[@class="duration"]')
                duration = duration_div.get_attribute('innerHTML')
                # print(duration)
                data['duration'] = duration
                user_info_div = item.find_element(By.XPATH, './/div[@class="user"]')
                img_tag = user_info_div.find_element(By.TAG_NAME, 'img')
                author_avatar = img_tag.get_attribute('src')
                # print(author_avatar)
                data['author_avatar'] = author_avatar

                base64_data = self.get_file_content_chrome(author_avatar)
                # print(base64_data)
                self.save_base64_as_file(base64_data, f'{dir}/author_avatar.png')

                author_span_tag = user_info_div.find_element(By.TAG_NAME, 'span')
                author = author_span_tag.get_attribute('innerHTML')
                # print(author)
                data['author'] = author
                self.actions.move_to_element(item).perform()
                self.driver.execute_script("arguments[0].click();", item)
                video_url, tags = self.reptile_detail()
                print(video_url)
                data['video_url'] = video_url
                # print(tags)
                data['tags'] = tags
                time.sleep(3)
                self.datas.append(data)
                
                # console_logs = self.driver.get_log('performance')

                # # 连接到 DevTools
                # self.driver.execute_cdp_cmd('Network.enable', {})
                # self.driver.execute_cdp_cmd('Network.setRequestInterception', {'patterns': [{'urlPattern': '*'}]})

                # def log_request(request):
                #     print(request['url'])
                #     if request['url'].endswith('.m3u8'):
                #         print(f'M3U8 URL found: {request["url"]}')

                # self.driver.request_interceptor = log_request
                # 打开文件（如果文件不存在会创建文件，如果文件已存在会覆盖）
                # with open('output.txt', 'w', encoding='utf-8') as file:
                #     for log in console_logs:
                #         # 将字典转换为 JSON 字符串
                #         log_json = json.dumps(log, indent=4)  # indent=4 用于格式化输出
                #         # 写入文本到文件
                #         file.write(log_json + '\n')


                performance_logs = self.driver.get_log("performance")
                with open(f'{dir}/output.txt', 'w', encoding='utf-8') as file:
                    for performance_log in performance_logs:
                        # performance_log内容: {"level": "INFO", message:"json字符串", "timestamp": 1694067123380}
                        message = json.loads(performance_log["message"])
                        # message内容: {"webview":"webview","message":{"method":"Network.requestWillBeSent","params":{}}}
                        message = message['message']
                        # 筛选事件: https://chromedevtools.github.io/devtools-protocol/tot/Network/
                        if message["method"] == 'Network.requestWillBeSent':
                            print("requestWillBeSent", json.dumps(message))
                            file.write(json.dumps(message) + '\n')
                            

                        # 请求头
                        if message["method"] == 'Network.responseReceived':
                            print("responseReceived", json.dumps(message))
                            file.write(json.dumps(message) + '\n')
                        


                # print("文本已成功写入到文件。")
                # print(console_logs)
                # self.get_blob_video()

                # self.datas.append(data)
                self.driver.refresh()
                if list_index < 5:
                    list_index += 1
                    # print(list_index)
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
    



    def get_file_content_chrome(self, uri):
        result = self.driver.execute_async_script("""
            var uri = arguments[0];
            var callback = arguments[1];
            var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
            var xhr = new XMLHttpRequest();
            xhr.responseType = 'arraybuffer';
            xhr.onload = function(){ callback(toBase64(xhr.response)) };
            xhr.onerror = function(){ callback(xhr.status) };
            xhr.open('GET', uri);
            xhr.send();
            """, uri)
        # print(result)
        if type(result) == int:
            raise Exception("Request failed with status %s" % result)
        return result



    def save_base64_as_file(self, base64_str, output_path):
        with open(output_path, 'wb') as file:
            file.write(base64.b64decode(base64_str))


    def create_directory_if_not_exists(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created.")
        else:
            print(f"Directory '{directory_path}' already exists.")



    def get_blob_video(self):
        # 访问目标页面
        # self.driver.get(url)

        # 获取性能日志
        logs = self.driver.get_log('browser')
        print(logs)
        # 提取网络请求数据
        for entry in logs:
            log = json.loads(entry['message'])['message']
            if log['method'] == 'Network.responseReceived':
                request_id = log['params']['requestId']
                response = log['params']['response']
                url = response['url']
                if 'blob:' in url:
                    print(f"Found blob URL: {url}")
                if 'm3u8' in url:
                    print(f"Found m3u8 URL: {url}")
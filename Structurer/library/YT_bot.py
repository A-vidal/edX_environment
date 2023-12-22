
import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *

class Bot:
    # constructor of the bot and open the chrome page
    def __init__(self, path: str, jsonfile: str = "./Data/chrome_options.json", debug: bool = False,):
        # path: where the bot is going to work
        # debug: to activate the console logs to debug
        # jsonfile

        with open(jsonfile) as file:
            dic = json.load(file)
            chrome_path = dic["chrome_path"]
            path_UserData = dic["path_UserData"]
            driver_path = dic["driver_path"]
            del dic

        options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--log-level=3")
        options.add_argument("user-data-dir=" + path_UserData)
        options.add_argument("start-maximized")
        # options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        # options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        options.binary_location = chrome_path
        
        try:
            driver_final_path = path.split("/")[0] + "/" + driver_path[driver_path.find("/"):]
            service = Service(driver_final_path)
            self.bot = webdriver.Chrome(options, service)
        except SessionNotCreatedException:
            print(driver_final_path)
            raise BaseException("The cromedriver.exe is not up-date")
        
        self.link_YTstudio = "https://studio.youtube.com/channel/UCkanTv6l_aY6PM_lskgbrlg?c=UCkanTv6l_aY6PM_lskgbrlg"
        
        if path.startswith(".."):
            self.path = "\\".join(os.getcwd().split("\\")[:-1]) + path.lstrip(".").replace("/","\\")
        elif path.startswith("."):
            self.path = os.getcwd() + path.lstrip(".").replace("/","\\")
        elif path.lower().startswith("c:"):
            self.path = path.replace("/","\\")
        else:
            raise AttributeError
        
        self.path = self.path.rstrip("\\").lstrip("\\")
        
        self.debug = debug
    
    # transform a linux/web path to an Win path
    def path_transform(self, path:str) -> str:
        # path: the linux/web original path
        # output: the new Win path
        if path.startswith("."):
            ret = self.path +  path.lstrip(".").replace("/","\\")
        elif path.lower().startswith("c:"):
            ret = path.replace("/","\\")
        else:
            raise AttributeError
        
        ret.lstrip("\\").rstrip("\\")
        
        return ret
    
    # change the YouTube studio link
    def set_YTstudio(self, link:str):
        # link: the new link
        self.link_YTstudio = link

    # to fill an input text with assertiveness
    def input_text(self, input, text) -> None:
        # input: textbox input
        # text: text to put in
        while input.text != "":
            input.clear()
            time.sleep(1)

        while input.text != text:
            input.clear()
            input.send_keys(text)
            time.sleep(1)
        
        return
    
    # a function to include a video in diferent playlists
    def list_in(self, *name: tuple[str]):
        # name: a substring of the playlists names that are going to be the video
        self.bot.find_element(By.CSS_SELECTOR, "#basics ytcp-dropdown-trigger").click()
        time.sleep(1)
        
        lists = self.bot.find_elements(By.CSS_SELECTOR, "div#items ytcp-ve")
        list_selector = self.bot.find_element(By.CSS_SELECTOR, "array-selector#selector")
        info = list_selector.get_property("__data")["items"]

        for i in range(len(info)):
            if any(filter(lambda x: (x in info[i]["label"]), name)) != info[i]["checked"]:
                lists[i].find_element(By.CSS_SELECTOR, "div#checkbox-container").click()

        self.bot.find_element(By.CSS_SELECTOR, "ytcp-button.done-button div").click()
    
    # upload a video
    def subir_video(self, path : str, name : str, desc: str) -> str:
        # path: path of the video
        # name: name of the video
        # desc: description of the video
        # output: the 11 character YouTube code of the video
        if self.bot.current_url != self.link_YTstudio: 
            self.bot.get(self.link_YTstudio)
            time.sleep(7)
        
        if self.debug:
            print("Start")
        
        try:
            upload_button = self.bot.find_element(By.CSS_SELECTOR, "#upload-button")
            upload_button.click()
        except:
            upload_button = self.bot.find_element(By.CSS_SELECTOR, "ytcp-icon-button#upload-icon")
            upload_button.click()
        time.sleep(1)
        
        if self.debug:
            print("Upload button")

        file_input = self.bot.find_element(By.XPATH, '//*[@id="content"]/input')
        
        file_input.send_keys(self.path_transform(path))
        
        if self.debug:
            print("Video to upload")

        time.sleep(5)
        
        title_input, description_input = self.bot.find_elements(By.XPATH, '//*[@id="textbox"]')
        
        self.input_text(title_input, name)
        
        if self.debug:
            print("Title")

        self.input_text(description_input, desc)
        time.sleep(1)
        
        if self.debug:
            print("Description")

        MC_code = name.split(".")[0]
        self.list_in(MC_code)

        next_button = self.bot.find_element(By.XPATH, '//*[@id="next-button"]')
        for i in range(3):
            next_button.click()
            time.sleep(1)
        
        if self.debug:
            print("Options")
        
        # oculto_option = self.bot.find_elements(By.XPATH, '//*[@id="radioLabel"]')[2]
        oculto_option = self.bot.find_element(By.CSS_SELECTOR, 'tp-yt-paper-radio-button[name="UNLISTED"]')
        oculto_option.click()
        
        if self.debug:
            print("Visibility")
        
        link = self.bot.find_element(By.CSS_SELECTOR, 'a.ytcp-video-info')
        ret = link.text[-11:]
        
        if self.debug:
            print("link")

        done_button = self.bot.find_element(By.XPATH, '//*[@id="done-button"]')
        done_button.click()
        time.sleep(3)
        
        if self.debug:
            print("Done")
        
        try:
            cerrar_button = self.bot.find_element(By.CSS_SELECTOR, 'ytcp-button#close-button div')
            cerrar_button.click()
        except:
            pass
        time.sleep(2)
        
        if self.debug:
            print("Continue")
        
        return ret

    # a function to manage alerts
    def possibleAlert(self, ret: bool) -> bool:
        # ret: if you want to accept or dismiss the alert
        # output: if there were an alert or not
        try:
            alert = self.bot.switch_to.alert
            if ret:
                alert.accept()
            else:
                alert.dismiss()
            return True
        except:
            return False
    
    # modifies the playlist description and name
    def list_name(self, code, name) -> None:
        # code: course code to find the playlist
        # name: the name of the course
        while True:
            self.bot.get(f"https://studio.youtube.com/channel/UCkanTv6l_aY6PM_lskgbrlg/content/playlists?c=UCkanTv6l_aY6PM_lskgbrlg")
            if not self.possibleAlert(False):
                break
            time.sleep(5)

        time.sleep(1)

        self.bot.refresh()
        time.sleep(2)

        # self.bot.find_element(By.CSS_SELECTOR, "#footer ytcp-dropdown-trigger").click()
        #self.bot.find_element(By.CSS_SELECTOR, "#text-item-2").click()
        #time.sleep(1)

        playlist = self.bot.find_elements(By.CSS_SELECTOR, "div#playlist-table-content ytcp-playlist-row")

        for i in range(len(playlist)):
            title = playlist[i].find_element(By.CSS_SELECTOR, "a#playlist-title-link")

            if title.text != code and title.text != (code+ " - " +name):
                continue

            title.click()
            time.sleep(1)
            title_input, description_input = self.bot.find_elements(By.XPATH, '//*[@id="textbox"]')

            while title_input.text != "":
                title_input.clear()
                time.sleep(1)
            
            title_input.send_keys(code+ " - " +name)

            while description_input.text != "":
                description_input.clear()
                time.sleep(1)
            
            description_input.send_keys(
                "These are the videos of a Master of RES4City.\n\nFor more information, please visit the following website:\nhttps://www.res4city.eu/"
            )
            time.sleep(1)
            try:
                self.bot.find_element(By.CSS_SELECTOR, "ytcp-button#save").click()
                print("save playlist")
            except Exception as ex:
                print(f"Error: {type(ex).__name__}")
                self.bot.find_element(By.CSS_SELECTOR, "ytcp-button#discard").click()
                print("discard playlist")
            
            time.sleep(1)
            self.possibleAlert(True)
            self.bot.find_element(By.CSS_SELECTOR, "div#contentIcon").click()

            playlist = self.bot.find_elements(By.CSS_SELECTOR, "div#playlist-table-content ytcp-playlist-row")
    
    # when the videos are uploaded, goes to a default page to close the bot
    def save_closing(self) -> None:
        here = os.getcwd().replace('\\', '/')
        print(here)
        while True:
            self.bot.get(f"file:///{here}/Data/close_bot.html")
            if not self.possibleAlert(False):
                break
            time.sleep(1)
        while True:
            try:
                close = self.bot.find_element(By.XPATH, '//*[@id="closing"]')
                if close.is_displayed():
                    break
                else:
                    time.sleep(1)
                    continue
            except:
                time.sleep(1)
        self.bot.close()
    
    def __delattr__(self, __name: str) -> None:
        while True:
            self.bot.close()
            if not self.possibleAlert(False):
                break
            time.sleep(1)
        pass

    def test(path: str = "./", jsonpath: str = "./Data/chrome_options.json"):
        bot = Bot(path, jsonpath, True)
        bot.bot.get(bot.link_YTstudio)
        del bot

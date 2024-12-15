from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tqdm import tqdm


import pandas as pd
import numpy as np

import pickle
import time
import re

class ChromeDriverManager:
    def __init__(self,
                 user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                 debugger_address="127.0.0.1:9221",
                 chrome_driver_path="/Applications/Google\ Chrome.app/Contents/MacOS/Google"
                ):
        
        """ ChromeDriver 환경 설정 """
        
        self.user_agent = user_agent
        self.debugger_address = debugger_address
        self.chrome_driver_path = chrome_driver_path

        # Chrome Options 설정
        self.chrome_options = Options()
        self.chrome_options.add_argument(f"user-agent={self.user_agent}")
        self.chrome_options.add_experimental_option("debuggerAddress", self.debugger_address)

        # ChromeDriver Service 설정
        self.service = ChromeService(executable_path=self.chrome_driver_path)

        # WebDriver 초기화
        # self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.driver = webdriver.Chrome(options=self.chrome_options)
    
    def get_driver(self):
        """ WebDriver 객체를 반환합니다. """
        # 다른 추가 작업에서 사용함
        return self.driver

    def close_driver(self):
        """ WebDriver를 닫습니다. """
        self.driver.quit()

class SeleniumScraper(ChromeDriverManager):
    def __init__(self, base_url=None, search_url=None):
        """ ChromeDriverManager를 상속받아 WebScraper 클래스를 초기화 """
        super().__init__()  # 부모 클래스 기본값 사용
        self.load_wait = WebDriverWait(self.driver, 10)
        
        # SeleniumScraper 전용 속성 추가
        self.base_url = base_url
        self.search_url = search_url


    def get_search(self, search_keyword, search_object, button_object):
        """
        주어진 키워드로 검색을 수행하는 메서드.
        
        Parameters:
            search_keyword (str): 검색 키워드.
            search_xpath (str): 검색 입력창의 요소.
            button_xpath (str): 검색 버튼의 요소.
        """
        # URL 이동
        self.driver.get(self.search_url)
    
        # 검색 입력창이 로드될 때까지 대기
        search_element = self.load_wait.until(EC.presence_of_element_located((By.XPATH, search_object)))
    
        # 키워드 입력
        search_element.send_keys(search_keyword)
    
        # 검색 버튼이 로드될 때까지 대기 후 클릭
        button_element = self.load_wait.until(EC.element_to_be_clickable((By.XPATH, button_object)))
        button_element.click()


    def filterlng(self, parent_object, child_object):

        # Class nm
        parent_cls_nm = (By.CLASS_NAME, parent_object)
        parent_button = self.load_wait.until(EC.element_to_be_clickable(parent_cls_nm))
        parent_button.click()
        
        # data-test
        child_datatest = (By.CSS_SELECTOR, child_object)
        child_button = self.load_wait.until(EC.element_to_be_clickable(child_datatest))
        actions = ActionChains(self.driver)
        actions.move_to_element(child_button).click().perform()

 
   
    
    
    
    
    
    
    
    

from cgitb import html
from typing_extensions import Self
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver    
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By




class Colossus(object):
    def __init__(self, *args):
        self.service=Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument("disable-gpu")
        self._driver = webdriver.Chrome(service=self.service,chrome_options=self.options)
        self._url = ""
        self.soup = None
        
    def _set_url(self, url):
        self._url = url

    def _load_url(self):
        self._driver.get(self._url)

    def _get(self):
        self._load_url()
        self.soup = BeautifulSoup(self._driver.page_source,"html.parser")

    def _procesar_respuestas(self , resultado ):
        return [ i.text for i in resultado]
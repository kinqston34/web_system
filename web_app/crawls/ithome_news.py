# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 15:46:32 2023

@author: USER
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
# from bs4 import BeautifulSoup
# import time

class IThome_News():

    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self.ithome = webdriver.Chrome(options=options)

    def __str__(self):
        return "IThome"

    def quit(self):
        self.ithome.quit()

    def news_init(self):

        url = "https://www.ithome.com.tw/news"
        self.ithome.get(url)

        self.news = {"source":[],"href":[],"description":[]}

    def get_news(self):
        self.news_init()
        # 重大新聞
        title = self.ithome.find_element(By.CSS_SELECTOR,"div.title a")
        content = self.ithome.find_element(By.CSS_SELECTOR,"div.summary p")

        self.news["source"].append(title.text)
        self.news["href"].append(title.get_attribute("href"))
        self.news["description"].append(content.text)

        #底下的新聞 目前只取第一頁
        title = self.ithome.find_elements(By.CSS_SELECTOR,"div.item p.title a")
        content = self.ithome.find_elements(By.CSS_SELECTOR,"div.item div.summary")

        for i,j in zip(title,content):
            self.news["source"].append(i.text)
            self.news["href"].append(i.get_attribute("href"))
            self.news["description"].append(j.text)

        return self.news

    def news_django_used(self):  #也是json格式
        self.news_init()
        article = []
        #重大新聞
        title = self.ithome.find_element(By.CSS_SELECTOR,"div.title a")
        content = self.ithome.find_element(By.CSS_SELECTOR,"div.summary p")

        article.append({"source":title.text,"href":title.get_attribute("href"),"description":content.text})
        #底下的新聞 目前只取第一頁
        title = self.ithome.find_elements(By.CSS_SELECTOR,"div.item p.title a")
        content = self.ithome.find_elements(By.CSS_SELECTOR,"div.item div.summary")

        for t,c in zip(title,content):
            article.append({"source":t.text,"href":t.get_attribute("href"),"description":c.text})
        return article

class IThome_Tech(IThome_News):

    def __init__(self):
        super().__init__()

    def news_init(self):

        url = "https://www.ithome.com.tw/tech"
        self.ithome.get(url)
        self.news = {"source":[],"href":[],"description":[]}

class IThome_Security(IThome_News):

    def __init__(self):
        super().__init__()

    def news_init(self):

        url = "https://www.ithome.com.tw/security"
        self.ithome.get(url)
        self.news = {"source":[],"href":[],"description":[]}



# a = IThome_Security()
# print(a.news_django_used())
# # time.sleep(5)
# a.quit()
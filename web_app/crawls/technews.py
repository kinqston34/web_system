# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 23:12:33 2024

@author: Administrator
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

class TechNews():
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self.technews = webdriver.Chrome(options=options)    
    
    def __str__(self):
        return "TechNews"

    def quit(self):
        self.technews.quit()
    
    def news_init_(self):
        
        url = "https://technews.tw/"
        self.technews.get(url)
        
    def news_django_used(self): 
        #最新文章第一頁
        self.news_init_()
        article = []
        soup = BeautifulSoup(self.technews.page_source,"html.parser")
        title = soup.select("h1.entry-title a")
        content = soup.select("div.moreinf")
        
        for i,j in zip(title,content):
            article.append({"source":i.text,"href":i["href"],"description":j.text.split("繼續閱讀..")[0]})
        return article

class TechNews_Tech(TechNews):
    
    def __init__(self):
        super().__init__()
        
    def news_init_(self):
        url = "https://technews.tw/category/cutting-edge/"
        self.technews.get(url)

class TechNews_Semi(TechNews):
    
    def __init__(self):
        super().__init__()
        
    def news_init_(self):
        url = "https://technews.tw/category/semiconductor/"
        self.technews.get(url)

class TechNews_Net(TechNews):
    
    def __init__(self):
        super().__init__()
        
    def news_init_(self):
        url = "https://technews.tw/category/internet/"
        self.technews.get(url)
    

# a = TechNews_Net()
# # a = TechNews()
# article = a.news_django_used()
# print(article)
# a.quit()
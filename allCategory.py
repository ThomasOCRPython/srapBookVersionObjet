import requests
from bs4 import BeautifulSoup
import time
from category import Category

class AllCategory:
    def __init__(self,url):
        self.url = url
        self.categorys = []
        self.urls_links =[]

    def __get_url_category(self,soup):
        url_link_category = []

        urls = soup.find("ul", {"class": "nav nav-list"}).findAll("li")
        for url in urls:
            a = url.find("a")
            url_category = a["href"]
            if url_category == "catalogue/category/books_1/index.html":
                continue
            else:
                url_link_category.append("http://books.toscrape.com/" + url_category)
        return url_link_category


    def get_all_category(self,url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        urls_links = self.__get_url_category(soup)
        

        for url_link in urls_links:
            self.urls_links.append(url_link)
            category=Category(url_link)
            self.categorys.append(category)
            

    def run(self):
        compteur=0
        for category,url_link in zip(self.categorys,self.urls_links):
            category.get_book_each_category(url_link)
            category.run()
            compteur+=1
            print(compteur)
            
                   
                
categorys = AllCategory("http://books.toscrape.com/index.html")
categorys.get_all_category("http://books.toscrape.com/index.html")
categorys.run()
   
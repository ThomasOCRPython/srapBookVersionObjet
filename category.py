import requests
from Livre import Book
from bs4 import BeautifulSoup
from math import *
import re



class Category:
    def __init__(self, url):
        self.url = url
        self.category_name = ""
        self.books = []
    
    def __get_number_of_page(self,url):
        page = requests.get(url)
        if page.ok:
            soup = BeautifulSoup(page.text, "html.parser")
            nb_book = soup.find("form", {"class": "form-horizontal"}).find("strong").text
            if int(nb_book) > 20:
                resultat = ceil(int(nb_book) / 20)
            else:
                resultat = 1
        return resultat


    def get_url_category(self,url):
        resultat = self.__get_number_of_page(url)
        # print(resultat)
        urls_links = []
        if resultat > 1:
            url1 = url.replace("index.html", "")
            for i in range(1, resultat + 1):
                URL = url1 + "page-" + str(i) + ".html"
                r = requests.get(URL)
                if r.ok:
                    #print("page :" + str(i))
                    soup = BeautifulSoup(r.text, "html.parser")
                    articles = soup.findAll("article")
                    for article in articles:
                        a = article.find("a")
                        link = a["href"]
                        urls_links.append("http://books.toscrape.com/" + link)
        else:
            r = requests.get(url)
            if r.ok:
                soup = BeautifulSoup(r.text, "html.parser")
                articles = soup.findAll("article")
                for article in articles:
                    a = article.find("a")
                    link = a["href"]
                    urls_links.append("http://books.toscrape.com/" + link)
        # print(len(links))
        return urls_links

    def __fill_category_name(self,url):
        url_category_name = url.replace(
            "http://books.toscrape.com/catalogue/category/books/", ""
            )
        category_name = re.sub(r"[0-9]+", "", url_category_name)
        self.category_name = category_name.replace("_/index.html", "")
        


    def search_image(self,books, folder_image):
        for image in books:
            picture = image["image_url"]
            page = requests.get(picture)
            file_name = picture.split("/")[-1]
            file_picture = Path(folder_image, file_name)
            with open(file_picture, "wb") as f:
                f.write(page.content)


    def get_book_each_category(self,url):
        urls_books = []
        
        clean_urls_categorys = self.get_url_category(url)
        for clean_url_category in clean_urls_categorys:
            replace_url = clean_url_category.replace("/../../../", "/catalogue/")
            urls_books.append(replace_url)

        for url_book in urls_books:
            book = Book(url_book)
            self.books.append(book)
    def run(self):
        for book in self.books:
            book.scrap()
            print (book)       

        
category = Category("http://books.toscrape.com/catalogue/category/books/new-adult_20/index.html")
category.get_book_each_category("http://books.toscrape.com/catalogue/category/books/new-adult_20/index.html")
category.run()           
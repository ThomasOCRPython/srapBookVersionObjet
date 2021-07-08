import requests
from Livre import Book
from bs4 import BeautifulSoup
from math import *


class Category:
    def __init__(self, url):
        self.url = url
        self.category_name = ""
        self.books = []
    
    def get_number_of_page(self,url):
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
        resultat = get_number_of_page(url)
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
            r = requests.get(self,url)
            if r.ok:
                soup = BeautifulSoup(r.text, "html.parser")
                articles = soup.findAll("article")
                for article in articles:
                    a = article.find("a")
                    link = a["href"]
                    urls_links.append("http://books.toscrape.com/" + link)
        # print(len(links))
        return links

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
        self.books = []

        clean_urls_categorys = get_url_category(self,url)
        for clean_url_category in clean_urls_categorys:
            replace_url = clean_url_category.replace("/../../../", "/catalogue/")
            urls_books.append(replace_url)
            # print(replace_url)

        for url_book in self.urls_books:
            book = Book(url_book)
            self.books.append(book)

        category = self.__fill_category_name(url)
        folder_category = Path("./Data/", category)
        folder_category.mkdir(exist_ok=True, parents=True)
        folder_image = Path(folder_category, "image")
        folder_image.mkdir(exist_ok=True)
        file_category = Path(folder_category, category + ".csv")

        search_image(books, folder_image)

        with open(file_category, "w", encoding="utf-8-sig", newline="") as f:
            fieldnames = books[0].keys()
            writer = csv.DictWriter(f, delimiter=";", fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(books)

category = Category("http://books.toscrape.com/catalogue/category/books/new-adult_20/index.html")
category.get_book_each_category("http://books.toscrape.com/catalogue/category/books/new-adult_20/index.html")           
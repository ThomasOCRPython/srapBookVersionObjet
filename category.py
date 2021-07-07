import requests
from Livre import Book
from bs4 import BeautifulSoup
from math import *


class Category:
    def __init__(self, url):
        self.url = url
        self.category_name = ""
        self.books = []
    
    def get_url_category(url):
        page = requests.get(url)
        if page.ok:
            soup = BeautifulSoup(page.text, "html.parser")
            nb_book = soup.find("form", {"class": "form-horizontal"}).find("strong").text
            if int(nb_book) > 20:
                resultat = ceil(int(nb_book) / 20)
            else:
                resultat = 1
        book_links = []
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
                        book_links.append("http://books.toscrape.com/" + link)
        else:
            r = requests.get(url)
            if r.ok:
                soup = BeautifulSoup(r.text, "html.parser")
                articles = soup.findAll("article")
                for article in articles:
                    a = article.find("a")
                    link = a["href"]
                    book_links.append("http://books.toscrape.com/" + link)
    
                for url in book_links:
                    book = Book(url)
                    self.books.append(book)
       
    
    #####################################################################################
    def get_category_name(url):
        url_category_name = url.replace(
            "http://books.toscrape.com/catalogue/category/books/", ""
        )
        category_name = re.sub(r"[0-9]+", "", url_category_name)
        self.category_name = category_name.replace("_/index.html", "")
        


    def search_image(books, folder_image):
        for image in books:
            picture = image["image_url"]
            page = requests.get(picture)
            file_name = picture.split("/")[-1]
            file_picture = Path(folder_image, file_name)
            with open(file_picture, "wb") as f:
                f.write(page.content)


    def get_book_each_ategory(url):
        urls_books = []
        books = []

        clean_urls_categorys = cat.get_url_category(url)
        for clean_url_category in clean_urls_categorys:
            replace_url = clean_url_category.replace("/../../../", "/catalogue/")
            urls_books.append(replace_url)
            # print(replace_url)

        for url_book in urls_books:
            book = search_book.get_book(url_book)
            books.append(book)

        category = get_category_name(url)
        folder_category = Path("./data/", category)
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
            
    def run_book_scrap(self):
        for book in self.books:
            book.scrap()
            print(book)
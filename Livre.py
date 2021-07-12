import requests
from bs4 import BeautifulSoup

class Book:

    def __init__(self, url):
        self.url = url
        self.title = ""
        self.category = ""
        self.upc=""
        self.price_including_tax=""
        self.price_excluding_tax=""
        self.number_available=""
        self.description=""
        self.review_rating=""
        self.image_url=""
        self.tax=""
        
    def scrap(self):    
        book = requests.get(self.url)        
        soup = BeautifulSoup(book.content, "html.parser")
        self.__fill_title(soup) 
        self.__fill_category(soup)
        self.__fill_upc(soup)
        self.__fill_price_including_tax(soup)
        self.__fill_price_excluding_tax(soup)
        self.__fill_number_available(soup)
        self.__fill_description(soup)
        self.__fill_review_rating(soup)
        self.__fill_image_url(soup)
        self.__fill_tax(soup)
        
    def __fill_title(self,soup): 
        title = soup.find("div", {"class": "col-sm-6 product_main"}).find("h1")
        self.title= title.text
        # return self.title
        
    
    def __fill_category(self,soup):
         category = soup.findAll("li")
         category2 = category[2].text
         self.category = category2.replace("\n", "")
        #  return self.category

    def __fill_upc(self,soup):
        tds = soup.findAll("td")
        self.upc = tds[0].text

    def __fill_price_including_tax(self,soup):
        tds = soup.findAll("td")
        self.price_including_tax = tds[3].text

    def __fill_price_excluding_tax(self,soup):
        tds = soup.findAll("td")
        self.price_excluding_tax = tds[2].text

    def __fill_number_available(self,soup):
        tds = soup.findAll("td")
        self.number_available = tds[5].text

    def __fill_description(self,soup):
        div = soup.find("div", class_="sub-header")
        p = div.find_next_sibling()
        self.description = p.text
        # return self.description

    def __fill_review_rating(self,soup):
        p = soup.find("div", {"class": "col-sm-6 product_main"}).find(
           "p", class_="star-rating"
        )
        rating = str(p["class"])
        star = rating[15:-1]
        star_rating = eval(star)
        return star_rating
        

    def __fill_image_url(self,soup):
        image = soup.find("div", {"class": "item active"}).find("img")
        image_url = image["src"]
        image_clean_url = image_url.replace("../../", "http://books.toscrape.com/")
        self.image_url = image_clean_url

    def __fill_tax(self,soup):
        tds = soup.findAll("td")
        self.tax = tds[4].text

    def __str__(self):
        output = f"url : {self.url} \ntitle : {self.title} \ncategory : {self.category}  \nupc : {self.upc}  \nprice_including_tax : {self.price_including_tax} \nprice_excluding_tax : {self.price_excluding_tax}  \nnumber_available : {self.number_available}  \ndescription : {self.description} \nreview_rating : {self.review_rating}  \nimage_url : {self.image_url}  \ntax : {self.tax} "
        return output
        
        

    
# book = Book("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
# book.scrap("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
# print(book)

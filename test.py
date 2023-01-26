import requests
import sys
import os
import difflib
from bs4 import BeautifulSoup

film_title = "The ninth gate"
URL = f"https://www.rottentomatoes.com/search?search={film_title}"

def init_request(film_title, url):
    response = requests.get(url, headers={"User-Agent": "Mozilla", "Accept-Language": "en-US,en;q=0.5"})
    parsed_html_mainpage = BeautifulSoup(response.text, "html.parser")
    title_data = parsed_html_mainpage.select("#search-results")
    return title_data

class RottenTomatoes:

    url = f"https://www.rottentomatoes.com/search?search={film_title}"

    def __init__(self, film_title):
    	self.film_title = film_title

    def __get_final_web(self, url):

        self.title_data = init_request(film_title, url)

        for title in self.title_data:
			pass
			
    	page_response = requests.get(link, headers={"User-Agent": "Mozilla", "Accept-Language": "en-US,en;q=0.5"})
    	parsed_html_film_page = BeautifulSoup(page_response.text, "html.parser")



if __name__ == "__main__":
    rotten = RottenTomatoes(film_title)
    print(rotten.url)



        






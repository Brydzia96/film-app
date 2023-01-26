import requests
import sys
import os
import difflib
import string
from bs4 import BeautifulSoup


def init_request(film_title, url, selector):
    response = requests.get(url, headers={"User-Agent": "Mozilla", "Accept-Language": "en-US,en;q=0.5"})
    parsed_html_mainpage = BeautifulSoup(response.text, "html.parser")
    title_data = parsed_html_mainpage.select(selector)
    return title_data

def cutting_around_string(string, cutting_list=None):
        string = string.split(f'{cutting_list[0]}')[1]
        string = string.split(f'{cutting_list[1]}')[0]
        return string


def string_similarity(str1, str2):
    result =  difflib.SequenceMatcher(a=str1.lower(), b=str2.lower())
    return result.ratio()

   
class RottenTomatoes:    

    def __init__(self, film_title, film_year):
        self.film_title = film_title
        self.film_year = film_year
        self.url = f"https://www.rottentomatoes.com/search?search={self.film_title}"

    def __get_final_web(self, url):

        checkpoint = False
        self.title_data = init_request(self.film_title, url, "#search-results > search-page-result")
        new = BeautifulSoup(str(self.title_data), "html.parser")
        media_list = [x for x in new.find_all('search-page-media-row')]
        for item in media_list:
            try:
                year = item['releaseyear']
                if year != self.film_year:
                    continue
                a_tags = [x for x in item.find_all('a')]
                link_tag = a_tags[1]
                link = link_tag['href']
                new_title = link_tag.get_text()
                new_title = new_title.strip()
                ratio = string_similarity(new_title, self.film_title)
                if ratio > 0.85:
                    checkpoint = True        
                    break
            except:
                sys.exit('Something went wrong')        


        if not checkpoint:
            print("No such a film found in RottenTomatoes")
            return False
        else:
            page_response = requests.get(link, headers={"User-Agent": "Mozilla", "Accept-Language": "en-US,en;q=0.5"})
            parsed_html_film_page = BeautifulSoup(page_response.text, "html.parser")
            return parsed_html_film_page

    def get_score(self):

        parsed_html_film_page = self.__get_final_web(self.url)
        if parsed_html_film_page:
            span = str(parsed_html_film_page.find_all("script", id="score-details-json")[0].get_text())
            self.tomatometer_score = cutting_around_string(span, ['tomatometerScore":', ','])
            self.audience_score = cutting_around_string(span, ['"audienceScore":', ','])
        else:
            self.tomatometer_score = "No score"
            self.audience_score = "No score" 


class Imdb:
    

    def __init__(self, film_title, film_year):
        self.film_title = film_title
        self.film_year = film_year
        self.url = f"https://www.imdb.com/find/?q={self.film_title}&ref_=nv_sr_sm"

    def __get_final_web(self, url):

        self.title_data = init_request(self.film_title, url, "li.find-title-result")       
        checkpoint = False
        for title in self.title_data:
            try:
                year = title.select("div:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1) > label:nth-child(1)")[0].get_text()
                if self.film_year not in year:
                    continue
                new_title = title.select("div:nth-child(2) > div:nth-child(1) > a:nth-child(1)")[0].get_text()
                link = "https://www.imdb.com" + title.select("div:nth-child(2) > div:nth-child(1) > a:nth-child(1)")[0].get('href')
                ratio = string_similarity(new_title, self.film_title)
                if ratio > 0.85:
                    checkpoint = True        
                    break
        
            except Error:
                sys.exit('Something went wrong')

        if not checkpoint:
            print("No such a film found in IMDb")
            return False

        else:
            page_response = requests.get(link, headers={"User-Agent": "Mozilla", "Accept-Language": "en-US,en;q=0.5"})
            parsed_html_film_page = BeautifulSoup(page_response.text, "html.parser")  
            return parsed_html_film_page

    def get_score(self):
        parsed_html_film_page = self.__get_final_web(self.url)     
        if parsed_html_film_page:
            self.score = parsed_html_film_page.select( ".sc-5be2ae66-3 > div:nth-child(1) > div:nth-child(1) > a:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)")[0].get_text()
        else:
            self.score = "No score"

        
        
if __name__ == "__main__":
    pass
    


    
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 2020 

@author: Stefan Mager and Christopher Henkel
"""

### Feel free to use the code for the automated download of journal article information.
# However, keep in mind that you might be blocked by the ais website if you 
# execute the code too often within a short amount of time. ###

import requests
from bs4 import BeautifulSoup
import csv

def start_scraping():
    scrape_articles(url='https://aisel.aisnet.org/jais', outlet="jais")
    scrape_articles(url='https://aisel.aisnet.org/misq', outlet="misq")
    
def scrape_articles(url, outlet):
    
    r=requests.get(url)
    file_name = outlet + "_request_download.txt"
    file=open(file_name,"w", encoding="utf-8")
    file.write(r.text)
    file.close()
    
    file = open(file_name, "r", encoding="utf-8")
    html = file.read()
    file.close()

    soup = BeautifulSoup(html, features='html.parser')

    all_articles = []

    issue_items = soup.findAll(class_="doc")
    for i in issue_items:

        current_article_authors = []

        h5_title = i.findAll("a")[1]
        current_article_titles = h5_title.attrs["title"]

        all_authors = i.find(class_="auth")
        current_article_authors= all_authors.text

        h5_link = i.findAll("a")[1]
        # TODO: Potential Issue if you want to scrape other sites apart from informs
        current_article_links = h5_link.attrs["href"]
        current_article_abstracts = scrape_abstract(current_article_links)

        all_articles.append({
            "authors": current_article_authors,
            "title": current_article_titles,
            "links": current_article_links,
            "abstract": current_article_abstracts,
            "outlet": outlet
        })        
        
    keys = all_articles[0].keys()
    outlet_csv_file_name = outlet + '.csv'
    with open(outlet_csv_file_name, 'w', encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(all_articles)


def scrape_abstract(article_url):
    print(article_url)
    r = requests.get(article_url)

    soup = BeautifulSoup(r.text, features='html.parser')

    abstract_text = soup.findAll(id="abstract")
    for j in abstract_text:
        
        abstract = j.find("p")
        if abstract is not None:
            return abstract.text
        else:
            return ""


if __name__ == '__main__':
    start_scraping()

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 2020 

@author: Stefan Mager and Christopher Henkel
"""

### Feel free to use the code for the automated download of journal article information.
# However, keep in mind that you might be blocked by the wiley website if you 
# execute the code too often within a short amount of time. ###

import requests
from bs4 import BeautifulSoup
import csv

def start_scraping():
    #scrape_articles(url='https://onlinelibrary.wiley.com/toc/13652575/current', outlet="isj")
    scrape_articles(url='https://onlinelibrary.wiley.com/toc/10970266/current', outlet="smj")

def strip_html_element(element):
    return " ".join(element.text.split())

def scrape_articles(url, outlet):
    
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,'referer':'https://onlinelibrary.wiley.com/'}
    r=requests.get(url, headers=header)
    file_name = outlet + "_request_download.txt"
    file=open(file_name,"w", encoding="utf-8")
    file.write(r.text)
    file.close()
    
    file = open(file_name, "r", encoding="utf-8")
    html = file.read()
    file.close()

    soup = BeautifulSoup(html, features='html.parser')

    all_articles = []

    issue_items = soup.findAll(class_="issue-item")
    skip_first = True
    for i in issue_items:
        if skip_first:
            skip_first = False
            continue

        current_article_authors = []

        h5_title = i.find(class_="issue-item__title visitable")
        title_strip = strip_html_element(h5_title)
        current_article_titles = title_strip
        print(current_article_titles)

        all_authors = i.findAll(class_="rlist--inline loa comma loa-authors-trunc")
        for single_author in all_authors:
            author_strip = strip_html_element(single_author)
            current_article_authors.append(author_strip)
        print(current_article_authors)

        h5_link = i.find("a")
        # TODO: Potential Issue if you want to scrape other sites apart from informs
        current_article_links = "https://onlinelibrary.wiley.com" + h5_link.attrs["href"]
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
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,'referer':'https://onlinelibrary.wiley.com/'}
    r = requests.get(article_url, headers=header)

    soup = BeautifulSoup(r.text, features='html.parser')

    abstract = soup.find(class_="article-section__content en main")

    if abstract is not None:
        abstract_strip = strip_html_element(abstract)
        return abstract_strip
    else:
        return ""


if __name__ == '__main__':
    start_scraping()

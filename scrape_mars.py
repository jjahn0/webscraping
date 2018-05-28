
import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path)

def scrape_news():
    browser = init_browser()
    info = {}
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    info["headline"] = soup.find("div", class_="content_title").get_text()
    info["date"] = soup.find("div", class_="list_date").get_text()
    info["teaser"] = soup.find("div", class_="article_teaser_body").get_text()
    browser.quit()
    return info


def scrape_img():
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url = "https://www.jpl.nasa.gov"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    img_path = soup.find("a", class_="button fancybox")['data-fancybox-href']
    full_img_url = base_url + img_path
    browser.quit()
    return full_img_url



def scrape_weather():
    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    latest_weather = soup.find("div", class_="js-tweet-text-container").get_text().replace('\n','')
    browser.quit()
    return latest_weather


def scrape_facts():
    mars_info_dict = {}
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    mars_info = tables[0]
    categories = list(mars_info[0])
    facts = list(mars_info[1])
    for i in range(len(categories)):
        categories[i] =categories[i].replace(":","").replace(" ","_")
    mars_info_dict = dict(zip(categories,facts))
    return mars_info_dict


## scrape href of mars hemisphere webpage, list them, 
## and return list 'url_list'

def scrape_url_list():
    url_list = []
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url = "https://astrogeology.usgs.gov"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("div", class_="item"):
        for a in item.find_all("a", href=True):
            url_list.append(base_url + a['href'])
    browser.quit()
    url_list = list(set(url_list))
    return url_list


## Follow the scraped url list and scrape again for img href and title
## Load into dictionary and return dict 'href_list'
## this method depends on correct url list being produced,
## aka scrap_url_list method

def scrape_href_list():
    href_list = []
    dict_item = {}
    
    url_list = scrape_url_list()
    browser = init_browser()
    for url in url_list:
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("h2", class_="title").get_text()
        for div in soup.find_all('div', class_="downloads"):
            dict_item = {
                "title": title,
                "href": div.find('a')['href']
            }
        href_list.append(dict_item)
    browser.quit()
    return href_list

def scrape():
    info = {
        "news" : scrape_news(),
        "img_url" : scrape_img(),
        "weather" : scrape_weather(),
        "facts" : scrape_facts(),
        "img_list" : scrape_href_list()
    }
    return info
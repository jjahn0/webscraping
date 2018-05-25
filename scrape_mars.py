import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path)


def scrape():
    browser = init_browser()
    info = {}
    # all_info = []

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    info["headline"] = soup.find("div", class_="content_title").get_text()
    info["date"] = soup.find("div", class_="list_date").get_text()
    info["teaser"] = soup.find("div", class_="article_teaser_body").get_text()

    return info

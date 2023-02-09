#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 6 12:12:47 2023
@author: joshrainbow

"""
################################# Imports ################################
# Imports for scraping
import csv
import requests
from bs4 import BeautifulSoup
import time


# setting URL
url = 'https://www.linkedin.com/jobs/search?keywords=Data+Science&location=Canada&geoId=&trk=public_jobs_jobs-search-bar_search-submit&original_referer=https://www.linkedin.com/jobs/search?keywords=data%20science&location=Calgary%2C%20Alberta%2C%20Canada&geoId=102199904&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&original_refer'

response = requests.get(url)
print(response)

'''
before we can start extracting any data from the page, we need to parse the raw HTML data
making it easier to navigate using CSS selectors
'''

# create a BS4 object by passing response.content as the first argument
soup = BeautifulSoup(response.content, 'html.parser')

jobTitle = soup.find('h3', class_='base-search-card__title').text
print(jobTitle)

'''
now we need to get around the problem of moving through the pages
'''
def linkedinScraper(webpage, pageNumber):
    nextPage = webpage + str(pageNumber)
    print(str(pageNumber))
    response = requests.get(nextPage)
    soup = BeautifulSoup(response.content, 'html.parser')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thurs Feb 9 12:12:47 2023
@author: joshrainbow

"""
################################# Imports ################################
# Imports for scraping
import csv
import requests
from bs4 import BeautifulSoup
import time

'''
# setting URL
url = 'https://www.linkedin.com/jobs/search?keywords=Data+Science&location=Canada&geoId=&trk=public_jobs_jobs-search-bar_search-submit&original_referer=https://www.linkedin.com/jobs/search?keywords=data%20science&location=Calgary%2C%20Alberta%2C%20Canada&geoId=102199904&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

response = requests.get(url)
print(response)


before we can start extracting any data from the page, we need to parse the raw HTML data
making it easier to navigate using CSS selectors


# create a BS4 object by passing response.content as the first argument
soup = BeautifulSoup(response.content, 'html.parser')

jobTitle = soup.find('h3', class_='base-search-card__title').text
company = soup.find('h4', class_='base-search-card__subtitle-link').text
#print(jobTitle)



now we need to get around the problem of moving through the pages
'''

file = open('linkedinJobs.csv', 'a')
writer = csv.writer(file)
writer.writerow(['Title', 'Company', 'Location', 'Link'])

def linkedinScraper(webpage, pageNumber):
    nextPage = webpage + str(pageNumber)
    print(str(pageNumber))
    response = requests.get(nextPage)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(response)
    
    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    
    for job in jobs:
        jobTitle = job.find('h3', class_='base-search-card__title').text.strip()
        jobCompany = job.find('h4', class_='base-search-card__subtitle').text.strip()
        jobLocation = job.find('span', class_='job-search-card__location').text.strip()
        jobLink = job.find('a', class_='base-card__full-link')['href']
    
    writer.writerow([jobTitle.encode('utf-8'), 
                     jobCompany.encode('utf-8'), 
                     jobLocation.encode('utf-8'), 
                     jobLink.encode('utf-8')])
    
    print("Data written to CSV")
    
    if pageNumber < 100:
        pageNumber += 25
        linkedinScraper(webpage, pageNumber)
    else:
        file.close()
        print("Scraping complete")
        
url = 'https://ca.linkedin.com/jobs/search?keywords=Data+Science&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
start = 0
linkedinScraper(url, start)


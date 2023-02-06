#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 6 12:12:47 2023
@author: joshrainbow

"""
################################# Imports ################################
# Imports for scraping
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# Date and time related imports
import time
from datetime import datetime

# Libraries needed for moving files around
from pathlib import Path
import glob
import os
import zipfile

# Assign the chrome driver to a variable
driver = webdriver.Chrome("/Users/mutumbo/Desktop/BTG/chromeDriver/chromedriver")

####################### Opening the Website #########################
# Go to the webpage of interest
driver.get("https://www.linkedin.com/jobs/")
print(driver.title)

# Wait for the page to load
page_load_wait_time = 5 # in seconds
# Wait up to 120s before assuming something is wrong with the download
max_wait_time_for_download = 120 
time.sleep(page_load_wait_time) # wait a certain number of seconds


####################### Utilizing the Search bars #########################

searchKeyword = driver.find_element(By.ID,"jobs-search-box-keyword-id-ember2827")
searchLocation = driver.find_element(By.ID,"jobs-search-box-location-id-ember2827")

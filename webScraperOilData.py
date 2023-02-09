#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 3 16:12:47 2023
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
driver.get("https://www.petrinex.ca/PD/Pages/APD.aspx")
print(driver.title)

# Wait for the page to load
page_load_wait_time = 5 # in seconds
# Wait up to 120s before assuming something is wrong with the download
max_wait_time_for_download = 120 
time.sleep(page_load_wait_time) # wait a certain number of seconds

## Important Folders
# This is the folder containing our monthly petrinex data folders
data_folder = "/Users/mutumbo/Desktop/BTG/Data"
# Referencing the downloads folder
downloads_path = "/Users/mutumbo/Desktop/BTG/Downloads"

######################## Useful Functions #########################
# Function that takes in month, year and number of months 
# ago to returns a dash separated string of that year and month
def previous_month_label(month, year, months_ago):
    if month <= months_ago:
        prev_m = 12 - months_ago % month
        prev_y = year - months_ago // month
    else:
        prev_m = month - months_ago
        prev_y = year
    if prev_m < 10:
        prev_m = "0" + str(prev_m)
    return str(prev_y) + "-" + str(prev_m)

# This function takes in the paths of the checkbox for specifying csv format and the download button
# It clicks both, which initiates the download
def start_csv_zip_download(format_checkbox_element, download_button_element):
    format_checkbox_element.click()
    download_button_element.click()

# This functions takes in the path of the downloads folder
# and a maximum number of seconds to wait for the download.
# It checks the folder to make sure nothing is being downloaded 
# from chrome and keeps looping and checking until the download 
# is finished or you pass the maximum wait time.
def download_wait(path_to_downloads, max_wait_time):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < max_wait_time:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    print("The download took ", str(seconds) + " seconds.")
    
# This function takes in the path of a zip file as a string,
# along with a path for it to be unzipped as, then
# it deletes the zip file
def unzip(zip_file_path, where_to_unzip):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(where_to_unzip)
    os.remove(zip_file_path)

# This is the main function
def perform_download_process(downloads_path, max_wait_time_for_download, data_folder, month, year):
    # Path to checkbox for csv format
    format_checkbox_element = driver.find_element("xpath", "//*[@id='FileFormat']")
    # Path to download button
    download_button_element = driver.find_element("xpath", "/html/body/div[1]/form/div[10]/div[2]/button")
    
    # Pressing the download button
    start_csv_zip_download(format_checkbox_element, download_button_element)
    
    # Wait 3 seconds to give google enough time to start the download
    time.sleep(7)
    ###################### Waiting for the Download #######################
    download_wait(downloads_path, max_wait_time_for_download)
    
    ############## Moving the downloaded files to the correct folder ############
    # A list of all files in the downloads folder
    list_of_downloads = glob.glob(downloads_path + "/*")
    # The latest download (should be the petrinex files)
    latest_download = max(list_of_downloads, key=os.path.getctime)

    ####################### Unzipping the Data ###############################
    petrinex_zip_path = data_folder + "/Petrinex " + previous_month_label(month, year, 0) + ".zip"
    unzipped_petrinex_folder = petrinex_zip_path[:-4]
    # Sending the download to our data folder
    Path(latest_download).rename(petrinex_zip_path)

    # Unzip the folder
    unzip(petrinex_zip_path, unzipped_petrinex_folder)
    # Unzip each individual csv file
    list_of_zipped_csv = glob.glob(unzipped_petrinex_folder + "/*")
    for zip_file in list_of_zipped_csv:
        unzip(zip_file, unzipped_petrinex_folder)



###################### Checking the Boxes ###########################
# The downloadable files section checkboxes
driver.find_element("xpath", "//*[@id='InfrastructureFiles_0__IsChecked']").click()
driver.find_element("xpath", "//*[@id='InfrastructureFiles_1__IsChecked']").click()
driver.find_element("xpath", "//*[@id='InfrastructureFiles_2__IsChecked']").click()
driver.find_element("xpath", "//*[@id='InfrastructureFiles_3__IsChecked']").click()
driver.find_element("xpath", "//*[@id='InfrastructureFiles_4__IsChecked']").click()
driver.find_element("xpath", "//*[@id='InfrastructureFiles_5__IsChecked']").click()
driver.find_element("xpath", "//*[@id='InfrastructureFiles_6__IsChecked']").click()

perform_download_process(downloads_path, max_wait_time_for_download, data_folder, curr_month, curr_year)

    
#################### Conventional Volumetric Data #####################
table_for_latest_year = driver.find_element("xpath", '/html/body/div[1]/form/div[9]/table/tbody/tr/td[1]/table/tbody')
# // means check whole html page, don't use it here because we just want this section
latest_volume_entry = table_for_latest_year.find_elements_by_xpath("tr")[-1]

# Confirming month and year for latest update
vol_data_latest_year_updated = int(driver.find_element("xpath", '/html/body/div[1]/form/div[9]/table/thead/tr/th[1]').text)
vol_data_latest_month_updated = int(latest_volume_entry.text.split(" ")[0])
latest_volume_entry.find_element("xpath", 'td/input').click()


perform_download_process(downloads_path, max_wait_time_for_download, data_folder, vol_data_latest_month_updated, vol_data_latest_year_updated)



################# Closing the Browser ##################

# Closes the current tab
driver.close()
# Closes the current window
driver.quit()
print('done')

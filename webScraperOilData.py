"""
Created on Fri Feb 3 16:12:47 2023

@author: joshrainbow

"""

################################# Imports ################################
# Imports for scraping
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# Date and time related imports
import time
from datetime import datetime

# Libraries needed for moving files around
from pathlib import Path
import glob
import os
import zipfile

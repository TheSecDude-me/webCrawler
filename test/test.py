from seleniumwire import webdriver 
from seleniumwire.utils import decode as sw_decode
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import os
import shutil
import pickle
import time
import json


url = "file:///C:/Users/alime/Projects/webcrawler/test/test.html"

driver = webdriver.Firefox()
driver.get(url=url)
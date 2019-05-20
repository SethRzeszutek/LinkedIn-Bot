import os, random, sys, time, re, csv, datetime
from configure import *
from selenium import webdriver
if BROWSER.upper() == "CHROME":
	from selenium.webdriver.chrome.options import Options
if BROWSER.upper() == "FIREFOX":
	from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from random import shuffle
import urllib.parse as urlparse
from os.path import join, dirname

SESSION_CONNECTION_COUNT = 0
TEMP_NAME=""
TEMP_JOB=""
TEMP_JOBMATCH=""
TEMP_LOCATION=""
TEMP_LOCATIONMATCH=""
TEMP_PROFILE=[]
CONNECTED = False

CSV_DATA = [["Name","Title", "Title Match", "Location","Location Match", "Current Company","Connected"]]


###CONFIGURE ALL SETTINGS IN configure.py###
EMAIL = CONFIGURED_EMAIL
PASSWORD = CONFIGURED_PASSWORD
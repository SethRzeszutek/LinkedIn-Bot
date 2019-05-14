#!/usr/bin/python
# -*- coding: utf-8 -*-
# Updated Author: Seth Rzeszutek
# Previous Authors: Matt Flood and helloitsim

import os, random, sys, time, re
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
#from dotenv import load_dotenv

SESSION_CONNECTION_COUNT = 0
TEMP_NAME=""
TEMP_JOB=""
TEMP_LOCATION=""

#dotenv_path = join(dirname(__file__), '.env')
#load_dotenv(dotenv_path)


###CONFIGURE ALL SETTINGS IN configure.py###
EMAIL = os.getenv("USERNAME",CONFIGURED_EMAIL)
PASSWORD = os.getenv("PASSWORD",CONFIGURED_PASSWORD)


def Launch():
	"""
	Launch the LinkedIn bot.
	"""

	# Check if the file 'visitedUsers.txt' exists, otherwise create it
	if os.path.isfile('visitedUsers.txt') == False:
		visitedUsersFile = open('visitedUsers.txt', 'wb')
		visitedUsersFile.close()

	StartBrowser()

def StartBrowser():
	"""
	Launch browser based on the user's selected choice.
	"""
	if BROWSER.upper() == "CHROME":
		if PRINT_ACTIONS:
			print('\n-> Launching Chrome')
		options = Options()
		#if HEADLESS:
		#	options.headless = True
		
		browser = webdriver.Chrome(options=options)
	elif BROWSER.upper() == "FIREFOX":
		if PRINT_ACTIONS:
			print('\n-> Launching Firefox')
		options = Options()
		if HEADLESS:
			if PRINT_DETAIL:
				print("* Headless Mode")
			options.headless = True
		browser = webdriver.Firefox(options=options)
	else:
		print("!!! Browser type not recognized, please check your configure.py - BROWSER="+BROWSER)

	# Sign in
	browser.get('https://linkedin.com/uas/login')
	emailElement = browser.find_element_by_id('username')
	emailElement.send_keys(EMAIL)
	passElement = browser.find_element_by_id('password')
	passElement.send_keys(PASSWORD)
	passElement.submit()

	if PRINT_ACTIONS:
		print('-> Signing in...')
	time.sleep(3)

	soup = BeautifulSoup(browser.page_source, PARSER)
	if soup.find('div', {'class':'alert error'}):
		print('!!! Error! Please verify your username and password.')
		browser.quit()
	elif browser.title == '403: Forbidden':
		print('!!! LinkedIn is momentarily unavailable. Please wait a moment, then try again.')
		browser.quit()
	else:
		print('!!! Success!\n')
		LinkedInBot(browser)


def LinkedInBot(browser):
	"""
	Run the LinkedIn Bot.
	browser: the selenium driver to run the bot with.
	"""

	T = 0
	V = 0
	profilesQueued = []
	error403Count = 0
	timer = time.time()

	global TEMP_NAME
	global TEMP_JOB
	global TEMP_LOCATION

	if SCREENSHOTS:
		if PRINT_ACTIONS:
			print("-> Creating Screenshot Folder")
		try:
			os.makedirs("Screenshots")
			if PRINT_ACTIONS:
				print("* Created Screenshot Folder")
		except FileExistsError:
			if PRINT_ACTIONS:
				print("* Screenshot Folder already exists!")
			pass

	if PRINT_ACTIONS:
		print('-> Scraping User URLs on Network tab.\n')

	# Infinite loop
	while True:

		# Generate random IDs
		while True:

			NavigateToMyNetworkPage(browser)
			T += 1
			if GetNewProfileURLS(BeautifulSoup(browser.page_source, PARSER), profilesQueued):
				break
			else:
				print('|',
				time.sleep(random.uniform(5, 7)))
		soup = BeautifulSoup(browser.page_source, PARSER)
		profilesQueued = list(set(GetNewProfileURLS(soup, profilesQueued)))

		V += 1
		if PRINT_ACTIONS:
			print('\n\n* Finished gathering User URLs.\n')
			print("--> Starting Process")

		print(browser.title.replace(' | LinkedIn', ''), ' visited. T:', T, '| V:', V, '| Q:', len(profilesQueued))

		while profilesQueued:
			if (SESSION_CONNECTION_COUNT>=CONNECTION_LIMIT):
				print("---Max connections reached stopping program---")
				exit()
			shuffle(profilesQueued)
			profileID = profilesQueued.pop()
			browser.get('https://www.linkedin.com'+profileID)
			locationMatches = LocationCheck(browser)
			regex = r'\(.*?\)'
			TEMP_NAME = re.sub(regex, '', browser.title.replace(' | LinkedIn', ''))
			TEMP_JOB = ReturnJobMatch(browser)
			TEMP_LOCATION = ReturnLocationMatch(browser)
			# Connect with users if the flag is turned on and matches your criteria
			if CONNECT_WITH_USERS and locationMatches:
				if LIMIT_CONNECTION:
					if (SESSION_CONNECTION_COUNT<CONNECTION_LIMIT):
						if not RANDOMIZE_CONNECTING_WITH_USERS:
							ConnectWithUser(browser)
						elif random.choice([True, False]):
							ConnectWithUser(browser)
				elif not LIMIT_CONNECTION:
					if not RANDOMIZE_CONNECTING_WITH_USERS:
						ConnectWithUser(browser)
					elif random.choice([True, False]):
						ConnectWithUser(browser)

			# Add the ID to the visitedUsersFile
			with open('visitedUsers.txt', 'a') as visitedUsersFile:
				visitedUsersFile.write((profileID)+'\r\n')
			visitedUsersFile.close()

			# Get new profiles ID
			time.sleep(10)
			soup = BeautifulSoup(browser.page_source, PARSER)
			profilesQueued.extend(GetNewProfileURLS(soup, profilesQueued))
			profilesQueued = list(set(profilesQueued))

			#browserTitle = (browser.title).encode('ascii', 'ignore').replace('  ',' ')
			browserTitle = (browser.title).replace('  ',' ')

			# 403 error
			if browserTitle == '403: Forbidden':
				error403Count += 1
				print('\n!!! LinkedIn is momentarily unavailable - Paused for', (error403Count), 'hour(s)\n')
				time.sleep(3600*error403Count+(random.randrange(0, 10))*60)
				timer = time.time() # Reset the timer

			# User out of network
			elif browserTitle == 'Profile | LinkedIn':
				T += 1
				error403Count = 0
				print('!!! User not in your network. T:', T, '| V:', V, '| Q:', len(profilesQueued))

			# User in network
			else:
				T += 1
				V += 1
				error403Count = 0
				if DELIMIT_BY_LOCATION and VIEW_SPECIFIC_USERS:
					#print(browserTitle.replace(' | LinkedIn', ''), 'visited. T:', T, '| V:', V, '| Q:', len(profilesQueued), '| Location Match:', ReturnLocationMatch(browser), '| Job Match:', ReturnJobMatch(browser))
					print(TEMP_NAME, 'visited. T:', T, '| V:', V, '| Q:', len(profilesQueued), '| Location Match:', TEMP_LOCATION, '| Job Match:', TEMP_JOB)
				elif DELIMIT_BY_LOCATION:
					print(TEMP_NAME, 'visited. T:', T, '| V:', V, '| Q:', len(profilesQueued), '| Location Match:', TEMP_LOCATION)
				elif VIEW_SPECIFIC_USERS:
					print(TEMP_NAME, 'visited. T:', T, '| V:', V, '| Q:', len(profilesQueued), '| Job Match:', TEMP_JOB)
				else:
					print(TEMP_NAME, 'visited. T:', T, '| V:', V, '| Q:', len(profilesQueued))

			# Pause
			if (T%1000==0) or time.time()-timer > 3600:
				print('\n!!! Paused for 1 hour\n')
				time.sleep(3600+(random.randrange(0, 10))*60)
				timer = time.time() # Reset the timer
			else:
				time.sleep(random.uniform(5, 7)) # Otherwise, sleep to make sure everything loads

		print('\n!!! No more profiles to visit. Everything restarts with the network page...\n')


def NavigateToMyNetworkPage(browser):
	"""
	Navigate to the my network page and scroll to the bottom and let the lazy loading
	go to be able to grab more potential users in your network. It is recommended to
	increase the NUM_LAZY_LOAD_ON_MY_NETWORK_PAGE value if you are using the variable
	SPECIFIC_USERS_TO_VIEW.
	browser: the selenium browser used to interact with the page.
	"""

	browser.get('https://www.linkedin.com/mynetwork/')
	for counter in range(1,NUM_LAZY_LOAD_ON_MY_NETWORK_PAGE):
		ScrollToBottomAndWaitForLoad(browser)


def ConnectWithUser(browser):
	"""
	Connect with the user viewing if their job title is found in your list of roles
	you want to connect with.
	browse: the selenium browser used to interact with the page.
	"""

	soup = BeautifulSoup(browser.page_source, PARSER)
	global SESSION_CONNECTION_COUNT
	jobTitleMatches = False
	# I know not that efficient of a loop but BeautifulSoup and Selenium are
	# giving me a hard time finding the specifc h2 element that contain's user's job title
	for selection in soup.findAll("h2", {"class": "pv-top-card-section__headline"}):
		for job in JOBS_TO_CONNECT_WITH:
			if job in selection.getText():
				jobTitleMatches = True
				break
	locationResult = LocationCheck(browser)
	if jobTitleMatches and locationResult:
		try:
			if SCREENSHOTS:
				filename = TEMP_NAME+"-connected.png"
				if PRINT_ACTIONS:
					print("* Saved "+filename)
				browser.save_screenshot(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Screenshots', filename))
			browser.find_element_by_xpath('//button[@class="pv-s-profile-actions pv-s-profile-actions--connect artdeco-button artdeco-button--3 mr2 mt2"]').click()
			time.sleep(3)
			browser.find_element_by_xpath('//button[@class="artdeco-button artdeco-button--3 ml1"]').click()
			SESSION_CONNECTION_COUNT += 1
			if PRINT_ACTIONS:
				print('* Sending the user an invitation to connect. Count = '+ str(SESSION_CONNECTION_COUNT))
		except:
			print("!!! Error connecting to " + TEMP_NAME)
			if PRINT_DETAIL:
				print(">>>> Name: "+TEMP_NAME+" Title: "+TEMP_JOB+" Location: "+TEMP_LOCATION)
				print(">>>> Location Match: "+locationResult+" Title Match: "+ jobTitleMatches)
			pass


def GetNewProfileURLS(soup, profilesQueued):
	"""
	Get new profile urls to add to the navigate queue.
	soup: beautiful soup instance of page's source code.
	profileQueued: current list of profile queues.
	"""
	# Open, load and close
	with open('visitedUsers.txt', 'r') as visitedUsersFile:
		visitedUsers = [line.strip() for line in visitedUsersFile]
	visitedUsersFile.close()

	profileURLS = []
	#I would like to add location based veiwing but cannot gain access based on that 

	profileURLS.extend(FindProfileURLsInNetworkPage(soup, profilesQueued, profileURLS, visitedUsers))

	profileURLS = list(set(profileURLS))

	return profileURLS


def FindProfileURLsInNetworkPage(soup, profilesQueued, profileURLS, visitedUsers):
	"""
	Get new profile urls to add to the navigate queue from the my network page.
	soup: beautiful soup instance of page's source code.
	profileQueued: current list of profile queues.
	profileURLS: profile urls already found this scrape.
	visitedUsers: user's profiles that we have already viewed.
	"""

	newProfileURLS = []

	try:
		for a in soup.find_all('a', class_='discover-person-card__link'):
			if ValidateURL(a['href'], profileURLS, profilesQueued, visitedUsers):
				if VIEW_SPECIFIC_USERS:
					for span in a.find_all('span', class_='discover-person-card__occupation'):
						for occupation in SPECIFIC_USERS_TO_VIEW:
							if VERBOSE:
								print(">>>> "+occupation)
							if occupation.lower() in span.text.lower(): #replicate this elsewhere
								if VERBOSE:
									print(">>>> "+a['href'])
								newProfileURLS.append(a['href'])
								break

				else:
					if VERBOSE:
						print(">>>> "+a['href'])
					newProfileURLS.append(a['href'])
	except:
		pass

	return newProfileURLS

def ValidateURL(url, profileURLS, profilesQueued, visitedUsers):
	"""
	Validate the url passed meets requirement to be navigated to.
	profileURLS: list of urls already added within the GetNewProfileURLS method to be returned.
		Want to make sure we are not adding duplicates.
	profilesQueued: list of urls already added and being looped. Want to make sure we are not
		adding duplicates.
	visitedUsers: users already visited. Don't want to be creepy and visit them multiple days in a row.
	"""

	return url not in profileURLS and url not in profilesQueued and "/in/" in url and "connections" not in url and "skills" not in url and url not in visitedUsers

def ScrollToBottomAndWaitForLoad(browser):
	"""
	Scroll to the bottom of the page and wait for the page to perform it's lazy loading.
	browser: selenium webdriver used to interact with the browser.
	"""

	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(4)

def LocationCheck(browser):
	soup = BeautifulSoup(browser.page_source, PARSER)
	if(DELIMIT_BY_LOCATION):
		locations = soup.findAll("h3", {"class": "pv-top-card-section__location"})
		for p in locations:
			for l in LOCATIONS:
				if VERBOSE:
					print(">>>> Web Location: "+str(p)+" Settings Location: "+str(l))
				if l.lower() in p.text.lower():
					return True
				else:
					return False
	else:
		return False

def ReturnLocationMatch(browser):
	soup = BeautifulSoup(browser.page_source, PARSER)
	rtn = ""
	locations = soup.findAll("h3", {"class": "pv-top-card-section__location"})
	for p in locations:
		for l in LOCATIONS:
			if l.lower() in p.text.lower():
				rtn = l
				if VERBOSE:
					print(">>>> Location Match: "+rtn)
	if rtn != "":
		return rtn
	else:
		return("X")

def ReturnJobMatch(browser):
	soup = BeautifulSoup(browser.page_source, PARSER)
	rtn = ""
	for selection in soup.findAll("h2", {"class": "pv-top-card-section__headline"}):
		for job in JOBS_TO_CONNECT_WITH:
			if job.lower() in selection.text.lower():
				rtn = job
				if VERBOSE:
					print(">>>> Job Match: "+rtn)
	if rtn != "":
		return rtn
	else:
		return("X")


if __name__ == '__main__':
	Launch()

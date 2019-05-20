#!/usr/bin/python
# -*- coding: utf-8 -*-
# Updated Author: Seth Rzeszutek
# Previous Authors: Matt Flood and helloitsim

from imports import *
from viewconnect import *
from analysis import *

def Launch():
	"""
	Launch the LinkedIn bot.
	"""

	# Check if the file 'visitedUsers.txt' exists, otherwise create it
	if os.path.isfile('visitedUsers.txt') == False:
		visitedUsersFile = open('visitedUsers.txt', 'wb')
		visitedUsersFile.close()

	if MENU:
		Menu()
	else:
		StartBrowser()

def StartBrowser():
	"""
	Launch browser based on the user's selected choice.
	"""
	if PRINT_SETTINGS:
		PrintSettings()


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
		print('!!! Sign in success!\n')
		if MODE.upper() == "VIEW/CONNECT":
			LinkedInBot(browser)
		elif MODE.upper() == "ANALYSIS":
			StartConnectionAnalysis(browser)

def PrintSettings():
	print("\n\n------SETTINGS------")
	print("BROWSER:"+BROWSER)
	print("HEADLESS:"+str(HEADLESS))
	print("PRINT_ACTIONS:"+str(PRINT_ACTIONS))
	print("PRINT_SETTINGS:"+str(PRINT_SETTINGS))
	print("PARSER:"+PARSER)
	print("SCREEENSHOTS:"+str(SCREENSHOTS))
	print("VIEW_SPECIFIC_USERS:"+str(VIEW_SPECIFIC_USERS))
	print("SPECIFIC_USERS_TO_VIEW:"+', '.join(SPECIFIC_USERS_TO_VIEW))
	print("DELIMIT_BY_LOCATION:"+str(DELIMIT_BY_LOCATION))
	print("LOCATIONS:"+', '.join(LOCATIONS))
	print("NUM_LAZY_LOAD:"+str(NUM_LAZY_LOAD))
	print("CONNECT_WITH_USERS:"+str(CONNECT_WITH_USERS))
	print("LIMIT_CONNECTION:"+str(LIMIT_CONNECTION))
	print("CONNECTION_LIMIT:"+str(CONNECTION_LIMIT))
	print("RANDOMIZE_CONNECTING_WITH_USERS:"+str(RANDOMIZE_CONNECTING_WITH_USERS))
	print("JOBS_TO_CONNECT_WITH:"+', '.join(JOBS_TO_CONNECT_WITH))
	print("VERBOSE:"+str(VERBOSE))
	print("-----------------------------\n\n")

def Menu():
	global BROWSER
	global HEADLESS
	global PRINT_ACTIONS
	global PRINT_SETTINGS
	global SCREENSHOTS
	global VIEW_SPECIFIC_USERS
	global DELIMIT_BY_LOCATION
	global NUM_LAZY_LOAD
	global CONNECT_WITH_USERS
	global LIMIT_CONNECTION
	global CONNECTION_LIMIT
	global RANDOMIZE_CONNECTING_WITH_USERS
	global VERBOSE
	global MODE

	inMenu = True
	while inMenu:
		try:
			print("Welcome to LinkedIn-Bot!")
			print('[1] Settings')
			print('[2] Run')
			print('[3] Exit Program')
			response = int(input('> '))
			if response == 1:
				PrintSettings()
				print("\t--Note: These settings are not permanently saved. They are only for the currently running program.--")
				print("\tWhat setting would you like to change?")
				settingChoice = (input('\t> ')).upper()
				if settingChoice == 'BROWSER':
					print("\t\tBROWSER:"+BROWSER)
					print("\t\tWhat browser would you like to use? (Chrome or Firefox)?")
					BROWSER = (input('\t\t> ')).upper()	
				elif settingChoice == 'HEADLESS':
					print("\t\tHEADLESS:"+str(HEADLESS))
					print("\t\tUse headless mode? (True or False)?")
					HEADLESS = ((input('\t\t> ')).upper()) == "TRUE"
				elif settingChoice == 'PRINT_ACTIONS':
					print("\t\tPRINT_ACTIONS:"+str(PRINT_ACTIONS))
					print("\t\tPrint out the steps the bot takes? (True or False)?")
					PRINT_ACTIONS = ((input('\t\t> ')).upper()) == "TRUE"
				elif settingChoice == 'PRINT_SETTINGS':
					print("\t\tPRINT_SETTINGS:"+str(PRINT_SETTINGS))
					print("\t\tPrint out the settings? (True or False)?")
					PRINT_SETTINGS = ((input('\t\t> ')).upper()) == "TRUE"
				elif settingChoice == 'PARSER':
					print("\t\tPARSER:"+PARSER)
					print("\t\tRecommended to change this in configure.py.")
					#PRINT_ACTIONS = ((input('\t\t> ')).upper()) == "TRUE"
				elif settingChoice == 'SCREENSHOTS':
					print("\t\tSCREEENSHOTS:"+str(SCREENSHOTS))
					print("\t\tTake screenshots of accounts? (True or False)?")
					SCREENSHOTS = ((input('\t\t> ')).upper()) == "TRUE"
				elif settingChoice == 'VIEW_SPECIFIC_USERS':
					print("\t\tVIEW_SPECIFIC_USERS:"+str(VIEW_SPECIFIC_USERS))
					print("\t\tOnly view specific users, if false it will view everyone? (True or False)?")
					VIEW_SPECIFIC_USERS = ((input('\t\t> ')).upper()) == "TRUE"
				#elif settingChoice == 'SPECIFIC_USERS_TO_VIEW':
				elif settingChoice == 'DELIMIT_BY_LOCATION':
					print("\t\tDELIMIT_BY_LOCATION:"+str(DELIMIT_BY_LOCATION))
					print("\t\tConnect to people based on location? (True or False)?")
					DELIMIT_BY_LOCATION = ((input('\t\t> ')).upper()) == "TRUE"
				#elif settingChoice == 'LOCATIONS':
				elif settingChoice == 'NUM_LAZY_LOAD':
					print("\t\tNUM_LAZY_LOAD:"+str(NUM_LAZY_LOAD))
					print("\t\tHow many times it will scroll? Recommend to keep this around 10-15.")
					NUM_LAZY_LOAD = int(input('\t\t> '))
				elif settingChoice == 'CONNECT_WITH_USERS':
					print("\t\tCONNECT_WITH_USERS:"+str(CONNECT_WITH_USERS))
					print("\t\tConnect with users? (True or False)?")
					CONNECT_WITH_USERS = ((input('\t\t> ')).upper()) == "TRUE"
				elif settingChoice == 'LIMIT_CONNECTION':
					print("\t\tLIMIT_CONNECTION:"+str(LIMIT_CONNECTION))
					print("\t\tLimit number of users to connect with? (True or False)?")
					LIMIT_CONNECTION = ((input('\t\t> ')).upper()) == "TRUE"
				elif settingChoice == 'CONNECTION_LIMIT':
					print("\t\tCONNECTION_LIMIT:"+str(CONNECTION_LIMIT))
					print("\t\tAmount of connections?")
					CONNECTION_LIMIT = int(input('\t\t> '))
				elif settingChoice == 'RANDOMIZE_CONNECTING_WITH_USERS':
					print("\t\tRANDOMIZE_CONNECTING_WITH_USERS:"+str(RANDOMIZE_CONNECTING_WITH_USERS))
					print("\t\t50% chance to connect with each user? (True or False)?")
					LIMIT_CONNECTION = ((input('\t\t> ')).upper()) == "TRUE"
				#elif settingChoice == 'JOBS_TO_CONNECT_WITH':
				elif settingChoice == 'VERBOSE':
					print("VERBOSE:"+str(VERBOSE))
					print("\t\tPrint out debugging info? (True or False)?")
					VERBOSE = ((input('\t\t> ')).upper()) == "TRUE"
			elif response == 2:
				print("\tWhat would you like to run?")
				print('\t[4] View/Connect Mode')
				print('\t[5] Connection Report')
				print('\t[6] Back')
				secondResponse = int(input('\t> '))
				if secondResponse == 4:
					MODE = "VIEW/CONNECT"
					StartBrowser()
					inMenu = False
				elif secondResponse == 5:
					MODE = "ANALYSIS"
					StartBrowser()
					inMenu = False
				elif secondResponse == 6:
					pass
			elif response == 3:
				exit()

		except ValueError:
			print('Invalid choice.')
		else:
			if response not in [1,2,3]:
				print('Invalid choice.')
			#else:
				#break

if __name__ == '__main__':
	# try:
	# 	Launch()
	# except:
	# 	print("\nProgram Stopped Running")
	Launch()

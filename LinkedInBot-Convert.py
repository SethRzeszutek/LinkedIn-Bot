#!/usr/bin/python
# -*- coding: utf-8 -*-
# Updated Author: Seth Rzeszutek
# Previous Authors: Matt Flood and helloitsim

from imports import *

SESSION_CONNECTION_COUNT = 0
TEMP_NAME=""
TEMP_JOB=""
TEMP_TITLEMATCH=""
TEMP_LOCATION=""
TEMP_LOCATIONMATCH=""
TEMP_PROFILE=[]
CONNECTED = False
TIME = str(datetime.datetime.now().time())
CSV_DATA = [["Name","Title", "Title Match", "Location","Location Match", "Current Company","Connected"]]

#dotenv_path = join(dirname(__file__), '.env')
#load_dotenv(dotenv_path)


###CONFIGURE ALL SETTINGS IN configure.py###
EMAIL = CONFIGURED_EMAIL
PASSWORD = CONFIGURED_PASSWORD


def Launch():
	"""
	Launch the LinkedIn bot.
	"""

	if MODE.upper() == "VIEW":
		# Check if the file 'visitedUsers.txt' exists, otherwise create it
		if os.path.isfile('visitedUsers.txt') == False:
			visitedUsersFile = open('visitedUsers.txt', 'wb')
			visitedUsersFile.close()
	elif MODE.upper() == "JOB":
		# Check if the file 'visitedJobs.txt' exists, otherwise create it
		if os.path.isfile('visitedJobs.txt') == False:
			visitedUsersFile = open('visitedJobs.txt', 'wb')
			visitedUsersFile.close()

	StartBrowser()

def StartBrowser():
	"""
	Launch browser based on the user's selected choice.
	"""
	if PRINT_SETTINGS:
		print("\n\n------SETTINGS------")
		print("BROWSER:"+BROWSER)
		print("HEADLESS:"+str(HEADLESS))
		print("PRINT_ACTIONS:"+str(PRINT_ACTIONS))
		print("PRINT_SETTINGS:"+str(PRINT_SETTINGS))
		print("PARSER:"+PARSER)
		print("SCREEENSHOTS:"+str(SCREENSHOTS))
		print("VIEW_SPECIFIC_TITLES:"+str(VIEW_SPECIFIC_TITLES))
		print("TITLES_TO_VIEW_CONNECT_WITH:"+', '.join(TITLES_TO_VIEW_CONNECT_WITH))
		print("CONNECT_BY_LOCATION:"+str(CONNECT_BY_LOCATION))
		print("LOCATIONS_TO_CONNECT:"+', '.join(LOCATIONS_TO_CONNECT))
		print("LAZY_LOAD_NUM:"+str(LAZY_LOAD_NUM))
		print("CONNECT_WITH_USERS:"+str(CONNECT_WITH_USERS))
		print("LIMIT_CONNECTION:"+str(LIMIT_CONNECTION))
		print("CONNECTION_LIMIT:"+str(CONNECTION_LIMIT))
		print("RANDOMIZE_CONNECTING_WITH_USERS:"+str(RANDOMIZE_CONNECTING_WITH_USERS))
		print("TITLES_TO_VIEW_CONNECT_WITH:"+', '.join(TITLES_TO_VIEW_CONNECT_WITH))
		print("VERBOSE:"+str(VERBOSE))
		print("-----------------------------\n\n")


	if BROWSER.upper() == "CHROME":
		if PRINT_ACTIONS:
			print('\n-> Launching Chrome')
		options = Options()
		if HEADLESS:
			print("\t*Chrome will not run correctly in headless mode, starting normal mode.")
			#options.headless = True
		
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
		if MODE.upper() == "VIEW":
			LinkedInView(browser)
		elif MODE.upper() == "JOB":
			LinkedInJob(browser)


def LinkedInView(browser):
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
	global TEMP_PROFILE
	global CSV_DATA
	global CONNECTED

	if SCREENSHOTS:
		if PRINT_ACTIONS:
			print("-> Enabled Screenshots")
		try:
			os.makedirs("Screenshots")
			if PRINT_ACTIONS:
				print("\t* Created Screenshot Folder")
		except FileExistsError:
			pass
	header = ["Name","Title", "Title Match", "Location","Location Match", "Current Company", "Connected"]
	if SAVECSV:
		if PRINT_ACTIONS:
			print("-> Enabled Save as CSV")
		try:
			os.makedirs("CSV")
			if PRINT_ACTIONS:
				print("\t* Created CSV Folder")
		except FileExistsError:
			pass
		createCSV(header, TIME)

	if PRINT_ACTIONS:
		print('-> Scraping User URLs on Network tab.')

	# Infinite loop
	while True:
		# Generate random IDs
		while True:

			NavigateToPage(browser, 'https://www.linkedin.com/mynetwork/')
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
			print('\t* Finished gathering User URLs.\n')
			print("--> Starting Process\n")

		while profilesQueued:
			if (SESSION_CONNECTION_COUNT>=CONNECTION_LIMIT):
				print("---Max connections reached stopping program---")
				exit()
			CONNECTED = False
			shuffle(profilesQueued)
			profileID = profilesQueued.pop()
			browser.get('https://www.linkedin.com'+profileID)

			title_check = False
	
			title_check = TitleCheck(browser)
			location_check = LocationCheck(browser)

			if(CONNECT_BY_LOCATION):
				locationMatches = LocationCheck(browser)
				if VERBOSE:
					print("Location Matches: "+str(locationMatches))
			else:
				locationMatches = False
			regex = r'\(.*?\)'
			TEMP_NAME = re.sub(regex, '', browser.title.replace(' | LinkedIn', ''))
			TEMP_JOB = TitleMatch(browser)
			TEMP_LOCATION = LocationMatch(browser)
			#company = getCompany(browser)
			company ="n/a"
			title ="n/a"
			if " at " in TEMP_TITLEMATCH:
				company = TEMP_TITLEMATCH.split(" at ",1)[1]
			elif " for " in TEMP_TITLEMATCH:
				company = TEMP_TITLEMATCH.split(" for ",1)[1]
			if " at " in TEMP_TITLEMATCH:
				title = TEMP_TITLEMATCH.split(" at ",1)[0]
			elif " for " in TEMP_TITLEMATCH:
				title = TEMP_TITLEMATCH.split(" for ",1)[0]

			if POTENTIAL_COMPANY:
				if company == "n/a":
					company = getCompany(browser)
			
			if VIEW_MODE.upper() == "BOX":
				tvq = str(T)+":"+str(V)+":"+str(len(profilesQueued))
				print("┌───────────────────────────────────┐")
				print("│● Name: %-26.26s │"%(TEMP_NAME))
				if CONNECT_BY_LOCATION and VIEW_SPECIFIC_TITLES:
					print("├───────────────────────────────────┼───────────────────────────────────┬───────────────────────────────────┐")
					print("│ Title Match: %-20.20s │ Location Match: %-17.17s │ T:V:Q %-28s│" %(TEMP_JOB, TEMP_LOCATION, tvq))
				elif CONNECT_BY_LOCATION:
					print("│ Title Match: %-20.20s │ Location Match: %-17.17s │ T:V:Q %-28s│" %("OFF", TEMP_LOCATION, tvq))
				elif VIEW_SPECIFIC_TITLES:
					print("│ Title Match: %-20.20s │ Location Match: %-17.17s │ T:V:Q %-28s│" %(TEMP_JOB, "OFF", tvq))
				else:
					print("│ Title Match: %-20.20s │ Location Match: %-17.17s │ T:V:Q %-28s│" %("OFF", "OFF", tvq))
				if EXTRA_USER_INFO:
					print("├───────────────────────────────────┼───────────────────────────────────┼───────────────────────────────────┤")
					print("│ Title: %-26.26s │ Location: %-23.23s │ Company %-26.26s│" %(title,TEMP_LOCATIONMATCH, company))
				print("└───────────────────────────────────┴───────────────────────────────────┴───────────────────────────────────┘")
			elif VIEW_MODE.upper() == "COMPRESSED":
				if CONNECT_BY_LOCATION and VIEW_SPECIFIC_TITLES:
					print("● Name: %-17.17s | T:V:Q %-3.3d:%-3.3d:%-3.3d" %(TEMP_NAME, T, V, len(profilesQueued)))
				elif CONNECT_BY_LOCATION:
					print("● Name: %-17.17s | T:V:Q %-3.3d:%-3.3d:%-3.3d" %(TEMP_NAME, T, V, len(profilesQueued)))
				elif VIEW_SPECIFIC_TITLES:
					print("● Name: %-17.17s | T:V:Q %-3.3d:%-3.3d:%-3.3d" %(TEMP_NAME, T, V, len(profilesQueued)))
				else:
					print("● Name: %-17.17s | T:V:Q %-3.3d:%-3.3d:%-3.3d" %(TEMP_NAME, T, V, len(profilesQueued)))
				if EXTRA_USER_INFO:
					print("↳       %17.17s | Title: %-21.21s | Location: %-19.19s | Company %-15.15s" %("",title,TEMP_LOCATIONMATCH, company))
			else:
				if CONNECT_BY_LOCATION and VIEW_SPECIFIC_TITLES:
					print("● Name: %-17.17s | Title Match: %-15.15s | Location Match: %-13.13s | T:V:Q %-3.3d:%-3.3d:%-3.3d" %(TEMP_NAME, TEMP_JOB, TEMP_LOCATION, T, V, len(profilesQueued)))
				elif CONNECT_BY_LOCATION:
					print("● Name: %-17.17s | Location Match: %-13.13s | T:V:Q %-3.3d:%-3.3d:%-3.3d" %(TEMP_NAME, TEMP_LOCATION, T, V, len(profilesQueued)))
				elif VIEW_SPECIFIC_TITLES:
					print("● Name: %-17.17s | Title Match: %-15.15s | T:V:Q %-3.3d:%-3.3d:%-3.3d" %(TEMP_NAME, TEMP_JOB, T, V, len(profilesQueued)))
				else:
					print("● Name: %-17.17s | T:V:Q %-3.3d:%-3.3d:%-3.3d" %(TEMP_NAME, T, V, len(profilesQueued)))
				if EXTRA_USER_INFO:
					print("↳       %17.17s | Title: %-21.21s | Location: %-19.19s | Company %-15.15s" %("",title,TEMP_LOCATIONMATCH, company))

			# Connect with users if the flag is turned on and matches your criteria
			# NOTE: FindProfileURLsInNetworkPage is already filtering by user's title, so before it is even added to the list it is filtered by title if the option is on
			if CONNECT_WITH_USERS and CONNECT_BY_LOCATION:
				if location_check:
					if LIMIT_CONNECTION and (SESSION_CONNECTION_COUNT<CONNECTION_LIMIT):
						if not RANDOMIZE_CONNECTING_WITH_USERS:
							ConnectWithUser(browser)
						elif random.choice([True, False]):
							ConnectWithUser(browser)
					elif not LIMIT_CONNECTION:
						if not RANDOMIZE_CONNECTING_WITH_USERS:
							ConnectWithUser(browser)
						elif random.choice([True, False]):
							ConnectWithUser(browser)
			elif CONNECT_WITH_USERS:
				if LIMIT_CONNECTION and (SESSION_CONNECTION_COUNT<CONNECTION_LIMIT):
					if not RANDOMIZE_CONNECTING_WITH_USERS:
						ConnectWithUser(browser)
					elif random.choice([True, False]):
						ConnectWithUser(browser)
				elif not LIMIT_CONNECTION:
					if not RANDOMIZE_CONNECTING_WITH_USERS:
						ConnectWithUser(browser)
					elif random.choice([True, False]):
						ConnectWithUser(browser)
			

			TEMP_PROFILE = [TEMP_NAME, TEMP_JOB, TEMP_TITLEMATCH, TEMP_LOCATION, TEMP_LOCATIONMATCH, company, CONNECTED]
			if SAVECSV:
				addToCSV(TEMP_PROFILE,TIME, 'CSV')
				if VERBOSE:
					print("-> Temp Profile List")
					print(TEMP_PROFILE)

			
			# Add the ID to the visitedUsersFile
			with open('visitedUsers.txt', 'a') as visitedUsersFile:
				visitedUsersFile.write((profileID)+'\r\n')
			visitedUsersFile.close()

			# Get new profiles ID
			time.sleep(10)
			soup = BeautifulSoup(browser.page_source, PARSER)
			profilesQueued.extend(GetNewProfileURLS(soup, profilesQueued))
			profilesQueued = list(set(profilesQueued))

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

			# Pause
			if (T%1000==0) or time.time()-timer > 3600:
				print('\n!!! Paused for 1 hour\n')
				time.sleep(3600+(random.randrange(0, 10))*60)
				timer = time.time() # Reset the timer
			else:
				time.sleep(random.uniform(5, 7)) # Otherwise, sleep to make sure everything loads
		print('\n!!! No more profiles to visit. Everything restarts with the network page...\n')
		if SAVECSV and VERBOSE:
			print("-> Data to be exported to CSV")
			print(CSV_DATA)


def NavigateToPage(browser, url):
	"""
	Navigate to the my network page and scroll to the bottom and let the lazy loading
	go to be able to grab more potential users in your network. It is recommended to
	increase the LAZY_LOAD_NUM value if you are using the variable
	TITLES_TO_VIEW_CONNECT_WITH.
	browser: the selenium browser used to interact with the page.
	"""

	browser.get(url)
	if MODE.upper() == "VIEW":
		for counter in range(1,VIEW_LAZY_LOAD_NUM):
			ScrollToBottomAndWaitForLoad(browser)
	elif MODE.upper() == "JOB":
		for counter in range(1,JOB_LAZY_LOAD_NUM):
			ScrollToBottomAndWaitForLoad(browser)


def ConnectWithUser(browser):
	"""
	Connect with the user viewing if their job title is found in your list of roles
	you want to connect with.
	browse: the selenium browser used to interact with the page.
	"""

	global SESSION_CONNECTION_COUNT
	global CONNECTED
	try:
		if SCREENSHOTS:
			filename = TEMP_NAME+"-connected.png"
			if PRINT_ACTIONS:
				print("\t* Saved "+filename)
			browser.save_screenshot(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Screenshots', filename))
		browser.find_element_by_xpath('//button[@class="pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view"]').click()
		time.sleep(3)
		browser.find_element_by_xpath('//button[@class="artdeco-button artdeco-button--3 ml1"]').click()
		CONNECTED = True
		SESSION_CONNECTION_COUNT += 1
		if PRINT_ACTIONS:
			print('\t* Sending the user an invitation to connect. Count = '+ str(SESSION_CONNECTION_COUNT))
	except:
		print("!!! Error connecting to " + TEMP_NAME)
		print(">>>> Name: "+TEMP_NAME+" Title: "+TEMP_JOB+" Location: "+TEMP_LOCATION)
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
				if VIEW_SPECIFIC_TITLES:
					for span in a.find_all('span', class_='discover-person-card__occupation'):
						for occupation in TITLES_TO_VIEW_CONNECT_WITH:
							if VERBOSE:
								print(">>>> "+occupation)
							if occupation.lower() in span.text.lower():
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

def ValidateURL(url, URLS, Queued, visited):
	"""
	Validate the url passed meets requirement to be navigated to.
	profileURLS: list of urls already added within the GetNewProfileURLS method to be returned.
		Want to make sure we are not adding duplicates.
	profilesQueued: list of urls already added and being looped. Want to make sure we are not
		adding duplicates.
	visitedUsers: users already visited. Don't want to be creepy and visit them multiple days in a row.
	"""
	if MODE.upper() == "VIEW":
		return url not in URLS and url not in Queued and "/in/" in url and "connections" not in url and "skills" not in url and url not in visited
	elif MODE.upper() == "JOB":
		return url not in URLS and url not in Queued and url not in visited

def ScrollToBottomAndWaitForLoad(browser):
	"""
	Scroll to the bottom of the page and wait for the page to perform it's lazy loading.
	browser: selenium webdriver used to interact with the browser.
	"""

	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(4)

def LocationCheck(browser):
	'''
	Checks if the location of the user matches your list of locations
	browser = selenium webdriver
	returns true or false
	'''
	soup = BeautifulSoup(browser.page_source, PARSER)
	
	ul = soup.find("ul", {"class": "pv-top-card-v3--list"})
	ul = ul.find_next("ul", {"class": "pv-top-card-v3--list"})
	li = ul.find_next("li")
	for l in LOCATIONS_TO_CONNECT:
		if VERBOSE:
			print(">>>> Web Location: "+str(li.text)+" Settings Location: "+str(l))
		if l.lower() in li.text.lower():
			return True
		else:
			return False

def TitleCheck(browser):
	'''
	Checks if the job/title of the user matches your list of job/titles
	browser = selenium webdriver
	returns true or false
	'''
	soup = BeautifulSoup(browser.page_source, PARSER)

	ul = soup.find("ul", {"class": "pv-top-card-v3--list"})
	li = ul.find_next("h2")
	for job in TITLES_TO_VIEW_CONNECT_WITH:
		if VERBOSE:
			print(">>>> Web Job/Title: "+str(li.text)+" Settings Job/Title: "+str(job))
		if job.lower() in li.text.lower():
			return True
		else:
			return False

def LocationMatch(browser):
	'''
	Gets the location that matches your settings and also sets TEMP_LOCATIONMATCH
	browser = selenium webdriver
	returns the locaiton as a string
	'''
	global TEMP_LOCATIONMATCH
	TEMP_LOCATIONMATCH = "X" #if this doesnt change it, it could have the previous connections data
	soup = BeautifulSoup(browser.page_source, PARSER)
	rtn = ""
	ul = soup.find("ul", {"class": "pv-top-card-v3--list"})
	ul = ul.find_next("ul", {"class": "pv-top-card-v3--list"})
	li = ul.find_next("li")
	for l in LOCATIONS_TO_CONNECT:
		if l.lower() in li.text.lower():
			TEMP_LOCATIONMATCH = str(" ".join((li.text.lower()).split()))
			location = str(l)
			rtn = location
			if VERBOSE:
				print(">>>> Location Match: "+rtn)
				print(">>>>"+location + " : " + TEMP_LOCATIONMATCH)
	if rtn != "":
		return rtn
	else:
		return("X")

def TitleMatch(browser):
	'''
	Gets the job that matches your settings and also sets TEMP_TITLEMATCH
	browser = selenium webdriver
	returns the job as a string
	'''

	global TEMP_TITLEMATCH
	TEMP_TITLEMATCH = "X" #if this doesnt change it, it could have the previous connections data
	soup = BeautifulSoup(browser.page_source, PARSER)
	rtn = ""
	ul = soup.find("ul", {"class": "pv-top-card-v3--list"})
	li = ul.find_next("h2")
	for job in TITLES_TO_VIEW_CONNECT_WITH:
		if job.lower() in li.text.lower():
			TEMP_TITLEMATCH = (" ".join((li.text.lower()).split()))
			jobtitle = str(job)
			rtn = jobtitle
			if VERBOSE:
				print(">>>> Job Match: "+rtn)
				print(">>>>"+jobtitle + " : " + TEMP_TITLEMATCH)
	if rtn != "":
		return rtn
	else:
		return("X")

def createCSV(data, time):
	'''
	Creates initial CSV file
	data is the list that will get added to the file(in this case its the headers)
	time is the time at creation of this file
	'''
	filename = 'Linked-In-'+time+'.csv'
	with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'CSV', filename), 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(data)
	csvFile.close()

def addToCSV(data, time, location):
	'''
	Appends to the CSV file that matches the name with that time
	data is the list that will get added to the file
	time is the time at creation of this file
	'''
	filename = 'Linked-In-'+time+'.csv'
	with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), location, filename), 'a') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(data)
	csvFile.close()

def getCompany(browser):
	'''
	Get first item in work experience on Linkedin
	browser = selenium webdriver
	Returns a single string that should be the job or nothing
	'''
	#A decent amount of false positives on this, more so than it makes me comfortable to actually push it. 
	#WIll probably revisit it but until then it wont be used.
	soup = BeautifulSoup(browser.page_source, PARSER)
	rtn = ""
	for tag in soup.findAll("span", {"class": "pv-entity__secondary-title"}):
		rtn = (tag.get_text())
		break
	
	if rtn != "":
		return rtn
	else:
		return("n/a")

''' JOB COLLECTION SECTION '''

def LinkedInJob(browser):
	"""
	Run the LinkedIn Bot.
	browser: the selenium driver to run the bot with.
	"""
	T = 0
	V = 0
	jobsQueued = []
	error403Count = 0
	timer = time.time()

	global TEMP_NAME
	global TEMP_JOB
	global TEMP_LOCATION
	global TEMP_PROFILE
	global CSV_DATA
	global CONNECTED

	header = ["Job","Company", "Location", "Keyword Match","Job Link"]
	try:
		os.makedirs("JOBS")
		if PRINT_ACTIONS:
			print("\t* Created JOBS Folder")
	except FileExistsError:
		pass
	createCSV(header, TIME)

	if PRINT_ACTIONS:
		print('-> Scraping Job URLs on Jobs tab.')

	# Infinite loop
	while True:
		# Generate random IDs
		while True:

			NavigateToPage(browser,'https://www.linkedin.com/jobs/')
			T += 1
			if GetJobURLS(BeautifulSoup(browser.page_source, PARSER), jobsQueued):
				break
			else:
				print('|',
				time.sleep(random.uniform(5, 7)))
		soup = BeautifulSoup(browser.page_source, PARSER)
		jobsQueued = list(set(GetJobURLS(soup, jobsQueued)))

		V += 1
		if PRINT_ACTIONS:
			print('\t* Finished gathering Job URLs.\n')
			print("--> Starting Process\n")

		while jobsQueued:
			add_job = False
			if (SESSION_CONNECTION_COUNT>=CONNECTION_LIMIT):
				print("---Max connections reached stopping program---")
				exit()
			CONNECTED = False
			shuffle(jobsQueued)
			jobID = jobsQueued.pop()
			url = 'https://www.linkedin.com'+jobID
			browser.get(url)

			job = (soup.find("h1", {"class": "jobs-top-card__job-title"})).text
			company = ((soup.find("h3", {"class": "jobs-top-card__company-info"})).find_next("span")).text
			location = (soup.find("a", {"class": "jobs-top-card__exact-location"})).text
			
			if VIEW_MODE.upper() == "BOX":
				tvq = str(T)+":"+str(V)+":"+str(len(jobsQueued))
				print("┌───────────────────────────────────┐")
				print("│● Job: %-27.27s │"%(job))
				print("├───────────────────────────────────┼───────────────────────────────────┬───────────────────────────────────┐")
				print("│ Company: %-24.24s │ Location: %-23.23s │ T:V:Q %-28s│" %(company, location, tvq))
				print("└───────────────────────────────────┴───────────────────────────────────┴───────────────────────────────────┘")
			else:
				print("● Job: %-17.17s | Company: %-15.15s | Location: %-13.13s | T:V:Q %-3.3d:%-3.3d:%-3.3d" %(job, company, location, T, V, len(jobsQueued)))

			keyword = ""
			# Connect with users if the flag is turned on and matches your criteria
			# NOTE: FindProfileURLsInNetworkPage is already filtering by user's title, so before it is even added to the list it is filtered by title if the option is on
			if FILTER_BY_KEYWORD:
				browser.find_element_by_xpath('//button[@class="artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--2 artdeco-button--tertiary ember-view"]').click()
				description = soup.find("div", {"class": "jobs-box"})
				for word in KEYWORDS:
					if word.lower() in description.lower():
						keyword = word
						add_job = True
			else:
				add_job = False
			temp_joblist = [job, company, location, keyword, url]
			addToCSV(temp_joblist,TIME, 'JOBS')
			if VERBOSE:
				print("-> Temp Job List")
				print(temp_joblist)

			
			# Add the ID to the visitedJobsFile
			with open('visitedJobs.txt', 'a') as visitedJobsFile:
				visitedJobsFile.write((jobID)+'\r\n')
			visitedJobsFile.close()

			# Get new profiles ID
			time.sleep(10)
			soup = BeautifulSoup(browser.page_source, PARSER)
			jobsQueued.extend(GetJobURLS(soup, jobsQueued))
			jobsQueued = list(set(jobsQueued))

			browserTitle = (browser.title).replace('  ',' ')

			# 403 error
			if browserTitle == '403: Forbidden':
				error403Count += 1
				print('\n!!! LinkedIn is momentarily unavailable - Paused for', (error403Count), 'hour(s)\n')
				time.sleep(3600*error403Count+(random.randrange(0, 10))*60)
				timer = time.time() # Reset the timer

			# User in network
			else:
				T += 1
				V += 1
				error403Count = 0

			# Pause
			if (T%1000==0) or time.time()-timer > 3600:
				print('\n!!! Paused for 1 hour\n')
				time.sleep(3600+(random.randrange(0, 10))*60)
				timer = time.time() # Reset the timer
			else:
				time.sleep(random.uniform(5, 7)) # Otherwise, sleep to make sure everything loads
		print('\n!!! No more jobs to visit. Everything restarts with the jobs page...\n')

def GetJobURLS(soup, jobsQueued):
	"""
	Get new profile urls to add to the navigate queue.
	soup: beautiful soup instance of page's source code.
	jobsQueued: current list of profile queues.
	"""
	# Open, load and close
	with open('visitedJobs.txt', 'r') as visitedJobsFile:
		visitedJobs = [line.strip() for line in visitedJobsFile]
	visitedJobsFile.close()

	jobURLS = []

	jobURLS.extend(FindJobURLs(soup, jobsQueued, jobURLS, visitedJobs))

	jobURLS = list(set(jobURLS))

	return jobURLS

def FindJobURLs(soup, jobsQueued, jobURLS, visitedJobs):
	"""
	Get new profile urls to add to the navigate queue from the my network page.
	soup: beautiful soup instance of page's source code.
	jobsQueued: current list of job queues.
	jobURLS: job urls already found this scrape.
	visitedJobs: jobs that we have already viewed.
	"""

	newJobURLS = []

	try:
		for li in soup.find_all('li', class_='job-card'):
			#print(li)
			a = li.find_next("a", {"data-control-name": "A_jobshome_job_link_click"})
			print(a.text)
			if ValidateURL(a['href'], jobURLS, jobsQueued, visitedJobs):
				#print("ValidateURL Pass")
				if JOB_LOCATION:
					for h5 in li.find('h5', class_='job-card__location'):
						print(h5.text)
						for location in JOB_LOCATIONS:
							if VERBOSE:
								print(">>>> "+location)
							if location.lower() in h5.text.lower():
								if VERBOSE:
									print(">>>> "+a['href'])
								newJobURLS.append(a['href'])
								break

				else:
					if VERBOSE:
						print(">>>> "+a['href'])
					newJobURLS.append(a['href'])
	except:
		pass

	return newJobURLS


if __name__ == '__main__':
	if DEBUGGING:
		Launch()
	else:
		try:
			Launch()
		except:
			print("\nProgram Stopped Running")


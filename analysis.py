from imports import *
from reusable import *
#from LinkedInBot import *

TIME = str(datetime.datetime.now().time())

def StartConnectionAnalysis(browser):

	if os.path.isfile('connections.txt') == False:
		visitedUsersFile = open('connections.txt', 'wb')
		visitedUsersFile.close()

	header = ["Name","Title", "Title Match", "Location","Location Match", "Current Company"]
	try:
		os.makedirs("Analysis")
		if PRINT_ACTIONS:
			print("\t* Created Analysis Folder")
	except FileExistsError:
		pass
	CreateCSV(header, TIME)
	Analysis(browser)

def Analysis(browser):
	"""
	Run the LinkedIn Analysis Bot.
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

	# if SCREENSHOTS:
	# 	if PRINT_ACTIONS:
	# 		print("-> Enabled Screenshots")
	# 	try:
	# 		os.makedirs("Screenshots")
	# 		if PRINT_ACTIONS:
	# 			print("\t* Created Screenshot Folder")
	# 	except FileExistsError:
	# 		pass
	# header = ["Name","Title", "Title Match", "Location","Location Match", "Current Company", "Connected"]
	# if SAVECSV:
	# 	if PRINT_ACTIONS:
	# 		print("-> Enabled Save as CSV")
	# 	try:
	# 		os.makedirs("CSV")
	# 		if PRINT_ACTIONS:
	# 			print("\t* Created CSV Folder")
	# 	except FileExistsError:
	# 		pass
	# 	CreateCSV(header, TIME)

	if PRINT_ACTIONS:
		print('-> Scraping User URLs on Network tab.')

	# Infinite loop
	while True:

		# Generate random IDs
		while True:

			NavigateToConnectionPage(browser)
			T += 1
			if GetConnectionProfileURLS(BeautifulSoup(browser.page_source, PARSER), profilesQueued):
				break
			else:
				print('|',
				time.sleep(random.uniform(5, 7)))
		soup = BeautifulSoup(browser.page_source, PARSER)
		profilesQueued = list(set(GetConnectionProfileURLS(soup, profilesQueued)))

		V += 1
		if PRINT_ACTIONS:
			print('\t* Finished gathering Connected User URLs.\n')
			print("--> Starting Process\n")

		while profilesQueued:
			shuffle(profilesQueued)
			profileID = profilesQueued.pop()
			browser.get('https://www.linkedin.com'+profileID)
			locationMatches = LocationCheck(browser)
			regex = r'\(.*?\)'
			TEMP_NAME = re.sub(regex, '', browser.title.replace(' | LinkedIn', ''))
			jobs = ["-","-"]
			locations = ["-","-"]
			jobs = ReturnJobMatch(browser) #jobtitle and temp_jobmatch
			locations = ReturnLocationMatch(browser) #location and temp_locationmatch
			#company = GetCompany(browser)
			company ="n/a"
			location = locations[0]
			job = jobs[0]
			templocation = locations[1]
			tempjob = jobs[1]
			if " at " in tempjob:
				company = tempjob.split(" at ",1)[1]
			elif " for " in jobs[0]:
				company = tempjob.split(" for ",1)[1]

			if DEEP_JOB_SEARCH and company != "n/a":
				companyresult = GetCompany(browser)
				if companyresult != "n/a":
					company = ("* "+companyresult)


			if DELIMIT_BY_LOCATION and VIEW_SPECIFIC_USERS:
				print("● Name: %-17s | T: %-2d | V: %-2d | Q: %-2d | Location: %-10s | Title: %-15s" %(TEMP_NAME, T, V, len(profilesQueued), location, job))
			elif DELIMIT_BY_LOCATION:
				print("● Name: %-17s | T: %-2d | V: %-2d | Q: %-2d | Location: %-10s" %(TEMP_NAME, T, V, len(profilesQueued), location))
			elif VIEW_SPECIFIC_USERS:
				print("● Name: %-17s | T: %-2d | V: %-2d | Q: %-2d | Title: %-15s" %(TEMP_NAME, T, V, len(profilesQueued), job))
			else:
				print("● Name: %-17s | T: %-2d | V: %-2d | Q: %-2d" %(TEMP_NAME, T, V, len(profilesQueued)))

			TEMP_PROFILE = [TEMP_NAME, jobs[0], jobs[1], locations[0], locations[1], company]

			AddToCSV(TEMP_PROFILE,TIME)
			
			if VERBOSE:
				print("-> Temp Profile List")
				print(TEMP_PROFILE)

			
			# Add the ID to the visitedUsersFile
			with open('connections.txt', 'a') as visitedUsersFile:
				visitedUsersFile.write((profileID)+'\r\n')
			visitedUsersFile.close()

			# Get new profiles ID
			time.sleep(random.uniform(2, 4))
			soup = BeautifulSoup(browser.page_source, PARSER)
			profilesQueued.extend(GetConnectionProfileURLS(soup, profilesQueued))
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


def NavigateToConnectionPage(browser):
	"""
	Navigate to the my network page and scroll to the bottom and let the lazy loading
	go to be able to grab more potential users in your network. It is recommended to
	increase the NUM_LAZY_LOAD value if you are using the variable
	SPECIFIC_USERS_TO_VIEW.
	browser: the selenium browser used to interact with the page.
	"""
	
	browser.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
	connectionCount = GetConnectionCount(browser)
	NumScrollsForAllConnections = connectionCount/8
	for counter in range(1,NUM_LAZY_LOAD):
		ScrollToBottomAndWaitForLoad(browser)

def GetConnectionProfileURLS(soup, profilesQueued):
	"""
	Get new profile urls to add to the navigate queue.
	soup: beautiful soup instance of page's source code.
	profileQueued: current list of profile queues.
	"""
	# Open, load and close
	with open('connections.txt', 'r') as visitedUsersFile:
		visitedUsers = [line.strip() for line in visitedUsersFile]
	visitedUsersFile.close()

	profileURLS = []
	#I would like to add location based veiwing here but cannot gain access based on LinkedIn's structure

	profileURLS.extend(FindProfileURLsInConnectionPage(soup, profilesQueued, profileURLS, visitedUsers))

	profileURLS = list(set(profileURLS))

	return profileURLS

def FindProfileURLsInConnectionPage(soup, profilesQueued, profileURLS, visitedUsers):
	"""
	Get new profile urls to add to the navigate queue from the connection page.
	soup: beautiful soup instance of page's source code.
	profileQueued: current list of profile queues.
	profileURLS: profile urls already found this scrape.
	visitedUsers: user's profiles that we have already viewed.
	"""

	newProfileURLS = []

	try:
		#for div in soup.find_all('div', class_='')
		for a in soup.find_all('a', class_='mn-connection-card__link'):
			if ValidateURL(a['href'], profileURLS, profilesQueued, visitedUsers):
				if VIEW_SPECIFIC_USERS:
					for span in a.find_all('span', class_='mn-connection-card__occupation'):
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


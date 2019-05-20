from imports import *
from reusable import *

TIME = str(datetime.datetime.now().time())

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
		CreateCSV(header, TIME)

	if PRINT_ACTIONS:
		print('-> Scraping User URLs on Network tab.')

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
			locationMatches = LocationCheck(browser)
			regex = r'\(.*?\)'
			TEMP_NAME = re.sub(regex, '', browser.title.replace(' | LinkedIn', ''))
			jobs = ReturnJobMatch(browser) #jobtitle and temp_jobmatch
			locations = ReturnLocationMatch(browser) #location and temp_locationmatch
			#company = GetCompany(browser)
			company ="n/a"
			if " at " in jobs[1]:
				company = jobs[1].split(" at ",1)[1] 
			elif " for " in jobs[1]:
				company = jobs[1].split(" for ",1)[1] 

			if DELIMIT_BY_LOCATION and VIEW_SPECIFIC_USERS:
				print("● Name: %-17s | T: %-2d | V: %-2d | Q: %-2d | Location: %-10s | Title: %-15s" %(TEMP_NAME, T, V, len(profilesQueued), locations[0], jobs[0]))
			elif DELIMIT_BY_LOCATION:
				print("● Name: %-17s | T: %-2d | V: %-2d | Q: %-2d | Location: %-10s" %(TEMP_NAME, T, V, len(profilesQueued), locations[0]))
			elif VIEW_SPECIFIC_USERS:
				print("● Name: %-17s | T: %-2d | V: %-2d | Q: %-2d | Title: %-15s" %(TEMP_NAME, T, V, len(profilesQueued), jobs[0]))
			else:
				print("● Name: %-17s | T: %-2d | V: %-2d | Q: %-2d" %(TEMP_NAME, T, V, len(profilesQueued)))

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

			TEMP_PROFILE = [TEMP_NAME, jobs[0], jobs[1], locations[0], locations[1], company, CONNECTED]
			if SAVECSV:
				AddToCSV(TEMP_PROFILE,TIME)
				#CSV_DATA.append(TEMP_PROFILE)
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

def NavigateToMyNetworkPage(browser):
	"""
	Navigate to the my network page and scroll to the bottom and let the lazy loading
	go to be able to grab more potential users in your network. It is recommended to
	increase the NUM_LAZY_LOAD value if you are using the variable
	SPECIFIC_USERS_TO_VIEW.
	browser: the selenium browser used to interact with the page.
	"""

	browser.get('https://www.linkedin.com/mynetwork/')
	for counter in range(1,NUM_LAZY_LOAD):
		ScrollToBottomAndWaitForLoad(browser)

def ConnectWithUser(browser):
	"""
	Connect with the user viewing if their job title is found in your list of roles
	you want to connect with.
	browse: the selenium browser used to interact with the page.
	"""

	soup = BeautifulSoup(browser.page_source, PARSER)
	global SESSION_CONNECTION_COUNT
	global CONNECTED
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
					print("\t* Saved "+filename)
				browser.save_screenshot(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Screenshots', filename))
			browser.find_element_by_xpath('//button[@class="pv-s-profile-actions pv-s-profile-actions--connect artdeco-button artdeco-button--3 mr2 mt2"]').click()
			time.sleep(3)
			browser.find_element_by_xpath('//button[@class="artdeco-button artdeco-button--3 ml1"]').click()
			CONNECTED = True
			SESSION_CONNECTION_COUNT += 1
			if PRINT_ACTIONS:
				print('\t* Sending the user an invitation to connect. Count = '+ str(SESSION_CONNECTION_COUNT))
		except:
			print("!!! Error connecting to " + TEMP_NAME)
			print(">>>> Name: "+TEMP_NAME+" Title: "+TEMP_JOB+" Location: "+TEMP_LOCATION)
			print(">>>> Location Match: "+ReturnLocationMatch+" Title Match: "+ jobTitleMatches)
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
	#I would like to add location based veiwing here but cannot gain access based on LinkedIn's structure

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





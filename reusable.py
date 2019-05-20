from imports import *


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
	time.sleep(2)

def LocationCheck(browser):
	'''
	Checks if the location of the user matches your list of locations
	browser = selenium webdriver
	returns true or false
	'''
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
	'''
	Gets the location that matches your settings
	browser = selenium webdriver
	returns the location and temp_locationmatch as a list
	'''
	temp_locationmatch = "X" #if this doesnt change it, it could have the previous connections data
	soup = BeautifulSoup(browser.page_source, PARSER)
	rtn = ["",""]
	locations = soup.findAll("h3", {"class": "pv-top-card-section__location"})
	for p in locations:
		for l in LOCATIONS:
			if l.lower() in p.text.lower():
				temp_locationmatch = str(" ".join((p.text.lower()).split()))
				location = str(l)
				print(location + " : " + temp_locationmatch)
				rtn = [location, temp_locationmatch]
				if VERBOSE:
					print(">>>> Location Match: "+rtn)
	if rtn[0] == "":
		rtn[0] = "X"
	if rtn[1] == "":
		rtn[1] = "X"
	else:
		return rtn

def ReturnJobMatch(browser):
	'''
	Gets the job that matches your settings
	browser = selenium webdriver
	returns the job and temp_jobmatch as a list
	'''
	temp_jobmatch = "X" #if this doesnt change it, it could have the previous connections data
	soup = BeautifulSoup(browser.page_source, PARSER)
	rtn = ["",""]
	for selection in soup.findAll("h2", {"class": "pv-top-card-section__headline"}):
		for job in SPECIFIC_USERS_TO_VIEW:
			if job.lower() in selection.text.lower():
				temp_jobmatch = (" ".join((selection.text.lower()).split()))
				jobtitle = str(job)
				print(jobtitle + " : " + temp_jobmatch)
				rtn = [jobtitle, temp_jobmatch]
				if VERBOSE:
					print(">>>> Job Match: "+rtn)
	if rtn[0] == "":
		rtn[0] = "X"
	if rtn[1] == "":
		rtn[1] = "X"
	else:
		return rtn

def CreateCSV(data, time):
	'''
	Creates initial CSV file
	data is the list that will get added to the file(in this case its the headers)
	time is the time at creation of this file
	'''
	if MODE.upper() == "VIEW/CONNECT":
		filename = 'Linked-In-'+time+'.csv'
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'CSV', filename), 'w') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(data)
		csvFile.close()
	elif MODE.upper() == "ANALYSIS":
		filename = 'Analysis-'+time+'.csv'
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Analysis', filename), 'w') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(data)
		csvFile.close()

def AddToCSV(data, time):
	'''
	Appends to the CSV file that matches the name with that time
	data is the list that will get added to the file
	time is the time at creation of this file
	'''
	if MODE.upper() == "VIEW/CONNECT":
		filename = 'Linked-In-'+time+'.csv'
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'CSV', filename), 'a') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(data)
		csvFile.close()
	elif MODE.upper() == "ANALYSIS":
		filename = 'Analysis-'+time+'.csv'
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Analysis', filename), 'a') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(data)
		csvFile.close()

def GetCompany(browser):
	'''
	Get first item in work experience on Linkedin
	browser = selenium webdriver
	Returns a single string that should be the job or nothing
	'''
	#A decent amount of false positives on this, more so than it makes me comfortable to actually push it. 
	#WIll probably revisit it but until then it wont be used.
	soup = BeautifulSoup(browser.page_source, PARSER)
	rtn = ""
	#if MODE.upper() == "VIEW/CONNECT":
	for tag in soup.findAll("span", {"class": "pv-entity__secondary-title"}):
		rtn = (tag.get_text())
		break
	# elif MODE.upper() == "ANALYSIS":
	# 	for tag in soup.findAll("span", {"class": "mn-connection-card__occupation"}):
	# 		rtn = (tag.get_text())
	# 		break
	
	if rtn != "":
		return rtn
	else:
		return("n/a")

def GetConnectionCount(browser):
	soup = BeautifulSoup(browser.page_source, PARSER)
	time.sleep(3)
	counthtml = soup.find("h1", attrs={'class':'t-18 t-black t-normal'})
	count = counthtml.get_text()
	count = int(re.sub('[^0-9]','', count))
	return count
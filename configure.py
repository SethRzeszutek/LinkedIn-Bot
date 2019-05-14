# Configurable Constants
from credentials import * 

CONFIGURED_EMAIL = email
CONFIGURED_PASSWORD = password

###-------ENVIRONMENT SETTINGS---------###
BROWSER = "Firefox" #Options are CHROME or FIREFOX
HEADLESS = True #Headless doesnt seem to run correctly in Chrome, so that is an issue. It works correctly in Firefox though
PRINT_ACTIONS = True
PRINT_SETTINGS = False


###-------BEAUTIFUL SOUP SETTINGS---------###
#Type of Parser for BeautifulSoup, lxml is the fastest but there are few different options
PARSER = "lxml"


###-------BOT SEARCH SETTINGS---------###


SCREENSHOTS = True
#For lists, you can enter partial words to search more broadly.
#For example, you can add 'Software' and titles like 'Software Developer' and 'Software Engineer' should work.

#Turn on Title Filter
VIEW_SPECIFIC_USERS = True
#Specific titles to filter by
SPECIFIC_USERS_TO_VIEW = ['CEO', 'CTO', 'Developer', 'HR', 'Recruiter','Software', 'Software Engineer', 'Python', 'Javascript', 'Node']

#Turn on Location Filter, this works only for Connecting
DELIMIT_BY_LOCATION = True
#List of locations to filter by
LOCATIONS = ['Ohio','Cleveland','Akron','Mentor','Chagrin', 'Solon', 'Westlake', 'Eastlake']

#Amount of times it will scroll the page to load more potential connections
#If you are using VIEW_SPECIFIC_USERS you might want to increase this value
NUM_LAZY_LOAD_ON_MY_NETWORK_PAGE = 10

#LinkedIn Limit on Connections is 15,000
#Turn on Quick Connecting with Users
CONNECT_WITH_USERS = True
#Limit the amount of people per session you will connect with
LIMIT_CONNECTION = True
CONNECTION_LIMIT = 20
#Don't connect with every single user
RANDOMIZE_CONNECTING_WITH_USERS = False
#List of Job titles to connect with
JOBS_TO_CONNECT_WITH = ['Developer', 'HR','Software', 'Software Engineer', 'Python', 'Javascript', 'Node']




###-------DEBUGGING---------###
#See more information about what the bot is doing
VERBOSE = False
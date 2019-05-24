# Configurable Constants
from credentials import *

CONFIGURED_EMAIL = email
CONFIGURED_PASSWORD = password

"""    ENVIRONMENT SETTINGS    """
BROWSER = "Chrome"  # Options are CHROME or FIREFOX
HEADLESS = True  # Headless doesnt seem to run correctly in Chrome, but works correctly in Firefox
PARSER = "lxml" #lxml is the fastest but there are few different options

# Amount of times it will scroll the page to load more potential connections
# If you are using VIEW_SPECIFIC_TITLES you might want to increase this value
LAZY_LOAD_NUM = 25

'''    TITLES SETTINGS    '''
VIEW_SPECIFIC_TITLES = True
SAVECSV = True #Save users viewed in CSV

'''    CONNECTING SETTINGS    '''
CONNECT_WITH_USERS = True
CONNECT_BY_LOCATION = True #Uses list of locations and only connects if they are in that list
LIMIT_CONNECTION = True #Limit number of users to connect with
CONNECTION_LIMIT = 50 #Max number of users to connect with
RANDOMIZE_CONNECTING_WITH_USERS = False #50/50 shot of connecting with the user
SCREENSHOTS = True #Screenshot user if you connect with them

'''    TITLES AND LOCATIONS    '''
# List of job and locations titles to view/connect with
# For lists, you can enter partial words to search more broadly.
# For example, you can add 'Software' and titles like 'Software Developer' and 'Software Engineer' should work.
# However, if you use a phrase like 'Developer' it will add 'Software Developer' and other things like 'Community Developer'
TITLES_TO_VIEW_CONNECT_WITH = ['Software Developer', 'Software', 'Software Engineer', 'Python', 'Javascript', 'Node']
LOCATIONS_TO_CONNECT = ['Ohio', 'Cleveland', 'Akron', 'Mentor', 'Chagrin', 'Solon', 'Westlake', 'Eastlake']

'''    VIEWING    '''
#BOX - is helpful and takes up the most space, it adds a nice box around each user.
#STANDARD - the normal view that is essentially a medium amount of space, you can still follow it but not as organized.
#COMPRESSED - the smallest view because sometimes size matters
VIEW_MODE = "BOX" #BOX, STANDARD, or COMPRESSED
PRINT_ACTIONS = True #See every major action the bot takes
PRINT_SETTINGS = False #Print settings before you start
EXTRA_USER_INFO = True #Print data that match your criteria with the user info

"""    DEBUGGING    """
VERBOSE = False #See more detailed info on what the bot is reading
POTENTIAL_COMPANY = True #This attempts to get the company name a new way that is prone to errors but would only be used when no company is found the normal way
DEBUGGING = True
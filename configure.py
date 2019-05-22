# Configurable Constants
from credentials import *

CONFIGURED_EMAIL = email
CONFIGURED_PASSWORD = password

"""    ENVIRONMENT SETTINGS    """
BROWSER = "Chrome"  # Options are CHROME or FIREFOX
HEADLESS = False  # Headless doesnt seem to run correctly in Chrome, but works correctly in Firefox
PARSER = "lxml" #lxml is the fastest but there are few different options

# Amount of times it will scroll the page to load more potential connections
# If you are using VIEW_SPECIFIC_TITLES you might want to increase this value
LAZY_LOAD_NUM = 18

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


"""    DEBUGGING    """
PRINT_ACTIONS = True #See every major action the bot takes
PRINT_SETTINGS = False #Print settings before you start
VERBOSE = False #See more detailed info on what the bot is reading
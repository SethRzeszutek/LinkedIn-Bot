# Configurable Constants
from credentials import *

CONFIGURED_EMAIL = email
CONFIGURED_PASSWORD = password

"""    ENVIRONMENT SETTINGS    """

BROWSER = "Chrome"  # Options are CHROME or FIREFOX
HEADLESS = False  # Headless doesnt seem to run correctly in Chrome, but works correctly in Firefox
PRINT_ACTIONS = True
PRINT_SETTINGS = False

"""    BEAUTIFUL SOUP SETTINGS  """

# Type of Parser for BeautifulSoup, lxml is the fastest but there are few different options
PARSER = "lxml"

"""    BOT SEARCH SETTINGS    """

# If connection is successful, store a screenshot of the user's page
SCREENSHOTS = True
# Save users viewed in CSV
SAVECSV = True

# Turn on Title Filter
VIEW_SPECIFIC_TITLES = True

""" For lists, you can enter partial words to search more broadly.
    For example, you can add 'Software' and titles like 'Software Developer' and 'Software Engineer' should work.
    However, if you use a phrase like 'Developer' it will add 'Software Developer' and other things like 'Community Developer' """

# Specific titles to filter by
#TITLES_TO_VIEW = ['CEO', 'CTO', 'Developer', 'HR', 'Recruiter', 'Software', 'Software Engineer', 'Python','Javascript', 'Node']


# List of job titles to connect with
TITLES_TO_VIEW_CONNECT_WITH = ['Software Developer', 'Software', 'Software Engineer', 'Python', 'Javascript', 'Node']

# Turn on Location Filter, this works only for Connecting
CONNECT_BY_LOCATION = True

# List of locations to filter by
LOCATIONS_TO_CONNECT = ['Ohio', 'Cleveland', 'Akron', 'Mentor', 'Chagrin', 'Solon', 'Westlake', 'Eastlake']

# Amount of times it will scroll the page to load more potential connections
# If you are using VIEW_SPECIFIC_TITLES you might want to increase this value
LAZY_LOAD_NUM = 18

# Turn on Quick Connecting with Users
CONNECT_WITH_USERS = True

# Limit the amount of people per session you will connect with
LIMIT_CONNECTION = True

# LinkedIn limit on Connections is 15,000
CONNECTION_LIMIT = 50

# Don't connect with every single user
RANDOMIZE_CONNECTING_WITH_USERS = False

"""    DEBUGGING    """
# See more information about what the bot is doing
VERBOSE = False

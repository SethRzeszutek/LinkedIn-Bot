![LinkedIn-Bot](https://i.imgur.com/od6HpD8.png)
[![Badges](https://img.shields.io/badge/language-Python-blue.svg)](https://github.com/SethRzeszutek/LinkedIn-Bot)
[![Badges](https://img.shields.io/badge/license-GPL-lightgreen.svg)](https://github.com/SethRzeszutek/LinkedIn-Bot)
[![Badges](https://img.shields.io/badge/version-2.1-lightgrey.svg)](https://github.com/SethRzeszutek/LinkedIn-Bot)
# LinkedInBot

Increase your likelihood to grow your connections and potentially get interview opportunities on LinkedIn by increasing visibility of your profile by viewing others profiles.

## About

![Stats](https://i.imgur.com/MVgProO.png)
When you view user's profile in LinkedIn they get notified that you have looked at their profile. This bot will allow you to view user's profiles thus increasing your visibility in your suggested LinkedIn network.

## Features
* Automate viewing and connecting with users based on their job title and/or location!
* Set a limit on how many connections you would like to connect with!
* Watch the browser work away or try out Headless mode! (Currently only working in Firefox)
* If connected store a screenshot or CSV of a users profile!
* Able to retrive user company about 70% of the time! (Still working on this!)
* If you have any suggestions open an issue and I or a contributor will gladly do our best to implement it if it aligns with the goals of the project! 

## Requirements

**Important:** make sure that you have your [Profile Viewing Setting](https://www.linkedin.com/settings/?trk=nav_account_sub_nav_settings) changed from 'Anonymous' to  'Public' so LinkedIn members can see that you have visited them and can visit your profile in return.
You also must change your language setting to **English**.

LinkedIn-Bot was updated to [Python 3+](https://www.python.org/downloads).

Before you can run the bot, you will need to install a few Python dependencies.
You can install the three below by doing: `pip install -r requirements.txt`

* [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4), for parsing html: `pip install BeautifulSoup4`
* [Selenium](http://www.seleniumhq.org/), for browser automation: `pip install Selenium`
* lxml for quicker HTML parsing: `pip install lxml`

You will also need the appropriate web driver that you would like as specificed in [Selenium](https://selenium-python.readthedocs.io/installation.html):
"Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, which needs to be installed before the below examples can be run. Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin.

Failure to observe this step will give you an error selenium.common.exceptions.WebDriverException: Message: ‘geckodriver’ executable needs to be in PATH.

Other supported browsers will have their own drivers available. Links to some of the more popular browser drivers follow."
* Chrome:	https://sites.google.com/a/chromium.org/chromedriver/downloads
	* On MacOS if you have [HomeBrew](https://brew.sh) installed you can use `brew install chromedriver`
* Firefox:	https://github.com/mozilla/geckodriver/releases
	* On MacOS if you have [HomeBrew](https://brew.sh) installed you can use `brew install geckodriver`



You will need to install the [webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for Google Chrome then put it in the same folder than the bot if you are on Windows, or in the `/usr/bin` folder if you are on OS X.

## Configuration and Running
To run the bot go into the directory where the bot is stored and type `python LinkedInBot-Convert.py`

Before you run the bot, edit the configuration portion of the script. This will include your account login information (email, password, etc.) and other logical values to make the bot more of your own. It's that simple!

Edit or create a `credentials.py` file for the config file to fetch from
```python
email = ''
password = ''
```
Then edit the `configure.py` file for other settings
```python
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
TITLES_TO_VIEW_CONNECT_WITH = ['Software Developer', 'Software Engineer','Javascript']
LOCATIONS_TO_CONNECT = ['Ohio', 'Cleveland', 'Akron']


"""    DEBUGGING    """
PRINT_ACTIONS = True #See every major action the bot takes
PRINT_SETTINGS = False #Print settings before you start
VERBOSE = False #See more detailed info on what the bot is reading
```


## Run
Once you have installed the required dependencies, created `credentials.py`, and edited the `configure.py` file, you can run the bot.

Make sure you are in the correct folder and run the following command: `python LinkedInBot.py`

## Output

T: Number of profiles the bot tried to access;

V: Number of profiles the bot actually visited (profiles you can access: rank 3 or less);

Q: Number of profiles in queue.

## POTENTIAL ISSUES

* 2 Factor Authentication
	* Solution: Working on a setting to give more time to get it, if it is enabled you cannot use headless mode
* Stuck on `-> Scraping User URLs on Network tab.`
	* Solution: I have encountered this issue before and restarting the script usually works
* LinkedIn Security Email
	* You were sent a pin to make sure its really you, either enter the pin if you are not in headless mode or restart the bot.
	* At this point it might be best to tread lightly, as your account could be flagged and being monitored. However I am not certain on that.

## DISCLAIMER

The use of bots and scrapers are mentioned [here](https://www.linkedin.com/help/linkedin/answer/56347/prohibited-software-and-extensions?lang=en).
Use this bot at your own risk. 
Just to push more knowledege a judge in California ruled that they cannot prohibit bots([article](https://www.bbc.com/news/technology-40932487)).

## Note

Updated and improved based on the sweet projects [Matt Flood](https://github.com/MattFlood7/LinkedInBot) and [LInBot](https://github.com/helloitsim/LInBot).
I would have made this a branch on Matt Flood's version, however I was tailoring it more specifically to my needs rather than making a setting out of everything. Just as he stood on helloitsim, I stand on the work that Matt Flood has done.

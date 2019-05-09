# LinkedInBot
Increase your likelihood to grow your connections and potentially get interview opportunities on LinkedIn by increasing visibility of your profile by viewing others profiles.
## About
When you view user's profile in LinkedIn they get notified that you have looked at their profile. This bot will allow you to view user's profiles thus increasing your visibility in your suggested LinkedIn network.
<p align="center">
  <img src="https://preview.ibb.co/mMDuAk/linked_In_Bot_Profile_View_Results.png" alt="LinkedInBot Result" width="325" height="200">
</p>

## Note

Updated and improved based on the sweet projects [Matt Flood](https://github.com/MattFlood7/LinkedInBot) and [LInBot](https://github.com/helloitsim/LInBot).

## Requirements
**Important:** make sure that you have your [Profile Viewing Setting](https://www.linkedin.com/settings/?trk=nav_account_sub_nav_settings) changed from 'Anonymous' to  'Public' so LinkedIn members can see that you have visited them and can visit your profile in return.
You also must change your language setting to **English**.

LinkedIn-Bot was updated to [Pyhton 3+](https://www.python.org/downloads).

Before you can run the bot, you will need to install a few Python dependencies.
You can install the three below by doing: `pip install -r requirements.txt`

- [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4), for parsing html: `pip install BeautifulSoup4`
- [Selenium](http://www.seleniumhq.org/), for browser automation: `pip install Selenium`
- xlmx for quicker HTML parsing: `pip install xmlx`

You will need to install the [webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for Google Chrome then put it in the same folder than the bot if you are on Windows, or in the `/usr/bin` folder if you are on OS X.

## Configuration
Before you run the bot, edit the configuration portion of the script. This will include your account login information (email, password, etc.) and other logical values to make the bot more of your own. It's that simple!

```python
# Configurable Constants
EMAIL = 'youremail@gmail.com'
PASSWORD = 'password'
VIEW_SPECIFIC_USERS = False
SPECIFIC_USERS_TO_VIEW = ['CEO', 'CTO', 'Developer', 'HR', 'Recruiter']
NUM_LAZY_LOAD_ON_MY_NETWORK_PAGE = 5
CONNECT_WITH_USERS = True
RANDOMIZE_CONNECTING_WITH_USERS = True
JOBS_TO_CONNECT_WITH = ['CEO', 'CTO', 'Developer', 'HR', 'Recruiter']
ENDORSE_CONNECTIONS = False
RANDOMIZE_ENDORSING_CONNECTIONS = True
VERBOSE = True
```

## Run
Once you have installed the required dependencies and edited the `config` file, you can run the bot.

Make sure you are in the correct folder and run the following command: `python LinkedInBot.py`

Then, after choosing your favorite browser the bot will start visiting profiles.

## Output

![LinkedInBot Demo Gif](http://g.recordit.co/xPh4gK70lz.gif)

T: Number of profiles the bot tried to access;

V: Number of profiles the bot actually visited (profiles you can access: rank 3 or less);

Q: Number of profiles in queue.

## Enhancements
Please feel free to message me or open an issue if you have an idea for an enhancement! Seems like people are starting to use this and I would like to improve it.




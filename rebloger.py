import argparse
import getpass
from logger import get_logger
from mastodon import Mastodon
import operator

# VARS
## Initiating variables
userToReblogID: int = ""
userWhoPostsID: int = ""
api = ""
baseUrl: str = ""
accessToken: str = ""
userWhoPosts: str = ""
userToReblog: str = ""
original_status: dict = {}
lastReblogedPost: int = ""
userWhoPostsStatus: list = []
filtered_statuses: list = []
newStatusToReblog: list = []
logLevel: str = "INFO"

# # Getting cmd parameters
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Requirements to use Rebloger"
    )
    parser.add_argument("--baseUrl", required=True, type=str, help="Instance URL (example: 'mastodon.social')")
    parser.add_argument("--accessToken", required=False, type=str, help="App acces token, don't use it to type it securely later")
    parser.add_argument("--userToReblog", required=True, type=str, help="Type username to reblog its posts with format 'username@instance' (example: 'nlhomme@pixelfed.social')")
    parser.add_argument("--userWhoPosts", required=True, type=str, help="Type username who will post with format 'username@instance' (example: 'nlhomme@mastodon.social')")
    parser.add_argument("--logLevel", required=False, type=str, help="Log level between DEBUG, INFO, WARNING, ERROR AND CRITICAL (default set to INFO)")

    args = parser.parse_args()

    baseUrl = args.baseUrl
    accessToken = args.accessToken
    userToReblog = args.userToReblog
    userWhoPosts = args.userWhoPosts
    logLevel = args.logLevel


# FUNCTIONS
## TODO: doc functions
def getID(username, followed: bool = False):
## TODO: If the access token or the user to reblog is not found, exit with error
    try:
        usernameInfos = api.account_search(username, following=followed)
        return usernameInfos[0].id
    except Exception as errorMessage:
        print('ERROR', errorMessage)

def getStatuses (userID, sincePostID):
    return api.account_statuses(userID, since_id = sincePostID)


# START
## Inviting user to provide his app acess token if not done via cmd parameters:
if not accessToken:
    print("Please provide your acess token:")
    accessToken = getpass.getpass(prompt="Access token:")

## Preparing API acess
api = Mastodon(access_token=accessToken, api_base_url=baseUrl)

## Preparing log file
logger = get_logger("logs", "rebloger", logLevel)

## Getting infos about the user to reblog's and the user who posts
userToReblogID = getID(userToReblog, True)
userWhoPostsID = getID(userWhoPosts)

## Printing IDs
logger.info("ID for " + userToReblog + " is " + str(userToReblogID))
logger.info("ID for " + userWhoPosts + " is " + str(userWhoPostsID))

# If last rebloged post is unknown then get it from user's statuses
# lastReblogedPost can be empty with no incidence
userWhoPostsStatuses = getStatuses(userWhoPostsID, lastReblogedPost)
#print(userWhoPostsStatus)

for status in userWhoPostsStatuses:
    original_status = status['reblog']
    if original_status and original_status['account']['id'] == userToReblogID:
        lastReblogedPost = original_status['id']
logger.debug(lastReblogedPost)

logger.info("The last status from " + userToReblog + " rebloged by " + userWhoPosts + " has ID " + str(lastReblogedPost))


#Debut cycle

# Geting new status to reblog since the last one
# lastReblogedPost can be empty with no incidence
newStatusToReblog = getStatuses(userToReblogID, lastReblogedPost)
logger.debug(newStatusToReblog)

#    Reblog des posts pixelfed ultérieurs à lastReblogedPost

#Mise en attente du prochain cycle
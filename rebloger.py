import argparse
import getpass
from logger import get_logger
from mastodon import Mastodon

# VARS
userToReblogID = None
userWhoPostsID = None
api = None
baseUrl = ""
accessToken = ""
userWhoPosts = ""
userToReblog = ""
lastReblogedPost = None
logLevel = "INFO"

# Getting cmd parameters
def parse_arguments():
    parser = argparse.ArgumentParser(description="Requirements to use Rebloger")
    parser.add_argument("--baseUrl", required=True, type=str, help="Instance URL (example: 'mastodon.social')")
    parser.add_argument("--accessToken", required=False, type=str, help="App access token, don't use it to type it securely later")
    parser.add_argument("--userToReblog", required=True, type=str, help="Type username to reblog its posts with format 'username@instance' (example: 'nlhomme@pixelfed.social')")
    parser.add_argument("--userWhoPosts", required=True, type=str, help="Type username who will post with format 'username@instance' (example: 'nlhomme@mastodon.social')")
    parser.add_argument("--logLevel", required=False, type=str, help="Log level between DEBUG, INFO, WARNING, ERROR AND CRITICAL (default set to INFO)")
    return parser.parse_args()

# FUNCTIONS
def getID(api, username, followed=False):
    try:
        usernameInfos = api.account_search(username, following=followed)
        return usernameInfos[0].id
    except Exception as errorMessage:
        print('ERROR:', errorMessage)
        exit(1)

def getStatuses(api, userID, sincePostID=None):
    return api.account_statuses(userID, since_id=sincePostID)

def main():
    global baseUrl, accessToken, userToReblog, userWhoPosts, logLevel, api, userToReblogID, userWhoPostsID, lastReblogedPost

    args = parse_arguments()

    baseUrl = args.baseUrl
    accessToken = args.accessToken
    userToReblog = args.userToReblog
    userWhoPosts = args.userWhoPosts
    logLevel = args.logLevel

    if not accessToken:
        print("Please provide your access token:")
        accessToken = getpass.getpass(prompt="Access token:")

    api = Mastodon(access_token=accessToken, api_base_url=baseUrl)

    logger = get_logger("logs", "rebloger", logLevel)

    userToReblogID = getID(api, userToReblog, True)
    userWhoPostsID = getID(api, userWhoPosts)

    logger.info(f"ID for {userToReblog} is {userToReblogID}")
    logger.info(f"ID for {userWhoPosts} is {userWhoPostsID}")

    userWhoPostsStatuses = getStatuses(api, userWhoPostsID, lastReblogedPost)

    for status in userWhoPostsStatuses:
        logger.debug(f"STATUS - DEBUG {status}")
        original_status = status.get('reblog')
        if original_status and original_status['account']['id'] == userToReblogID:
            lastReblogedPost = original_status['id']
    logger.debug(lastReblogedPost)

    logger.info(f"The last status from {userToReblog} rebloged by {userWhoPosts} has ID {lastReblogedPost}")

    newStatusToReblog = getStatuses(api, userToReblogID, lastReblogedPost)
    logger.debug(newStatusToReblog)

if __name__ == "__main__":
    main()

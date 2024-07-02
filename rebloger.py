import argparse
import getpass
from mastodon import Mastodon
import operator

# TODO:
# Turn print statements into logs

# VARS
## Init variables
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

# # Get cmd parameters
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Requirements to use Rebloger"
    )
    parser.add_argument("--baseUrl", required=True, type=str, help="Instance URL (example: 'mastodon.social')")
    parser.add_argument("--accessToken", required=False, type=str, help="App acces token, requires scopes 'read:accounts', 'read:statuses' and 'write:statuses'")
    parser.add_argument("--userToReblog", required=True, type=str, help="Type username to reblog its posts with format 'username@instance' (example: 'nlhomme@pixelfed.social')")
    parser.add_argument("--userWhoPosts", required=True, type=str, help="Type username who will post with format 'username@instance' (example: 'nlhomme@mastodon.social')")
    args = parser.parse_args()

    baseUrl = args.baseUrl
    accessToken = args.accessToken
    userToReblog = args.userToReblog
    userWhoPosts = args.userWhoPosts


# FUNCTIONS
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
## Invite user to provide his app acess token if not done via cmd parameters:
if not accessToken:
    print("Please provide your acess token:")
    accessToken = getpass.getpass(prompt="Access token:")

## Preparing API acess
api = Mastodon(access_token=accessToken, api_base_url=baseUrl)

## Getting infos about the user to reblog's and the user who posts
## TODO: Turn to function that return only ID
userToReblogID = getID(userToReblog, True)
userWhoPostsID = getID(userWhoPosts)

## Printing IDs
## TODO: turn to function to print AND log
print("ID for " + userToReblog + " is " + str(userToReblogID))
print("ID for " + userWhoPosts + " is " + str(userWhoPostsID))

# If last rebloged post is unknown
# Then get it from user's statuses
# lastReblogedPost can be empty with no incidence
userWhoPostsStatuses = getStatuses(userWhoPostsID, lastReblogedPost)
#print(userWhoPostsStatus)

for status in userWhoPostsStatuses:
    original_status = status['reblog']
    if original_status and original_status['account']['id'] == userToReblogID:
        lastReblogedPost = original_status['id']
print(lastReblogedPost)

print("The last status from " + userToReblog + " rebloged by " + userWhoPosts + " has ID " + str(lastReblogedPost))


#Debut cycle

# Get new status to reblog since the last one
# lastReblogedPost can be empty with no incidence
newStatusToReblog = getStatuses(userToReblogID, lastReblogedPost)
print(newStatusToReblog)

#    Reblog des posts pixelfed ultérieurs à lastReblogedPost

#Mise en attente du prochain cycle
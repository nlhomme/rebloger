import argparse
import getpass
from mastodon import Mastodon

# TODO:
# Turn print statements into logs

# VARS
## Init variables
userToReblogInfos = "" 
api = ""
baseUrl = ""
accessToken = ""
userToReblog = ""
lastReblogedPost = ""

# Get cmd parameters
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Requirements to use Rebloger"
    )
    parser.add_argument("--baseUrl", required=True, type=str, help="Instance URL (example: 'mastodon.social')")
    parser.add_argument("--accessToken", required=False, type=str, help="App acces token, requires scopes 'read:accounts', 'read:statuses' and 'write:statuses'")
    parser.add_argument("--userToReblog", required=True, type=str, help="Type username to reblog its posts with format 'username@instance' (example: 'nlhomme@pixelfed.social')")
    args = parser.parse_args()

    baseUrl = args.baseUrl
    accessToken = args.accessToken
    userToReblog = args.userToReblog


# FUNCTIONS


# START
## Invite user to provide his app acess token if not done via cmd parameters:
if not accessToken:
    print("Please provide your acess token:")
    accessToken = getpass.getpass(prompt="Access token:")

# TODO: capter les erreur de token

## Preparing API acess
api = Mastodon(access_token=accessToken, api_base_url=baseUrl)

## Getting user to reblog's informations
## If the access token or the user to reblog is wrong or not found, exit with error
try:
    userToReblogInfos = api.account_search(userToReblog, following=True)
except Exception as errorMessage:
    print('ERROR', errorMessage)

## Printing id
#print("ID for " + userToReblog + " is " + str(userToReblogInfos[0].id))


# If last rebloged post is unknown
# Then get it from user's timeline
#if lastReblogedPost == "":
#    api.account_statuses()


#Vérifier la veleur de la variable qui contient le dernier id repouété
#Si la var est vide, consulter les pouets Mastodon et trouver le dernier repouety

#Debut cycle

#    Lecture des posts pixelfed ultérieurs à l'horodatage

#    Reblog des posts pixelfed ultérieurs à l'horodatage

#Mise en attente du prochain cycle


#api.status_post("Test de l'API Mastodon / Testing Mastodon's API")

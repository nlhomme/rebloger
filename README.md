# Rebloger (Work in progress)

Rebloger is a Python script that automatically reblogs (or retoots) a post from a fediverse user of your choice

## Requirements

- Follow the account you plan to reblog posts from
- Python 3 if you plan to run the scripton a local machine ([download Python3](https://www.python.org/downloads/))
- Docker if you plan to run the script in a container
- An acess token to your Mastodon account:
  - Access you regular Mastodon account from a web browser
  - **Optional**: mute that account to avoid seeing its publications and polluting your timeline
  - Go to "Preferences" -> "Development"
  - Click "New Application" and:
    - Give it a name
    - In the "Scopes" section, check **ONLY** "read:statuses", "read:accounts" and "write:statuses"
    - Click "SUBMIT"
    - Copy the access token somewhere safe such as your password manager

## Limitations

- You can only reblog an account's posts from the moment you follow it, more on the Fediverse documentation: </p>
<https://fedi.tips/why-arent-all-mastodon-and-fediverse-posts-and-accounts-automatically-visible-from-all-servers/>

## Usage

### On your machine

Install the script's requirements:

```bash
pip install -r requirements.txt
```

Run

If one or several parameters is/are missing, an errer will appear:

```bash
python /Users/nicolas/git/python/rebloger/rebloger.py                                                                                 
usage: rebloger.py [-h] --baseUrl BASEURL [--accessToken ACCESSTOKEN] --userToReblog USERTOREBLOG
reblog.py: error: the following arguments are required: --baseUrl, --userToReblog
```

Help is available via the `-h` or `--help`:

```bash
python /Users/nicolas/git/python/rebloger/rebloger.py --help
usage: rebloger.py [-h] --baseUrl BASEURL [--accessToken ACCESSTOKEN] --userToReblog USERTOREBLOG

Requirements to reblog recent posts from someone

options:
  -h, --help            show this help message and exit
  --baseUrl BASEURL     Instance URL (example: 'mastodon.social')
  --accessToken ACCESSTOKEN
                        App acces token, requires scopes 'read:accounts', 'read:statuses' and 'write:statuses'
  --userToReblog USERTOREBLOG
                        Type username to reblog its posts with format 'username@instance' (example: 'nlhomme@pixelfed.social')
```

### Using Docker
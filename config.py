"""
    This file contains configuration stuff for the sendemails module

    It depends on the configuration file placed at ~/.config/sendemails/sendemails.yaml

    Contents expected in the configuration file are:

# Client secrets: this is the file downloaded from google that contains keys to get credentials
client_secret_path: 'path to the gmail credentials.json file'


# The token file stores the user's access and refresh tokens, and is created
# automatically when the authorization flow completes for the first time.
token_path: 'path to the gmail token file'


# When changin the scopes, remember to remove the token file so it can be regenerated
# Check scopes at: https://developers.google.com/gmail/api/auth/scopes
scopes: 'https://www.googleapis.com/auth/gmail.send'


# Folder containing the files with the email specs to be sent
email_folder: './emails'


# Sender of the messages
sender: 'your email address'


# time in seconds to wait from one email to the next (so gmail does not
# get too busy)
time_sleep_seconds: 1

"""
from pathlib import Path
import yaml

CONFIG_FILE_PATH = Path('~/.config/sendemails/sendemails.yaml').expanduser()

assert CONFIG_FILE_PATH.is_file(), "No configuration file found"

with open(CONFIG_FILE_PATH) as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.SafeLoader)

# Check for minimum contents
assert 'client_secret_path' in config
assert 'token_path' in config
assert 'sender' in config

client_secret_path = Path(config['client_secret_path']).expanduser()
token_path = Path(config['token_path']).expanduser()
scopes = config.get('scopes', 'https://www.googleapis.com/auth/gmail.send')
email_folder = Path(config.get('email_folder', './emails')).expanduser().resolve()
sender = config['sender']
time_sleep_seconds = config.get('time_sleep_seconds', 1)

# check paths actualy exist
assert client_secret_path.is_file(), f"file not found: {client_secret_path}"
assert token_path.is_file(), f"file not found: {token_path}"
assert email_folder.is_dir(), f"folder not found: {email_folder}"

from __future__ import print_function

import datetime
import os.path

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

all_events = []
SCOPES = ['https://www.googleapis.com/auth/calendar']

auth_url = 'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=759569633564' \
           '-q85sfhj5q0mfrolot0s9q0aodp6vdb85.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A57514' \
           '%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.readonly&state' \
           '=0Z2RJ0fKTeyINcmaFqqQeHobMsFmiZ&access_type=offline '


def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

if __name__ == '__main__':
    main()



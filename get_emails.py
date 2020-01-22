from __future__ import print_function
import pickle
import os.path
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pprint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']
service = None


def initialize_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels
    """
    global service

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

def get_unread_mails():
    # Call the Gmail API
    #results = service.users().labels().list(userId='me').execute()
    #labels = results.get('labels', [])

    results = service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
    #pprint.pprint(results1['messages'])

    #msg_id = results1['messages'][1]['id']
    #pprint.pprint(service.users().messages().get(userId='me', id=msg_id).execute())
    #pprint.pprint(service.users().messages().get(userId='me', id=msg_id).execute())

    '''
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
    '''

    return results

def get_attachments(mails):
    mails_kept = []

    if not os.path.exists('attachments'):
        os.mkdir('attachments')

    for mail in mails['messages']:
        msg_id = mail['id']
        msg = service.users().messages().get(userId='me', id=msg_id).execute()
        #pprint.pprint(msg)

        for header in msg['payload']['headers']:
            if header['name'] == 'Subject' and 'Exercise Tracker' in header['value']:
                mails_kept.append(msg_id)
                for part in msg['payload']['parts']:
                    if part['filename']:
                        if 'data' in part['body']:
                            data = part['body']['data']
                        else:
                            attachment_id = part['body']['attachmentId']
                            attachment = service.users().messages().attachments().get(userId='me', messageId=msg_id, id=attachment_id).execute()
                            data = attachment['data']
                        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                        save_path = os.getcwd()+'\\attachments\\'+part['filename']

                        with open(save_path, 'wb') as sp:
                            sp.write(file_data)
    return mails_kept

def mark_read(mails):
    for mail in mails:
        msg_label = {'removeLabelIds': ['UNREAD']}
        ret = service.users().messages().modify(userId='me', id=mail, body=msg_label).execute()
        print('ret', ret)

if __name__ == '__main__':
    initialize_service()
    unread_mails = get_unread_mails()
    mails_kept = get_attachments(unread_mails)
    mark_read(mails_kept)
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
import time


def mark_unread_emails_as_read(service, user_id='me'):
    all_messages = []
    request = service.users().messages().list(userId=user_id, labelIds=['UNREAD'])

    print("Starting to fetch unread messages...")

    while request is not None:
        try:
            response = request.execute()
            if 'messages' in response:
                all_messages.extend(response['messages'])
                print(f"Fetched {len(response['messages'])} unread messages...")
                for message in response['messages']:
                    try:
                        # Attempt to mark the message as read by removing the 'UNREAD' label
                        service.users().messages().modify(userId=user_id, id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
                        print(f"Marked message {message['id']} as read.")
                    except HttpError as error:
                        if error.resp.status == 400:
                            print(f"Skipping message {message['id']} due to precondition failure.")
                        else:
                            raise # raise for some other error
        except HttpError as error:
            print(f"An error occurred: {error}")
            time.sleep(1)  # Sleep 1 sec, then continue

        # Get the next page of unread messages
        request = service.users().messages().list_next(previous_request=request, previous_response=response)

    return all_messages

def main():
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    CLIENT_SECRETS_FILE = 'credentials.json'

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=credentials)

    # Fetch and mark all unread emails as read
    emails = mark_unread_emails_as_read(service)
    print(f'Total unread emails processed: {len(emails)}')

if __name__ == '__main__':
    main()


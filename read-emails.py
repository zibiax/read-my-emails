from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def mark_unread_emails_as_read(service, user_id='me'):
    all_messages = []
    # Fetch only unread messages by specifying labelIds as ['UNREAD']
    request = service.users().messages().list(userId=user_id, labelIds=['UNREAD'])

    print("Starting to fetch unread messages...")

    while request is not None:
        response = request.execute()
        if 'messages' in response:
            all_messages.extend(response['messages'])
            print(f"Fetched {len(response['messages'])} unread messages...")
            for message in response['messages']:
                # Mark the message as read by removing the 'UNREAD' label
                service.users().messages().modify(userId=user_id, id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
                print(f"Marked message {message['id']} as read.")

        # Get the next page of unread messages
        request = service.users().messages().list_next(previous_request=request, previous_response=response)

    print("Completed processing all unread messages.")
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


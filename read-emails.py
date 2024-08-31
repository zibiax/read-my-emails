import asyncio
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from aiohttp import ClientSession

# Define the async function to mark an email as read
async def mark_email_as_read(session, token, user_id, message_id):
    url = f'https://gmail.googleapis.com/gmail/v1/users/{user_id}/messages/{message_id}/modify?alt=json'
    body = {'removeLabelIds': ['UNREAD']}
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    async with session.post(url, json=body, headers=headers) as response:
        if response.status == 200:
            print(f"Successfully marked message {message_id} as read.")
        else:
            print(f"Failed to mark message {message_id} as read. Status: {response.status}")

# Function to fetch all unread emails and process them concurrently
async def mark_unread_emails_as_read(service, token, user_id='me'):
    all_messages = []
    request = service.users().messages().list(userId=user_id, labelIds=['UNREAD'])
    
    print("Starting to fetch unread messages...")

    async with ClientSession() as session:
        while request is not None:
            try:
                response = request.execute()
                if 'messages' in response:
                    all_messages.extend(response['messages'])
                    print(f"Fetched {len(response['messages'])} unread messages...")
                    
                    # Schedule marking emails as read concurrently
                    tasks = [
                        asyncio.create_task(mark_email_as_read(session, token, user_id, message['id']))
                        for message in response['messages']
                    ]
                    
                    # Wait for all tasks to complete
                    await asyncio.gather(*tasks)

            except HttpError as error:
                print(f"An error occurred: {error}")
                await asyncio.sleep(1)  # Sleep briefly before retrying

            # Get the next page of unread messages
            request = service.users().messages().list_next(previous_request=request, previous_response=response)

    print("Completed processing all unread messages.")
    return all_messages

# Entry point for running the script
def main():
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    CLIENT_SECRETS_FILE = 'credentials.json'

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=credentials)

    # Access the OAuth token directly from credentials
    token = credentials.token

    # Run the asyncio event loop to process unread emails
    reading_emails = asyncio.run(mark_unread_emails_as_read(service, token))
    print(f'{len(reading_emails)} Emails has been marked read')


if __name__ == '__main__':
    main()


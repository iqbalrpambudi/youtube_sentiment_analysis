import os
import csv
import google.oauth2.credentials
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyDkvj9b0-5BNIiFZXlTvVkeDOOo5WJNKYM"
video_id = "JbxULCgqLPg"
#"oHLabJiGl_Q"
service = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)
    
 
 
 
def get_video_comments(service, **kwargs):
    comments = []
    results = service.commentThreads().list(**kwargs).execute()

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        # Check if another page exists
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break
    print(comments)
    write_to_csv(comments)

 
 
def write_to_csv(comments):
    with open('Vaksin Covid-19 Tiba di Tanah Air.csv', 'w') as comments_file:
        comments_writer = csv.writer(comments_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        comments_writer.writerow(['Title','Comment'])
        for row in comments:
            # convert the tuple to a list and write to the output file
            comments_writer.writerow(list([row]))
 
if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    
    get_video_comments(service, part='snippet', videoId=video_id,maxResults=100, textFormat='plainText')
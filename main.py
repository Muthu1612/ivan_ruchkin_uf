import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from google_service import GoogleService
from github_service import GitHubService

# Define scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Load credentials
creds = Credentials.from_service_account_file("creds/prod.json", scopes=SCOPES)
client = gspread.authorize(creds)

#Initialize services
google_service = GoogleService()
github_service = GitHubService()

#get email id from user
email = input("Enter your email ID: ")


# #try to give google drive access
drive_success = google_service.share_file(email, role="fileOrganizer")

if drive_success:
    print(f"✅ Drive access given for: {email}")
else:
    print(f"❌ Failed to give Drive access for: {email}")

#try to give github access
github_success = github_service.invite_user(email, role="direct_member")

if github_success:
    print(f"✅ Github access given for: {email}")
else:
    print(f"❌ Failed to give Github access for: {email}")
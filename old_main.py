import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe
from google.oauth2.service_account import Credentials
from google_service import GoogleService

# Define scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Load credentials
creds = Credentials.from_service_account_file("creds/prod.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Open sheet (by key or by URL)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/12bJ_q9uOUkiazJvZRfF1ml7iQyUgsiS4rs2qGDOUfJ8/edit?resourcekey=&gid=2033677273#gid=2033677273")
worksheet = sheet.sheet1

# Convert to pandas DataFrame
df = get_as_dataframe(worksheet, evaluate_formulas=True, header=0)

# Clean the dataframe - remove empty rows
df = df.dropna(subset=['Email Address'])

# Initialize Google Service
google_service = GoogleService()

print("\n" + "="*50)
print("ACCESS STATUS CHECK")
print("="*50)

# Loop through each row
for index, row in df.iterrows():
    email = str(row['Email Address']).strip()
    
    # Skip if email is empty or NaN
    if email == '' or email == 'nan' or pd.isna(row['Email Address']):
        continue
        
    # Check Drive Access
    drive_access = str(row['Drive Access']).strip() if pd.notna(row['Drive Access']) else ""
    if drive_access.lower() != "✅ given":
        print(f"🔴 Drive access not given to: {email}")
        # continue
        # Give Content Manager (fileOrganizer) access
        success = google_service.share_file(email, role="fileOrganizer")
        
        # Update the spreadsheet if access was successfully given
        if success:
            try:
                # Find the row in the spreadsheet (adding 2 because: 1 for header, 1 for 0-based index)
                sheet_row = index + 2
                
                # Find the column number for 'Drive Access'
                drive_access_col = None
                header_row = worksheet.row_values(1)  # Get header row
                for col_index, header in enumerate(header_row, start=1):
                    if header == 'Drive Access':
                        drive_access_col = col_index
                        break
                
                if drive_access_col:
                    # Update the cell to "Given"
                    worksheet.update_cell(sheet_row, drive_access_col, "✅ Given")
                    print(f"✅ Updated spreadsheet: Drive access marked as 'Given' for {email}")
                else:
                    print(f"⚠️ Could not find 'Drive Access' column in spreadsheet")
                    
            except Exception as e:
                print(f"❌ Error updating spreadsheet for {email}: {e}")
        else:
            print(f"⚠️ Drive access failed for {email}, not updating spreadsheet")
    
    # Check GitHub Access
    github_access = str(row['GitHub Access']).strip() if pd.notna(row['GitHub Access']) else ""
    if "invite" not in github_access.lower():
        print(f"🟡 GitHub access not given to: {email}")

print("\n" + "="*50)
print("ACCESS CHECK COMPLETE")
print("="*50)
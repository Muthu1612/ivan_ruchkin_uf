from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

class GoogleService:
    def __init__(self, service_account_file: str = None, file_id: str = None, default_role: str = "reader"):
        # Load environment variables automatically
        load_dotenv()
        
        # Use provided parameters or fall back to environment variables
        self.service_account_file = service_account_file or os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
        self.file_id = file_id or os.getenv("GOOGLE_FILE_ID")
        self.default_role = default_role or os.getenv("DEFAULT_SHARE_ROLE", "reader")
        
        # Validate required parameters
        if not self.service_account_file or not self.file_id:
            raise ValueError(
                "Missing required Google Drive configuration. "
                "Provide service_account_file and file_id as parameters or set "
                "GOOGLE_SERVICE_ACCOUNT_FILE and GOOGLE_FILE_ID in .env file"
            )

        self.scopes = ["https://www.googleapis.com/auth/drive"]

        # Authenticate service
        try:
            creds = service_account.Credentials.from_service_account_file(
                self.service_account_file, scopes=self.scopes
            )
            self.service = build("drive", "v3", credentials=creds)
            
            print("🔧 Google Drive Service initialized")
            # print(f"   File/Folder ID: {self.file_id}")
            # print(f"   Default Role: {self.default_role}")
            # print("---")
        except Exception as e:
            raise Exception(f"Failed to initialize Google Drive service: {e}")

    def share_file(self, email: str, role: str = None) -> bool:
        """Share file or folder with a single user"""
        role = role or self.default_role
        try:
            permission = {
                "type": "user",
                "role": role,        # e.g., "reader", "writer", "commenter", "fileOrganizer"
                "emailAddress": email,
            }
            self.service.permissions().create(
                fileId=self.file_id,
                body=permission,
                supportsAllDrives=True,   # important for shared drives
                fields="id"
            ).execute()
            print(f"✅ Shared {self.file_id} with {email} as {role}")
            return True
        except Exception as e:
            print(f"❌ Error sharing with {email}: {e}")
            return False

    def share_with_multiple_users(self, emails: list[str], role: str = None) -> int:
        """Share file or folder with multiple users"""
        role = role or self.default_role
        print(f"Sharing {self.file_id} with multiple users...")

        success_count = 0
        for email in emails:
            if self.share_file(email.strip(), role):
                success_count += 1
            print("---")

        print(f"Successfully shared with {success_count}/{len(emails)} users")
        return success_count

    def change_file_id(self, new_file_id: str):
        """Change the file/folder ID for subsequent operations"""
        self.file_id = new_file_id
        print(f"Changed target file/folder ID to: {new_file_id}")


# # --- Usage Example ---
# if __name__ == "__main__":
#     # Simple initialization - uses .env automatically
#     google_service = GoogleService()

#     # Example: Give Content Manager (fileOrganizer) access
#     email = input("Enter your email ID: ")
#     google_service.share_file(email, role="fileOrganizer")
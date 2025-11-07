import requests
import os
from dotenv import load_dotenv

class GitHubService:
    def __init__(self):

        # Load environment variables automatically
        load_dotenv()

        GITHUB_TOKEN = os.getenv("GITHUB_ORG_TOKEN")
        ORG_NAME = os.getenv("GITHUB_ORG")

        if not GITHUB_TOKEN or not ORG_NAME:
            raise ValueError("Missing required GitHub configuration.")

        self.token = GITHUB_TOKEN
        self.org_name = ORG_NAME
        self.base_url = f"https://api.github.com/orgs/{self.org_name}/invitations"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        print("🔧 GitHub Service initialized")
        print(f"   Organization: {self.org_name}")
        print("---")

    def invite_user(self, email: str, role: str = "direct_member", team_ids: list[int] = None):
        """Invite a single user to the GitHub organization by email"""
        data = {
            "email": email,
            "role": role  # "direct_member", "admin", "billing_manager"
        }
        if team_ids:
            data["team_ids"] = team_ids

        try:
            response = requests.post(self.base_url, headers=self.headers, json=data)
            if response.status_code in (201, 202):
                print(f"✅ Invited {email} to {self.org_name} as {role}")
                return response.json()
            else:
                print(f"❌ Failed to invite {email}: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error inviting {email}: {e}")
            return None

    def invite_multiple_users(self, emails: list[str], role: str = "direct_member", team_ids: list[int] = None):
        """Invite multiple users to the GitHub organization"""
        print(f"🚀 Inviting multiple users to {self.org_name}...")

        success_count = 0
        for email in emails:
            if self.invite_user(email.strip(), role, team_ids):
                success_count += 1
            print("---")

        print(f"📊 Successfully invited {success_count}/{len(emails)} users")
        return success_count


# --- Usage Example (with .env) ---
# if __name__ == "__main__":
#     load_dotenv()

#     GITHUB_TOKEN = os.getenv("GITHUB_ORG_TOKEN")
#     ORG_NAME = os.getenv("GITHUB_ORG")
#     DEFAULT_EMAIL = os.getenv("DEFAULT_GITHUB_EMAIL")

#     github_service = GitHubService(token=GITHUB_TOKEN, org_name=ORG_NAME)

#     github_service.invite_user('sampleemail@gmail.com', role="direct_member")
    # # Invite a single user
    # if DEFAULT_EMAIL:
    #     github_service.invite_user(DEFAULT_EMAIL, role="direct_member")

    # # Invite multiple users
    # github_service.invite_multiple_users(
    #     ["user1@example.com", "user2@example.com"], role="direct_member"
    # )

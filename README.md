# Ivan Ruckhin - Access Management Tool

A Python automation tool that grants Google Drive and GitHub access to users via email.

## Prerequisites

- **Python 3.11** or higher
- A Google Cloud service account with Google Drive API enabled
- GitHub Personal Access Token (PAT) or Organization Token

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Muthu1612/ivan_ruchkin_uf.git
cd ivan_ruchkin_uf
```

### 2. Create Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv ivan_env
```

**On macOS/Linux:**
```bash
python3.11 -m venv ivan_env
```

### 3. Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
.\ivan_env\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
.\ivan_env\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
source ivan_env/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root directory with the following variables:

```properties
# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_OWNER=your_github_username

# Google Drive Configuration
GOOGLE_SERVICE_ACCOUNT_FILE=creds/prod.json
GOOGLE_FILE_ID=your_google_drive_file_id
DEFAULT_SHARE_ROLE=reader
DEFAULT_EMAIL=your_email@example.com
```

### 6. Add Google Service Account Credentials

Place your Google Cloud service account JSON file at:
```
creds/prod.json
```

## Usage

### Run the Script

```bash
python main.py
```

### Expected Behavior

1. The script prompts you to enter an email address:
   ```
   Enter your email ID: user@example.com
   ```

2. The script attempts to:
   - Grant Google Drive access to the specified email
   - Add the user as a collaborator to the GitHub repository

3. Output examples:
   ```
   ✅ Drive access given for: user@example.com
   ✅ Github access given for: user@example.com
   ```
   
   Or if there are errors:
   ```
   ❌ Failed to give Drive access for: user@example.com
   ❌ Failed to give Github access for: user@example.com
   ```

## Project Structure

```
ivan_ruckhin/
├── main.py                 # Main entry point
├── google_service.py       # Google Drive API integration
├── github_service.py       # GitHub API integration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not tracked)
├── .gitignore             # Git ignore rules
└── creds/
    └── prod.json          # Google service account key (not tracked)
```

## Troubleshooting

### Python Version Issues
Make sure you have Python 3.11 installed:
```bash
python --version
```

### Virtual Environment Not Activating
If you get an execution policy error on Windows:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Missing Dependencies
If imports fail, ensure you activated the virtual environment and ran:
```bash
pip install -r requirements.txt
```

### API Authentication Errors
- **Google Drive**: Verify `creds/prod.json` exists and contains valid credentials
- **GitHub**: Check that your `GITHUB_TOKEN` in `.env` has the necessary permissions

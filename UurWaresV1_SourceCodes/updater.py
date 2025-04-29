"""
updater.py
This script serves as the main entry point for the UurWaresv1 application. It is responsible for 
checking for updates, downloading and applying them if necessary, and then launching the login page 
of the application. The script is designed to ensure that the user always runs the latest version 
of the software.
Key Features:
- Checks the local version of the application against the latest version available on GitHub.
- Downloads and applies updates automatically if a newer version is available.
- Restarts itself after applying updates to ensure the latest code is executed.
- Launches the login page if the application is up-to-date.
Requirements:
- Python 3.13.1 or later.
- Internet access to fetch version information and updates from GitHub.
- The `requests`, `json`, `shutil`, and `zipfile` modules are used for HTTP requests, JSON parsing, 
    file operations, and handling ZIP archives, respectively.
Constants:
- `GITHUB_VERSION_URL`: URL to fetch the latest version information (version.json).
- `GITHUB_RELEASE_URL`: URL to download the latest release as a ZIP file.
- `LOCAL_VERSION_FILE`: Path to the local version.json file.
- `APP_DIRECTORY`: Directory where the application is installed.
Functions:
- `get_current_version()`: Reads and returns the current version of the application from the local 
    version.json file.
- `check_for_updates(current_version)`: Checks if a newer version is available on GitHub.
- `download_and_replace_files()`: Downloads the latest release, extracts it, and replaces the 
    existing files with the updated ones.
- `main()`: Orchestrates the update process and launches the login page if no updates are needed.
Usage:
- Run this script directly to check for updates and start the application.
- Ensure that the application directory (`APP_DIRECTORY`) has the necessary permissions for file 
    operations.
Note:
- This script is designed to be the starting point of the UurWaresv1 application.
- Make sure to configure the constants (`GITHUB_VERSION_URL`, `GITHUB_RELEASE_URL`, etc.) correctly 
    before deploying the application.
- Handle exceptions carefully to avoid breaking the update process or application startup.
Author:
- This script is part of the UurWaresv1 project and is maintained by Ugurkan Yilmaz.
"""
import os
import sys
import requests
import json
import shutil
import zipfile

GITHUB_VERSION_URL = "https://raw.githubusercontent.com/ugurkanyilmaz/UurWares/main/version.json"
GITHUB_RELEASE_URL = "https://github.com/ugurkanyilmaz/UurWaresv1/releases/download/v1.0/UurWares.zip"  # Release link
LOCAL_VERSION_FILE = os.path.join(os.getcwd(), "version.json")
APP_DIRECTORY = os.getcwd()


def get_current_version():
    try:
        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as version_file:
                version_data = json.load(version_file)
                return version_data.get("client", {}).get("version", "1")
        return "1"
    except Exception as e:
        print(f"Error - Unable to read local version: {e}")
        return "1"


def check_for_updates(current_version):
    try:
        response = requests.get(GITHUB_VERSION_URL)
        if response.status_code == 200:
            remote_version_data = response.json()
            remote_version = remote_version_data.get("client", {}).get("version", None)
            return remote_version if remote_version and remote_version != current_version else None
        print("Unable to fetch the latest version information.")
        return None
    except Exception as e:
        print(f"Version check error: {e}")
        return None


def download_and_extract_zip(url, extract_to):
    try:
        zip_path = os.path.join(extract_to, "update.zip")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(zip_path, "wb") as f:
                f.write(response.content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)

            os.remove(zip_path)
            print("Update completed successfully.")
        else:
            print(f"Failed to download the update. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error during update: {e}")


def main():
    current_version = get_current_version()
    update_version = check_for_updates(current_version)

    if update_version:
        print(f"New version {update_version} found. Updating...")
        download_and_extract_zip(GITHUB_RELEASE_URL, APP_DIRECTORY)
        os.execl(sys.executable, sys.executable, *sys.argv)  # Restart after update
    else:
        print("The latest version is already installed. Starting the login page...")
        try:
            import loginpage
            loginpage.app()
        except Exception as e:
            print(f"Failed to start the login page: {e}")
        sys.exit()


if __name__ == "__main__":
    main()


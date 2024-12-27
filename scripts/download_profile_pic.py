import requests
import os
import hashlib

def calculate_file_hash(file_path):
    """Calculate the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def download_profile_pic(username):
    # Construct the Instagram URL for the username
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    
    # Set headers to mimic a real browser (important for bypassing basic restrictions)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Referer": "https://www.instagram.com/",
        "x-ig-app-id": "936619743392459"  # App ID for Instagram's web version
    }
    
    # Ensure the folder exists
    folder_name = "profile_photo"
    os.makedirs(folder_name, exist_ok=True)
    
    try:
        # Send a GET request to the API endpoint
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch profile data. HTTP Status: {response.status_code}")
            return
        
        # Parse the JSON response to extract profile picture URL
        data = response.json()
        profile_pic_url_hd = data["data"]["user"]["profile_pic_url_hd"]
        
        # Temporary file path for the new profile picture
        temp_file_name = os.path.join(folder_name, f"{username}_temp.jpg")
        pic_response = requests.get(profile_pic_url_hd, headers=headers)
        if pic_response.status_code == 200:
            with open(temp_file_name, 'wb') as f:
                f.write(pic_response.content)
        else:
            print("Failed to download the profile picture.")
            return
        
        # Permanent file path for the stored profile picture
        file_name = os.path.join(folder_name, f"{username}_profile_pic.jpg")
        
        # Check if the new profile picture is different from the current one
        if os.path.exists(file_name):
            current_hash = calculate_file_hash(file_name)
            new_hash = calculate_file_hash(temp_file_name)
            if current_hash == new_hash:
                print(f"No changes detected for {username}'s profile picture.")
                os.remove(temp_file_name)  # Clean up the temporary file
                return
        
        # Save the new profile picture if it is different
        os.rename(temp_file_name, file_name)
        print(f"Profile picture for {username} downloaded successfully in maximum resolution!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage: Download the profile picture of the user 'rhutika_1612'
download_profile_pic('rhutika_1612')

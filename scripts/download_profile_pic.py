import instaloader
import os
import shutil
import hashlib

# Function to calculate the hash of a file
def calculate_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

# Instagram username
profile_name = "rhutika_1612"  # Replace with the target username

# File to save the previous profile picture hash
hash_file = f"{profile_name}_profile_pic_hash.txt"
existing_pic = f"{profile_name}_profile_pic.jpg"

# Initialize Instaloader
ig = instaloader.Instaloader()

# Check if the previous profile picture exists and get its hash
previous_hash = None
if os.path.exists(hash_file):
    with open(hash_file, 'r') as f:
        previous_hash = f.read().strip()

# Download the profile picture to a temporary folder
temp_folder = f"{profile_name}_temp"
ig.download_profile(profile_name, profile_pic_only=True, dirname=temp_folder)

# Find the new profile picture
new_image_path = None
for file in os.listdir(temp_folder):
    if file.endswith(".jpg"):  # Look for the profile picture
        new_image_path = os.path.join(temp_folder, file)
        break

if new_image_path:
    # Calculate hash of the new picture
    new_hash = calculate_hash(new_image_path)

    if new_hash == previous_hash:
        print("The profile picture has not changed.")
    else:
        # Save the new picture and update the hash
        shutil.move(new_image_path, existing_pic)
        print(f"New profile picture saved as {existing_pic}")

   

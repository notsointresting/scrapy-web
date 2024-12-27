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

# Initialize Instaloader
ig = instaloader.Instaloader()

# Get Instagram username
dp = 'rhutika_1612'

# File to save the previous profile picture hash
hash_file = f"{dp}_profile_pic_hash.txt"
existing_pic = f"{dp}_profile_pic.jpg"

# Check if the previous profile picture exists and get its hash
previous_hash = None
if os.path.exists(hash_file):
    with open(hash_file, 'r') as f:
        previous_hash = f.read().strip()

# Download the profile picture
folder_name = dp
ig.download_profile(dp, profile_pic_only=True)

# Find the new profile picture
new_image_path = None
for file in os.listdir(folder_name):
    if file.endswith(".jpg"):  # Look for the profile picture
        new_image_path = os.path.join(folder_name, file)
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

        # Save the new hash
        with open(hash_file, 'w') as f:
            f.write(new_hash)

# Clean up: Remove the folder
if os.path.isdir(folder_name):
    shutil.rmtree(folder_name)

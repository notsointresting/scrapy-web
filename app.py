import streamlit as st
import instaloader
import os
import hashlib
import tempfile
import shutil
import glob
from PIL import Image


def hash_file(file_path):
    """Calculate the MD5 hash of a file."""
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def remove_folder_content(folder_path):
    """Removes all files and subdirectories within a given folder."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to remove {file_path}. Reason: {e}")


def download_profile_pic_with_check(username):
    # Initialize Instaloader
    mod = instaloader.Instaloader()

    # Set up the directory and file name for the profile picture
    os.makedirs("profile_pictures", exist_ok=True)
    file_name = os.path.join("profile_pictures", f"{username}_profile_pic.jpg")

    # Check if the profile picture already exists
    if os.path.exists(file_name):
        current_hash = hash_file(file_name)
    else:
        current_hash = None

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download profile picture to temporary directory
            mod.download_profile(username, profile_pic_only=True)
            downloaded_folder = username
            image_files = glob.glob(f"{downloaded_folder}/*.jpg")
            if image_files:
                downloaded_file = image_files[0]
                # Compute hash of the new profile picture
                new_hash = hash_file(downloaded_file)
                # Compare hashes to check if the picture has changed
                if current_hash == new_hash:
                    message = "Profile picture is unchanged. No need to update."
                    remove_folder_content(downloaded_folder)
                    os.rmdir(downloaded_folder)
                    return message, file_name  # Return existing file path
                else:
                    # Save the new profile picture in the profile_pictures directory
                    shutil.move(downloaded_file, file_name)
                    message = f"Profile picture for {username} updated successfully!"
                    remove_folder_content(downloaded_folder)
                    os.rmdir(downloaded_folder)
                    return message, file_name
            else:
                message = "Profile picture could not be downloaded."
                if os.path.exists(downloaded_folder):
                  remove_folder_content(downloaded_folder)
                  os.rmdir(downloaded_folder)
                return message, None
    except Exception as e:
        message = f"An error occurred: {e}"
        return message, None


def main():
    st.title("Instagram Profile Picture Downloader")

    username = st.text_input("Enter Instagram Username:")

    if st.button("Download Profile Picture"):
        if username:
            with st.spinner("Downloading..."):
                message, image_file = download_profile_pic_with_check(username)
                st.text(message)
                if image_file:
                     try:
                        image = Image.open(image_file)
                        st.image(image, caption="Profile Picture", use_column_width=True)
                        with open(image_file, 'rb') as f:
                            st.download_button(
                            label="Download Image",
                            data=f.read(),
                            file_name=os.path.basename(image_file),
                            mime="image/jpeg"
                        )
                     except Exception as e:
                        st.error(f"Error displaying the image: {e}")
        else:
           st.warning("Please enter a username.")


if __name__ == "__main__":
    main()
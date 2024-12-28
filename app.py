import streamlit as st
import instaloader
import os
import tempfile
import glob
from PIL import Image


def download_profile_pic(username):
    """Downloads the profile picture and returns the path to the temp file."""
    mod = instaloader.Instaloader()

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download profile picture to temporary directory
            mod.download_profile(username, profile_pic_only=True)
            downloaded_folder = username
            image_files = glob.glob(f"{downloaded_folder}/*.jpg")
            if image_files:
                downloaded_file = image_files[0]
                return downloaded_file
            else:
                return None
    except Exception as e:
         print(f"An error occurred: {e}")
         return None


def main():
    st.title("Instagram Profile Picture Downloader")

    username = st.text_input("Enter Instagram Username:")

    if st.button("Download Profile Picture"):
        if username:
            with st.spinner("Downloading..."):
                image_file = download_profile_pic(username)
                if image_file:
                    try:
                        image = Image.open(image_file)
                        st.image(image, caption="Profile Picture", use_column_width=True)
                        with open(image_file, 'rb') as f:
                            st.download_button(
                                label="Download Image",
                                data=f.read(),
                                file_name=f"{username}_profile_pic.jpg",
                                mime="image/jpeg"
                            )
                    except Exception as e:
                        st.error(f"Error displaying the image: {e}")
                    finally:
                       if os.path.exists(image_file):
                            os.remove(image_file)
                            downloaded_folder = username
                            if os.path.exists(downloaded_folder):
                                os.rmdir(downloaded_folder)

                else:
                     st.error("Could not download the profile picture.")

        else:
           st.warning("Please enter a username.")


if __name__ == "__main__":
    main()
import streamlit as st
import instaloader
import os
import tempfile
import glob
from io import BytesIO
from PIL import Image


def download_profile_pic(username):
    """Downloads the profile picture and returns image data."""
    mod = instaloader.Instaloader()
    try:
      with tempfile.TemporaryDirectory() as temp_dir:
        # Download profile picture to temporary directory
            mod.download_profile(username, profile_pic_only=True)
            downloaded_folder = username
            image_files = glob.glob(f"{downloaded_folder}/*.jpg")
            if image_files:
                downloaded_file = image_files[0]
                with open(downloaded_file, "rb") as f:
                      image_data = f.read()
                os.remove(downloaded_file)
                if os.path.exists(downloaded_folder):
                  os.rmdir(downloaded_folder)
                return image_data
            else:
                if os.path.exists(downloaded_folder):
                  os.rmdir(downloaded_folder)
                print("No image files found in temporary folder.")
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
                image_data = download_profile_pic(username)
                if image_data:
                    try:
                        image = Image.open(BytesIO(image_data))
                        st.image(image, caption="Profile Picture", use_column_width=True)
                        st.download_button(
                            label="Download Image",
                            data=image_data,
                            file_name=f"{username}_profile_pic.jpg",
                            mime="image/jpeg"
                        )
                    except Exception as e:
                        st.error(f"Error displaying the image: {e}")
                else:
                     st.error("Could not download the profile picture.")
        else:
           st.warning("Please enter a username.")


if __name__ == "__main__":
    main()
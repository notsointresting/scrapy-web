from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import os

# Instagram username
profile_name = "rhutika_1612"

# Configure Selenium
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

# Open the profile page
driver.get(f"https://www.instagram.com/{profile_name}/")

# Find the profile picture
profile_pic_element = driver.find_element("xpath", "//img[contains(@class, '_6q-tv')]")
profile_pic_url = profile_pic_element.get_attribute("src")

# Download the profile picture
response = requests.get(profile_pic_url, stream=True)
if response.status_code == 200:
    with open(f"{profile_name}_profile_pic.jpg", "wb") as f:
        f.write(response.content)
    print("Profile picture downloaded successfully.")
else:
    print("Failed to download profile picture.")

driver.quit()

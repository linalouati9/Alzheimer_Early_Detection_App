from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

class DataScraper:
    def __init__(self, download_folder):
        self.download_folder = download_folder
        # Ensure the download folder exists
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
        self.driver = self.setup_driver()

    def setup_driver(self):
        """Set up the Chrome WebDriver."""
        options = webdriver.ChromeOptions()

        # Set the default download directory
        prefs = {
            "download.default_directory": self.download_folder,
        }
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        return driver

    def login(self, url, username, password, next_page):
        # Open the login page
        self.driver.get(url)
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "authModals_loginLogoutBtn"))
        )
        # Click on the  link
        login_btn = self.driver.find_element(By.ID, "authModals_loginLogoutBtn")
        login_btn.click()

        # Give the page some time to load
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "authModals_userName"))
        )

        # Find the email input field and enter the username
        email_input = self.driver.find_element(By.ID, "authModals_userName")
        email_input.clear()  # Clear any pre-filled text
        email_input.send_keys(username)

        # Find the password input field and enter the password
        password_input = self.driver.find_element(By.ID, "authModals_pswd")
        password_input.clear()  # Clear any pre-filled text
        password_input.send_keys(password)

        # Find the login button and click it
        login_button = self.driver.find_element(By.ID, "authModals_loginBtn")
        login_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, next_page))
        )

    def click_link(self, link_label):
        # Wait for the page to load after login
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, link_label))
        )
        # Click on the  link
        zero_extra_link = self.driver.find_element(By.LINK_TEXT, link_label)
        zero_extra_link.click()

    def extract_cookie(self):
        self.click_link("Control/")
        self.click_link("cookie/")
        self.download_audio_files()

    def download_audio_files(self):
        # Wait until the table is visible
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        # Find all audio download links
        audio_links = self.driver.find_elements(By.XPATH, "//tr//td[2]/a")

        # Loop through all audio links and download each file
        for link in audio_links:
            file_url = link.get_attribute("href")
            file_name = file_url.split('/')[-1].split('&')[0]  # Extract file name from URL
            link.click()
            time.sleep(1)
            print(f"Downloading {file_name} from {file_url}...")

        print(f"\nDownloaded Links {len(audio_links)}\n")

    def pipeline(self):

        login_url = "https://media.talkbank.org/dementia/English/Pitt/"
        self.login(login_url, 'yassine.labyed@fsb.ucar.tn', 'YTyU868@Ki8!qD!', "Control/")
        self.extract_cookie()

    def close(self):
        # Close the WebDriver
        self.driver.quit()

import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep



# Set up Chrome to run in a maximized window
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Set up the Selenium WebDriver with the maximized window option
driver = webdriver.Chrome(options=chrome_options)

# Read the URLs from a text file and store them in a list
with open("urls.txt", "r") as file:
    urls = file.read().splitlines()


# Define the XPaths for section 1 and section 2
section1_xpath1 = '//*[@id="container"]/div[1]/div[2]/div/div[2]/div[2]/div/div[5]/div/div/div[1]/div[1]/span[2]'
section1_xpath2 = '//*[@id="container"]/div[1]/div[2]/div/div[2]/div[2]/div/div[5]/div/div/div[1]/div[2]/div[2]/a'
section2_xpath1 = '//*[@id="container"]/div[1]/div[2]/div/div[2]/div[2]/div/div[5]/div/div/div[2]/div[1]/span[2]'
section2_xpath2 = '//*[@id="container"]/div[1]/div[2]/div/div[2]/div[2]/div/div[5]/div/div/div[2]/div[2]/div[2]/a'
section3_xpath1 = '//*[@id="container"]/div/div[2]/div/div[2]/div[2]/div/div[5]/div/div/div/div[1]/span[2]'
section3_xpath2 = '//*[@id="container"]/div/div[2]/div/div[2]/div[2]/div/div[5]/div/div/div/div[2]/div[2]/a'


# Create a directory to save downloaded content
download_dir = "downloaded_content"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)


opened_links = []
downloadFound = False



# Iterate through the list of URLs
for url in urls:
    downloadFound = False
    # Open the URL in the browser
    driver.get(url)

    # Wait for the page to load (you might need to adjust the wait time)
    driver.implicitly_wait(500)
    sleep(1)
    while (downloadFound == False):
        # Check section 1
        span_elements_section1 = driver.find_elements(By.XPATH, section1_xpath1)
        link_elements_section1 = driver.find_elements(By.XPATH, section1_xpath2)

        if span_elements_section1:
            if "Windows" in span_elements_section1[0].text:
                if link_elements_section1:
                    section1_href = link_elements_section1[0].get_attribute("href")
                    print(section1_href)
                    opened_links.append(section1_href)
                    downloadFound = True
                    break
        if not span_elements_section1:
            continue

        # Check section 2
        span_elements_section2 = driver.find_elements(By.XPATH, section2_xpath1)
        link_elements_section2 = driver.find_elements(By.XPATH, section2_xpath2)

        if span_elements_section2:
            if "Windows" in span_elements_section2[0].text:
                if link_elements_section2:
                    section2_href = link_elements_section2[0].get_attribute("href")
                    print(section2_href)
                    opened_links.append(section2_href)
                    downloadFound = True
                    break
        if not span_elements_section2:
            continue

        span_elements_section3 = driver.find_elements(By.XPATH, section3_xpath1)
        link_elements_section3 = driver.find_elements(By.XPATH, section3_xpath2)

        if span_elements_section3:
            if "Windows" in span_elements_section3[0].text:
                if link_elements_section3:
                        section3_href = link_elements_section3[0].get_attribute("href")
                        print(section3_href)
                        opened_links.append(section3_href)
                        downloadFound = True
                        break
        if not span_elements_section3:
            continue


driver.quit()
print("--------------OPENING HREFS----------------------")


def download_and_save(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Append ".zip" extension to the filename
            filename = save_path + ".zip"
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print(f"Download from {url} completed. File saved as '{filename}'.")
        else:
            print(f"Failed to download from {url} (Status Code: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading from {url}: {e}")

# Iterate through the list of URLs and download
for href in opened_links:
    # Use a specific filename for each URL, e.g., based on index or a custom name
    download_and_save(href, f"downloaded_file_{opened_links.index(href)}")

print("All downloads have completed.")
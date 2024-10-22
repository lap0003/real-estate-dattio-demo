#!/Users/lynn/venv/bin/python

import time
import random
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Safari WebDriver
driver = webdriver.Safari()

# The base URL of the listings page
base_url = "https://www.plusvalia.com/departamentos-en-alquiler-en-quito-pagina-{}.html"
page_number = 1
max_pages = 20  # Set a maximum number of pages to scrape for safety

listings_data = []

while page_number <= max_pages:
    try:
        # Construct the URL for the current page
        current_url = base_url.format(page_number)
        driver.get(current_url)

        # Wait for the page content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.egwEUc a"))
        )
        time.sleep(random.uniform(2, 5))  # Random delay between 2 and 5 seconds

        # Extract listing URLs
        listings = driver.find_elements(By.CSS_SELECTOR, 'div.egwEUc a')
        scraped_urls = []
        for listing in listings:
            listing_url = listing.get_attribute('href')
            if listing_url not in listings_data:  # Avoid duplicates
                listings_data.append(listing_url)
                scraped_urls.append(listing_url)

        # Log the number of URLs scraped from the current page
        print(f"Page {page_number}: Scraped {len(scraped_urls)} URLs")

        page_number += 1  # Increment to the next page

    except Exception as e:
        print(f"An error occurred while scraping page {page_number}: {e}")
        break

# After collecting URLs, now visit each listing to scrape details
final_data = []

for index, url in enumerate(listings_data, start=1):
    driver.get(url)

    # Wait for the listing details to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.Price-sc-12dh9kl-3"))
    )
    time.sleep(random.uniform(2, 5))  # Random delay between 2 and 5 seconds

    # Scrape the listing details using Selenium
    try:
        precio = driver.find_element(By.CSS_SELECTOR, 'div.Price-sc-12dh9kl-3').text
    except Exception:
        precio = False

    try:
        area = driver.find_element(By.CSS_SELECTOR, '.PostingMainFeaturesBlock-sc-1uhtbxc-0 span:nth-of-type(1)').text
    except Exception:
        area = False

    try:
        habitaciones = driver.find_element(By.CSS_SELECTOR, 'span:nth-of-type(2)').text
    except Exception:
        habitaciones = False

    try:
        baños = driver.find_element(By.CSS_SELECTOR, 'span:nth-of-type(3)').text
    except Exception:
        baños = False

    try:
        estacionamiento = driver.find_element(By.CSS_SELECTOR, 'span:nth-of-type(4)').text
    except Exception:
        estacionamiento = False

    try:
        ubicacion = driver.find_element(By.CSS_SELECTOR, 'div.PostingCardRow-sc-i1odl-5.gJKAik > div > h2').text
    except Exception:
        ubicacion = False

    try:
        imgURL = driver.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
    except Exception:
        imgURL = False

    # Store the scraped data
    data = {
        'url': url,
        'precio': precio,
        'area': area,
        'habitaciones': habitaciones,
        'baños': baños,
        'estacionamiento': estacionamiento,
        'ubicacion': ubicacion,
        'imgURL': imgURL,
    }

    final_data.append(data)
    print(f"Scraped {index}/{len(listings_data)} listings.")

# Save the scraped data to a CSV file
csv_file = 'listings.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=final_data[0].keys())
    writer.writeheader()
    writer.writerows(final_data)

# Close the WebDriver
driver.quit()

print(f"Scraping completed. Data saved to {csv_file}.")



import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    # Get credentials from environment
    USER = os.environ.get("SAQ_USERNAME")
    PASS = os.environ.get("SAQ_PASSWORD")

    if not USER or not PASS:
        raise Exception("Missing SAQ_USERNAME or SAQ_PASSWORD environment variable")

    # Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://www.saq-b2b.com/")

        # Login
        driver.find_element(By.NAME, "Session_Username").send_keys(USER)
        driver.find_element(By.NAME, "Session_Password").send_keys(PASS)
        driver.find_element(By.CSS_SELECTOR, "input[type=submit]").click()

        wait.until(lambda d: d.current_url != "https://www.saq-b2b.com/")

        # Go to Reports page
        driver.get("https://www.saq-b2b.com/wxic/fr/Report.Selection$Prep")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "reportsTable")))

        # Collect Sales Summary URL
        sales_link = driver.find_element(By.XPATH, "//table[contains(@class,'reportsTable')][1]//tr[3]/td[3]/a")
        urls = [sales_link.get_attribute("href")]

        # Collect Raw Data URLs
        raw_links = driver.find_elements(By.XPATH, "//table[contains(@class,'reportsTable')][2]//tr/td[3]/a")
        urls += [a.get_attribute("href") for a in raw_links]

        # Output as JSON
        print(json.dumps({"urls": urls}))

    finally:
        driver.quit()


if __name__ == "__main__":
    main()

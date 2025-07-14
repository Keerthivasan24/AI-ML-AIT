import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)


url = "https://hcfl.gov/government/board-of-county-commissioners/board-of-county-commissioners-policies"
driver.get(url)

os.makedirs("downloaded_pdfs", exist_ok=True)

for page in range(3):
    print(f"\nScraping Page {page + 1}...")

    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href$='.pdf']")))
        time.sleep(2)

   
        pdf_links = driver.find_elements(By.CSS_SELECTOR, "a[href$='.pdf']")
        for link in pdf_links:
            href = link.get_attribute("href")
            filename = href.split("/")[-1].split("?")[0]
            filepath = os.path.join("downloaded_pdfs", filename)

            if not os.path.exists(filepath):
                try:
                    res = requests.get(href)
                    with open(filepath, "wb") as f:
                        f.write(res.content)
                    print(f"Downloaded: {filename}")
                except Exception as err:
                    print(f" Failed to download {filename}: {err}")

        # Next page click
        next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Next page']")))
        if next_btn.get_attribute("aria-disabled") == "true":
            print(" Reached end of pagination.")
            break

        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(3)

    except Exception as e:
        print(f" Error on page {page + 1}: {e}")
        break

driver.quit()

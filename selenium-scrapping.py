from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os


def extract_specs(driver, link):
    try:
        driver.get(link)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "feature-bullets"))
        )
        bullets = driver.find_elements(By.CSS_SELECTOR, "#feature-bullets ul li span")
        specs = [b.text.strip() for b in bullets if b.text.strip()]
        driver.back()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot.s-result-list"))
        )
        return " | ".join(specs)
    except Exception as e:
        print(f"Spec extraction failed for {link}: {e}")
        try:
            driver.back()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot.s-result-list"))
            )
        except:
            pass
        return "N/A"


search_query = input("Enter the product to search on Amazon: ")


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.amazon.in")


search_box = driver.find_element(By.ID, "twotabsearchtextbox")
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

products = []

for page in range(1,2):
    try:
        print(f"\nScraping page {page}...")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot.s-result-list"))
        )

        items = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']")

        for i in range(len(items)):
  
            items = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']")
            item = items[i]

            try:
                title = item.find_element(By.CSS_SELECTOR, "h2 span").text
            except:
                title = "N/A"

            try:
                link_elem = item.find_element(By.CSS_SELECTOR, "a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
                relative_url = link_elem.get_attribute("href")
                link = "https://www.amazon.in" + relative_url if relative_url.startswith("/") else relative_url
            except:
                link = "N/A"

            try:
                price = item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
            except:
                price = "N/A"

            specs = extract_specs(driver, link) if link != "N/A" else "N/A"

            products.append({
                "Title": title,
                "Price": price,
                "Link": link,
                "Specs": specs
            })


        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.s-pagination-next"))
        )
        next_button.click()
        time.sleep(2)

    except Exception as e:
        print(f"Stopping at page {page} due to error: {e}")
        break

driver.quit()


df = pd.DataFrame(products)
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop_path, "amazon_products.csv")
df.to_csv(output_file, index=False)
print(f"\nScraping completed. Data saved to {output_file}")

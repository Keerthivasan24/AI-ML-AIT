from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


driver.get("https://www.tutorialspoint.com/selenium/practice/accordion.php")


WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "accordion-item"))
)


accordion_items = driver.find_elements(By.CLASS_NAME, "accordion-item")

data = []


for item in accordion_items:
    try:

        header = item.find_element(By.CLASS_NAME, "accordion-header").text

        button = item.find_element(By.CLASS_NAME, "accordion-button")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(0.5) 


        body = item.find_element(By.CLASS_NAME, "accordion-body").text

        data.append({
            "Title": header,
            "Content": body
        })

    except Exception as e:
        print(f"Error while scraping: {e}")


driver.quit()


df = pd.DataFrame(data)
df.to_csv("accordion_content.csv", index=False)
print("Data saved to accordion_content.csv")

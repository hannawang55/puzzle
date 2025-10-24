from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import openpyxl

chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service("/usr/local/bin/chromedriver")  
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://idtoolkit.com")

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Generated IDs"
ws.append(["Natural Number", "Generated ID"])

for i in range(1, 101): 
    try:
        input_box = driver.find_element(By.ID, "generate-input")
        input_box.clear()
        input_box.send_keys(str(i))


        generate_button = driver.find_element(By.ID, "generate-button")  
        generate_button.click()

        time.sleep(0.5)  

        result_box = driver.find_element(By.ID, "generate-result")
        generated_id = result_box.text.strip()


        ws.append([i, generated_id])
    except Exception as e:
        ws.append([i, f"Error: {e}"])

wb.save("generated_ids_from_web.xlsx")
driver.quit()

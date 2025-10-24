from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import openpyxl

# 设置 Chrome 驱动路径（请根据你的系统调整）
chrome_options = Options()
chrome_options.add_argument("--headless")  # 可选：无界面运行
service = Service("/usr/local/bin/chromedriver")  # 替换为你的 chromedriver 路径
driver = webdriver.Chrome(service=service, options=chrome_options)

# 打开 ID Toolkit 网页
driver.get("https://idtoolkit.com")  # 请确认这是你打开的网页地址

# 创建 Excel 文件
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Generated IDs"
ws.append(["Natural Number", "Generated ID"])

# 输入自然数范围
for i in range(1, 101):  # 可修改范围
    try:
        # 找到输入框并输入自然数
        input_box = driver.find_element(By.ID, "generate-input")  # 替换为实际 ID
        input_box.clear()
        input_box.send_keys(str(i))

        # 点击生成按钮
        generate_button = driver.find_element(By.ID, "generate-button")  # 替换为实际 ID
        generate_button.click()

        time.sleep(0.5)  # 等待结果加载

        # 获取生成的 ID
        result_box = driver.find_element(By.ID, "generate-result")  # 替换为实际 ID
        generated_id = result_box.text.strip()

        # 写入 Excel
        ws.append([i, generated_id])
    except Exception as e:
        ws.append([i, f"Error: {e}"])

# 保存文件
wb.save("generated_ids_from_web.xlsx")
driver.quit()
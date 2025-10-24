from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=options)

# 读取 Excel 文件中的受试者编号
df = pd.read_excel("quota_ids.xlsx", sheet_name="in", engine="openpyxl")
ids = df["quota_id"].tolist()

# 设置浏览器驱动（确保 chromedriver 在系统路径中）
driver = webdriver.Chrome()

# 打开验证网页
driver.get("https://158.247.250.232:8504/")
PASSWORD = "xrao-buyao-gaosu-qitaren-aaa"

# 登录步骤
driver.find_element(By.ID, "text_input_1").send_keys(PASSWORD)
driver.find_element(By.XPATH, "//div[@data-testid='stMarkdownContainer']//p[text()='Sign in']").click
time.sleep(2)  # 等待登录完成

results = []

# 遍历每个受试者编号进行验证
for id_str in ids:
    try:
        # 输入编号
        input_box = driver.find_element(By.ID, "text_input_4")
        input_box.clear()
        input_box.send_keys(id_str)

        # 点击验证按钮
        validate_div = driver.find_element(By.XPATH, "//div[@data-testid='stMarkdownContainer' and .//p[text()='Validate']]")
        validate_div.click()
        time.sleep(1)  # 等待结果显示




        # 获取验证结果文本
        result_text = driver.find_element(By.XPATH, "//div[@data-testid='stMarkdownContainer' and .//p[text()='valid id']]").text
        print(f"{id_str} 验证结果：{result_text}")

        # 判断验证结果
        if "Valid ID✅" in result_text:
            results.append({"quota_id": id_str, "is_valid": True})
        elif "Invalid ID❌" in result_text:
            results.append({"quota_id": id_str, "is_valid": False})
        else:
            results.append({"quota_id": id_str, "is_valid": "Unknown"})
    except Exception as e:
        print(f"验证失败：{id_str}，错误：{e}")
        results.append({"quota_id": id_str, "is_valid": "Error"})

# 保存验证结果到下载文件夹
download_path = os.path.expanduser("~/Downloads/validated_ids.xlsx")
pd.DataFrame(results).to_excel(download_path, index=False)
print("验证结果已保存到:", download_path)

print("当前页面URL:", driver.current_url)
print("页面标题:", driver.title)

# 关闭浏览器
driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# 设置 Edge WebDriver 路径
edge_driver_path = r'D:\edgedriver_win64\msedgedriver.exe' # 这里填入自己的Edge驱动程序路径

# 启动 Edge 浏览器
service = Service(edge_driver_path)
options = webdriver.EdgeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")  # 禁用自动化控制特征
driver = webdriver.Edge(service=service, options=options)

# 修改webdriver属性
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# 打开问卷页面
driver.get('https://www.wjx.cn/vm/h4Ck0yh.aspx#')

# 配置参数
MAX_WAIT_TIME = 3600 # 这里设置运行时长
REFRESH_INTERVAL = 0 # 这里设置刷新间隔

YOUR_NAME = 'aaa' # 这里填入姓名
YOUR_QQ = '111' # 这里填入QQ号
YOUR_ID = '111' # 这里填入学号
YOUR_NUMBER = '111' # 这里填入电话
YOUR_GENDER = '男'  # 这里填入性别，或 '女'

# 记录时间
start_time = time.time()

try:
    while True:
        if time.time() - start_time > MAX_WAIT_TIME:
            print("超时退出")
            break

        try:
            # 定义字段及其可能的关键词（用 | 分隔）
            fields = [
                ("学号", YOUR_ID),
                ("姓名", YOUR_NAME),
                ("电话|联系方式|手机号", YOUR_NUMBER)
                # ("qq|QQ", YOUR_QQ)
            ]

            # 选择性别（不依赖 class）
            try:
                gender_label = WebDriverWait(driver, REFRESH_INTERVAL).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '性别')]")))
                print("找到性别问题")
                try:
                    if YOUR_GENDER == '男':
                        text_element = gender_label.find_element(By.XPATH, ".//following::div[text()='男']")
                    elif YOUR_GENDER == '女':
                        text_element = gender_label.find_element(By.XPATH, ".//following::div[text()='女']")

                    clickable_element = text_element.find_element(By.XPATH, "./preceding-sibling::span//a")
                    driver.execute_script("arguments[0].click();", clickable_element)
                    print(f"已选择性别：{YOUR_GENDER}")
                except:
                    print(f"未找到男女选项跳过")

            except Exception as e:
                print(f"选择性别失败: {str(e)}")

            # 填写所有字段
            for field_keywords, value in fields:
                try:
                    keywords = field_keywords.split("|")
                    xpath_conditions = " or ".join([f"contains(text(), '{kw}')" for kw in keywords])
                    input_element = WebDriverWait(driver, REFRESH_INTERVAL).until(
                        EC.presence_of_element_located((By.XPATH, f"//*[{xpath_conditions}]/following::input[1]")))
                    input_element.send_keys(value)
                    print(f"已填写 {keywords[0]}")
                except:
                    print(f"未找到 {keywords} 输入框，跳过")

            # 提交问卷
            submit_button = WebDriverWait(driver, REFRESH_INTERVAL).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='提交']")))
            submit_button.click()
            print("已提交问卷")

            try:
                verify_button = WebDriverWait(driver, REFRESH_INTERVAL).until(
                    EC.element_to_be_clickable((By.ID, "SM_BTN_1"))
                )
                verify_button.click()
                print("验证已完成！")
            except Exception as e:
                print(f"未检测到验证按钮或验证失败: {e}")

            break
        except:
            print("刷新重试...")
            driver.refresh()
            time.sleep(REFRESH_INTERVAL)

except Exception as e:
    print(f"运行失败: {str(e)}")

finally:
    time.sleep(10000)
    driver.quit()

    print("浏览器已关闭")

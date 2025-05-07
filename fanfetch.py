from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.chromium.options import ChromiumOptions
from urllib import parse
import time
import pandas as pd
import logging
logging.basicConfig(filename='error.log', level=logging.ERROR)
fandict = {}
uidin = input("请输入需要查询的UID：")
if (not uidin.isdigit()) or (int(uidin) <= 0):
    print("输入的UID格式不合法！将以1为UID默认值")
    uidin = "1"
page = "https://music.163.com/#/user/fans?id=" + uidin
ser = ChromiumService()
ser.path = "/usr/bin/chromedriver"
options = ChromiumOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=ser, options=options)
driver.get(page)
def save_fandata(dictionary):
    uid,fname,num = [],[],[]
    fandf = pd.DataFrame()
    try:
        for elements in dictionary:
            uid.append(elements)
            fname.append(dictionary[elements])
        num = [str(i) for i in range(1, len(uid) + 1)]
        fandf = pd.DataFrame({
            '编号': num,
            'UID': uid,
            '昵称': fname
        })
        fandf.to_csv('fandata.csv',encoding='utf8',index=False)
        print("保存成功！请在py文件目录中寻找fandata.csv")
    except Exception as e:
        print(f"运行过程中出错: {e}")
def findfans():
    for fn in driver.find_elements(By.CSS_SELECTOR,".s-fc7.f-fs1.nm.f-thide"):
        link = fn.get_attribute('href')
        parselink = parse.urlparse(link)
        uid = parse.parse_qs(parselink.query).get('id', ['未知UID'])[0]
        fandict[uid] = fn.text
try:
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it("contentFrame")
    )
    fancount_span = driver.find_element(By.ID,"fan_count_down")
    fancount = int(fancount_span.text.split()[0])
    print("粉丝总数：",fancount)
    fanpagen = min(fancount // 20 + (1 if fancount % 20 != 0 else 0), 50)
    print("预计获取页数：",fanpagen)
    i = 1
    print(f"正在获取第{i}页......")
    findfans()
    for i in range(1,fanpagen):
        button = driver.find_element(By.CSS_SELECTOR,".zbtn.znxt")
        driver.execute_script("arguments[0].click()",button)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".s-fc7.f-fs1.nm.f-thide"))
        )
        print(f"正在获取第{i+1}页......")
        findfans()
        i = i + 1
except Exception as e:
    print(f"运行过程中出错: {e}")
finally:
    save_fandata(fandict)
    driver.quit()

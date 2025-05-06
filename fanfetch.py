from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chromium.service import ChromiumService
from urllib import parse
page = "https://music.163.com/#/user/fans?id=1"
fandict = {}
ser = ChromiumService()
ser.path = "/usr/bin/chromedriver"
driver = webdriver.Chrome(service=ser)
driver.get(page)
try:
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it("contentFrame")
    )
    fancount_span = driver.find_element(By.ID,"fan_count_down")
    fancount = int(fancount_span.text.split()[0])
    print(fancount)
    for fn in driver.find_elements(By.CSS_SELECTOR,".s-fc7.f-fs1.nm.f-thide"):
        link = fn.get_attribute('href')
        parselink = parse.urlparse(link)
        uid = parse.parse_qs(parselink.query).get('id')[0]
        fandict[uid] = fn.text
    print(fandict)
except Exception as e:
    print(f"运行过程中出错: {e}")
finally:
    driver.quit()

import re
import time

from selenium.webdriver import Keys

from selenium.webdriver.common.by import By
import undetected_chromedriver
from sqlalchemy import create_engine, insert
from models import Laptops, metadata

from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

driver = undetected_chromedriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))

engine = create_engine('postgresql://postgres:postgres@localhost/homework_2')
metadata.create_all(engine)
conn = engine.connect()
ins = insert(Laptops)

for page in range(1, 51):
    start_url = "https://www.computeruniverse.net/ru/c/noutbuki-planshety-i-pk/noutbuki?page=" + str(page)
    driver.get(start_url)
    driver.maximize_window()
    time.sleep(5)

    tables = driver.find_elements(By.CLASS_NAME, "ProductListItemRow_product__zBkg9")
    i = 1
    for table in tables:

        div = table.find_elements(By.TAG_NAME, "div")
        url = table.find_element(By.TAG_NAME, "a").get_attribute("href")
        product_name = div[0].find_element(By.TAG_NAME, "a").text
        cpu_xpath = f"/html/body/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]/div[8]/div/ul/li[{i}]/div/div[3]/div[1]/ul/li[3]"
        gb_xpath = f"/html/body/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]/div[8]/div/ul/li[{i}]/div/div[3]/div[1]/ul/li[5]"
        price_xpath = f"/html/body/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]/div[8]/div/ul/li[{i}]/div/div[3]/div[2]"
        try:
            cpu_hhz = float(re.findall(r"\d+[.]\d+", driver.find_element(By.XPATH, cpu_xpath).text)[0])
        except IndexError:
            i += 1
            continue
        else:
            i = i

        try:
            ram_gb = int(re.findall(r"\d+", driver.find_element(By.XPATH, gb_xpath).text)[0])
        except IndexError:
            i += 1
            continue
        else:
            i = i

        try:
            ssd_gb = int(re.findall(r"\d+", driver.find_element(By.XPATH, gb_xpath).text)[1])
        except IndexError:
            i += 1
            continue
        else:
            i = i

        if ssd_gb == 1 or ssd_gb == 2:
            ssd_gb = ssd_gb*1024
        else:
            ssd_gb

        try:
            price = int((re.findall(r"\d+[ ]\d+", driver.find_element(By.XPATH, price_xpath).text)[0]).replace(" ", ""))
        except IndexError:
            i += 1
            continue
        else:
            i = i

        rank = round((cpu_hhz*5.7 + ram_gb*6.2 + ssd_gb*1.4 +price*(-0.0003)), 2)

        print(url, "|", product_name, "|", cpu_hhz, "|", ram_gb, "|", ssd_gb, "|", price, "|", rank)
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        i += 1
        conn.execute(ins,
                     url=url,
                     product_name=product_name,
                     cpu_hhz=cpu_hhz,
                     ram_gb=ram_gb,
                     ssd_gb=ssd_gb,
                     price=price,
                     rank=rank
                     )
driver.close()
import re
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from sqlalchemy import create_engine, insert
from models import Laptops, metadata

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

engine = create_engine('postgresql://postgres:postgres@localhost/homework_2')
metadata.create_all(engine)
conn = engine.connect()
ins = insert(Laptops)

firefox_options = Options()

for page in range(1, 3):
    start_url = "https://www.notik.ru/search_catalog/filter/work.htm?page=" + str(page)
    driver.get(start_url)
    time.sleep(3)

    tables = driver.find_elements(By.CLASS_NAME, "goods-list-table")

    for table in tables:
        td = table.find_elements(By.TAG_NAME, "td")

        url = table.find_element(By.TAG_NAME, "a").get_attribute("href")
        product_name = td[7].find_element(By.TAG_NAME, "a").get_attribute('ecname')
        cpu_hhz = (float(re.findall(r"\d+", td[1].text)[-1]))/1000
        print(cpu_hhz)
        ram_gb = int(re.findall(r"\d+", td[2].text)[0])
        ssd_gb = int(re.findall(r"\d+", td[2].text)[-1])
        price = int("".join(re.findall(r"\d+", td[7].text)[-2:]))
        rank = round((cpu_hhz*5.7 + ram_gb*6.2 + ssd_gb*1.4 +price*(-0.0003)), 2)
        print(url, "|", product_name, "|", cpu_hhz, "|", ram_gb, "|", ssd_gb, "|", price, "|", rank)
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

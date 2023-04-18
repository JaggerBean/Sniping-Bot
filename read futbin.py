
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import bs4
import requests

options = Options()
options.page_load_strategy = 'eager'
options.add_argument('--enable-extensions')
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_extension(r'C:\Users\Jagge_vbl7d7m\PycharmProjects\pythonProject\extension_5_4_1_0.crx')
options.add_argument("disable-infobars")

driver_path = r'C:\cmder\bin\chromedriver.exe'
service = Service(executable_path=driver_path)
# driver = webdriver.Chrome(service=service)


# for page in range(1):
#     print(f"loop {page}")
#     page_url = 'https://www.futbin.com/players?page='+str(page)
#     driver.get(page_url)
#     player_elements = driver.find_elements(By.CSS_SELECTOR, 'tr[data-url]')
#     # print(player_elements)
#     for player_element in player_elements:
#         player_data = player_element.get_attribute('data-url')
#         print(player_data)
#
# page_url = 'https://www.futbin.com/players?page=1'
# driver.get(page_url)
# driver.quit()
# time.sleep(5)
#
# page_url = 'https://www.futbin.com/players?page=2'
# driver.get(page_url)


# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium import webdriver
#
# # specify the location of the geckodriver executable
# driver_path = r'C:\Users\Jagge_vbl7d7m\PycharmProjects\pythonProject\geckodriver.exe'
#
# # specify the location of the Firefox binary
# firefox_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
#
# # create a Firefox options object
# firefox_options = Options()
#
# # set the path to the Firefox binary
# firefox_options.binary_location = firefox_binary_path
#
# # create a Firefox service object
# service = Service(executable_path=driver_path)

# create a Firefox webdriver instance
# driver = webdriver.Firefox(service=service, options=firefox_options)

# navigate to a webpage


# with open ('player_futbin_data.txt', 'w') as f:
#     for page in range(1, 689):
#         finished = 0
#
#         wait = WebDriverWait(driver, 5)
#         driver.set_page_load_timeout(15)
#         page_url = 'https://www.futbin.com/players?page=' + str(page)
#         driver.get(page_url)
#         time.sleep(3)
#         source = driver.page_source
#         #         time.sleep(15)
#         #         is_it_there = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr[data-url]')))
#         #         finished = 1
#         #     except:
#         #         driver.quit()
#         #         time.sleep(5)
#         # print(f"loop {page}")
#         # player_elements = driver.find_elements(By.CSS_SELECTOR, 'tr[data-url]')
#
#         # print(player_elements)
#         for line in source.splitlines():
#             print(line)
#             # f.write(player_data + '\n' + icon_text + '\n\n')
#         driver.quit()
#         time.sleep(1)

# driver = webdriver.Firefox(service=service)
# with open ('player_futbin_data.txt', 'w') as f:
#     for page in range(1, 689):
#         finished = 0
#         print(f'page: {page}')
#         print(finished)
#         while finished == 0:
#             try:
#                 print('1')
#
#                 print('2')
#                 wait = WebDriverWait(driver, 5)
#                 print('3')
#                 driver.set_page_load_timeout(15)
#                 print('4')
#                 page_url = 'https://www.futbin.com/players?page=' + str(page)
#                 print("opening page")
#                 driver.get(page_url)
#                 time.sleep(10)
#                 is_it_there = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr[data-url]')))
#                 finished = 1
#             except:
#                 driver.quit()
#                 time.sleep(5)
#                 driver = webdriver.Firefox(service=service)
#         print(f"loop {page}")
#         player_elements = driver.find_elements(By.CSS_SELECTOR, 'tr[data-url]')
#
#         # print(player_elements)
#         for player_element in player_elements:
#             player_data = player_element.get_attribute('data-url')
#             print(player_data)
#             icon_element = player_element.find_element(By.CSS_SELECTOR, '.mobile-hide-table-col div')
#             icon_text = icon_element.text
#             print(icon_text)
#             # f.write(player_data + '\n' + icon_text + '\n\n')
#         driver.quit()
#         time.sleep(1)


# driver = webdriver.Chrome(service=service, options=options)
# wait = WebDriverWait(driver, 5)
# driver.set_page_load_timeout(30)
#
# page_url = 'https://www.futbin.com/players?page=' + str(1)
# driver.get(page_url)
# time.sleep(5)
# pya.press('F12')
# time.sleep(0.5)
# pya.click(955,155)
# time.sleep(500)



with open ('player_futbin_data.txt', 'a') as f:
    for page in range(64, 689):
        finished = 0

        while finished == 0:
            try:
                driver = webdriver.Chrome(service=service, options=options)
                wait = WebDriverWait(driver, 5)
                driver.set_page_load_timeout(15)
                page_url = 'https://www.futbin.com/players?page=' + str(page)
                driver.get(page_url)
                time.sleep(5)
                is_it_there = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr[data-url]')))
                finished = 1
            except Exception as e:
                driver.quit()
                time.sleep(5)
                print(e)
        print(f"loop {page}")
        player_elements = driver.find_elements(By.CSS_SELECTOR, 'tr[data-url]')

        # print(player_elements)
        for player_element in player_elements:
            player_data = player_element.get_attribute('data-url')
            print(player_data)
            icon_element = player_element.find_element(By.CSS_SELECTOR, '.mobile-hide-table-col div')
            icon_text = icon_element.text
            print(icon_text)
            f.write(player_data + '\n' + icon_text + '\n\n')
        driver.quit()
        time.sleep(1)

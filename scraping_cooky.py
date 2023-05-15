# pylint: disable=W0702
# pylint: disable=C0301
# pylint: disable=C0103

import time
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from config import DatabaseConnection, FoodCategory

# Set timeout for webpage
WEBPAGE_TIMEOUT = 10

page_dir = os.path.dirname(os.path.realpath(
    __file__)) + os.sep + 'offline_pages\\cooky'
# Download webpages
# remove dir
# if os.path.exists(page_dir):
# shutil.rmtree(page_dir)
# create dir if not exists
if not os.path.exists(page_dir):
    os.makedirs(page_dir)

firefox_options = Options()
firefox_options.headless = True
firefox_options.set_preference("privacy.trackingprotection.enabled", True)
firefox_options.set_preference("browser.download.dir", page_dir)
firefox_options.set_preference("browser.download.folderList", 2)
firefox_options.set_preference("browser.warnOnQuit", False)
firefox_options.set_capability("pageLoadStrategy", "none")

# Initialize a Firefox webdriver
driver = webdriver.Firefox(options=firefox_options)
# driver = webdriver.Firefox()

# Grab the web page
# driver.get("https://www.cooky.vn/cach-lam/thuc-uong-c7")
driver.get("https://www.cooky.vn/cach-lam/")

# Category dictionary
xpath = {
    'Thực đơn': '/html/body/div[10]/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div',
    # 'Loại món': '/html/body/div[10]/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div[2]/div',
    # 'Nguyên liệu': '/html/body/div[10]/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div',
    # 'Độ khó': '/html/body/div[10]/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div[4]/div',
    # 'Ẩm thực': '/html/body/div[10]/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div[6]/div',
    # 'Cách thực hiện': '/html/body/div[10]/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div[7]/div'
}

# # wait until red_span and gray_span are loaded
# WebDriverWait(driver, 10).until(EC.presence_of_element_located(
#     (By.XPATH, "//span[@class='text-red ng-binding']")))
time.sleep(5)

# create an empty dict to store the mapping between submenu_text and food_id
submenu_dict = {}
# create a set to keep track of food_ids that have already been added to the submenu_dict
food_id_set = set()

# Connection to DB
db = DatabaseConnection("Food-RS-0")
conn = db.connection
cur = conn.cursor()

for parent_name, xpath_value in xpath.items():
    food_categories = ['Thức uống']
    gray_span = driver.find_element(
        By.XPATH, "//strong[@class='text-highlight ng-binding']")
    gray_text = gray_span.text
    gray_num = int(re.findall('\d+', gray_text)[0])
    print(gray_num)
    parent_id = int(
        ((xpath_value.split('/')[13]).replace('div', '')).replace('[', '').replace(']', ''))

    wait = WebDriverWait(driver, WEBPAGE_TIMEOUT)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_value)))
    element.click()
    print(f"{parent_name}")
    count = 0
    submenus = driver.find_elements(
        By.XPATH, '//span[@class="fa text-gray fa-square-o"]')
    for submenu in submenus:
        submenu.click()
        count += 1
        # extract the value from span element
        selected_submenu = driver.find_element(
            By.XPATH, '//span[@class="fa text-gray fa-check-square text-highlight"]/following-sibling::span[@class="ng-binding"]')
        submenu_text = selected_submenu.text
        # restrict conditions to  only those submenus that are or aren't in the food_categories list
        if submenu_text in food_categories:
            submenu_dict[submenu_text] = []
            print(f"  checked {submenu_text}")

        # if there is something to load, then load more
            red_span = driver.find_element(
                By.XPATH, "//span[@class='text-red ng-binding']")
            gray_span = driver.find_element(
                By.XPATH, "//strong[@class='text-highlight ng-binding']")

            red_text = red_span.text
            gray_text = gray_span.text

            # Extract the numbers from the text using regular expressions
            red_num = int(re.findall('\d+', red_text)[0])
            gray_num = int(re.findall('\d+', gray_text)[0])

            # Click the "Xem thêm" button repeatedly until there are no more recipes to load
            try:
                while True:
                    # print(f"{red_num}/{gray_num}")
                    load_more_button = WebDriverWait(driver, WEBPAGE_TIMEOUT).until(EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/div[10]/div/div[1]/div/div/div/div/div[4]/div[4]/div/a/span[1]')))
                    load_more_button.click()
            except:
                # Wait for the page to load and extract the new recipe links
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                # recipe_link as a set
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    if href.startswith('/cong-thuc'):
                        food_id = int(''.join(filter(str.isdigit, href)))
                        # add mapping to the dict only if the food_id is not already in the set
                        if food_id not in food_id_set:
                            # add the mapping to the food_id_dict
                            submenu_dict[submenu_text].append(food_id)
                            food_id_set.add(food_id)
                            # print(food_id)

                # create a list of FoodCategory objects
            for submenu_text, food_ids in submenu_dict.items():
                # restrict conditions to  only those submenus that are or aren't in the food_categories list
                if submenu_text in food_categories:
                    if food_ids:
                        print(len(food_ids))
                        for food_id in food_ids:
                            food_category = FoodCategory(
                                parent_id=parent_id,
                                parent_name=parent_name,
                                child_id=(parent_id + count / 100),
                                child_name=submenu_text,
                                food_id=food_id
                            )

                            # Insert into database
                            cur.execute(
                                "INSERT INTO foods_category_cooky_test (parent_category_id, parent_category_name, child_category_id, child_category_name, food_id) VALUES (%s, %s, %s, %s, %s)",
                                (
                                    food_category.parent_id,
                                    food_category.parent_name,
                                    food_category.child_id,
                                    food_category.child_name,
                                    food_category.food_id
                                )
                            )
                            conn.commit()
            food_categories.append(food_category.child_name)
        submenu.click()  # Close submenu
        print(f"  unchecked {submenu_text}")
    element.click()
    print(f"unchecked {parent_name}")


conn.close()
cur.close()

# Quit the web driver
driver.quit()

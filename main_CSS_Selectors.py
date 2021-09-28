from selenium import webdriver
import re
import json

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

URL = "https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99"


def init_settings():
    chrome_driver_path = '../Edited_task - CSS Selectors/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chrome_driver_path)

    driver.get(URL)
    return driver


def check_page_availability(browser):
    try:
        delay = 10  # seconds
        WebDriverWait(browser, delay).until(expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, 'h1.product-name')))
    except Exception as err:
        raise RuntimeError(f'Failed to find an element. Details: {str(err)}')


def convert_to_float(price):
    try:
        find_num = re.findall(r"(\d+\.\d{2}?)|\d+", price)
        result_float_number = float(''.join(find_num))
        return result_float_number
    except ValueError as err:
        return f"Unable to convert the value: [{price}]. Details: {str(err)}"


def get_list_sizes(sizes):
    try:
        list_sizes = [span.get_attribute('data-size') for span in sizes]
        return list_sizes
    except Exception as err:
        return f"Unable to create а list. Details: {str(err)}"

def create_json(result_dict):
    try:
        file_name = '../Edited_task - CSS Selectors/data.json'
        with open('../Edited_task - CSS Selectors/data.json', 'w') as outfile:
            json.dump(result_dict, outfile)
        return file_name
    except Exception as err:
        return f"Unable to create a json file. Details: {str(err)}"


def app():
    try:
        browser = init_settings()
        print(browser)
        check_page_availability(browser)
        item_name = browser.find_element_by_css_selector('.product-actions .product-name').text
        item_price = browser.find_element_by_css_selector('div.product-prices span.product-sale').text
        item_color = browser.find_element_by_css_selector('div.colors-info span.colors-info-name').text
        item_sizes = browser.find_elements_by_css_selector('div.selector-list span')

        item_price_digits = convert_to_float(item_price)
        list_item_sizes = get_list_sizes(item_sizes)
        item_details = {
            "name": item_name,
            "price": item_price_digits,
            "color": item_color,
            "size": list_item_sizes,
        }
        location_file = create_json(item_details)
        return f"File has been created in main directory: {location_file}"
    except Exception as err:
        return f"Unable to scrap data from the web page.Details: {str(err)}"


result = app()

print(result)

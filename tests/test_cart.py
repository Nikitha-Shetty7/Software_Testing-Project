import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

BASE_URL = 'http://127.0.0.1:5000'


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    d.implicitly_wait(3)

    d.get(f'{BASE_URL}/login')
    d.find_element(By.ID, 'email').send_keys('test@gmail.com')
    d.find_element(By.ID, 'password').send_keys('password123')
    d.find_element(By.ID, 'login').click()
    WebDriverWait(d, 5).until(EC.url_contains('/home'))

    yield d
    d.quit()


def add_product_to_cart(driver, product_id, quantity=1):
    driver.get(f'{BASE_URL}/product/{product_id}')

    wait = WebDriverWait(driver, 8)
    qty_input = wait.until(EC.presence_of_element_located((By.ID, 'quantity')))

    # Set the value directly via JS instead of send_keys, to avoid
    # native number-input spinner controls interfering with the click
    driver.execute_script(
        "arguments[0].value = arguments[1];", qty_input, str(quantity)
    )

    add_button = wait.until(EC.presence_of_element_located((By.ID, 'addToCart')))
    driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
    driver.execute_script("arguments[0].click();", add_button)

    wait.until(EC.url_contains('/cart'))


def wait_for_quantity_value(driver, product_id, expected_value, timeout=5):
    """Polls for the quantity text, safely ignoring stale references
    caused by the page reloading mid-check after a form submit."""
    def check(d):
        try:
            return d.find_element(By.ID, f'qtyValue-{product_id}').text.strip() == expected_value
        except StaleElementReferenceException:
            return False
    WebDriverWait(driver, timeout).until(check)


# Test Case: Add a single product to cart
def test_add_product_to_cart(driver):
    add_product_to_cart(driver, 'laptop', 1)
    row = driver.find_element(By.ID, 'cart-item-laptop')
    assert 'Laptop' in row.text


# Test Case: Add multiple different products
def test_add_multiple_products(driver):
    add_product_to_cart(driver, 'laptop', 1)
    add_product_to_cart(driver, 'headphones', 1)

    assert driver.find_element(By.ID, 'cart-item-laptop') is not None
    assert driver.find_element(By.ID, 'cart-item-headphones') is not None


# Test Case: Increase quantity
def test_increase_quantity(driver):
    add_product_to_cart(driver, 'laptop', 1)

    driver.find_element(By.ID, 'increase-laptop').click()
    wait_for_quantity_value(driver, 'laptop', '2')

    qty = driver.find_element(By.ID, 'qtyValue-laptop').text.strip()
    assert qty == '2'


# Test Case: Decrease quantity (but never below 1)
def test_decrease_quantity(driver):
    add_product_to_cart(driver, 'laptop', 2)

    driver.find_element(By.ID, 'decrease-laptop').click()
    wait_for_quantity_value(driver, 'laptop', '1')
    assert driver.find_element(By.ID, 'qtyValue-laptop').text.strip() == '1'

    # Click decrease again - should stay at 1, not go to 0
    driver.find_element(By.ID, 'decrease-laptop').click()
    time.sleep(1)
    assert driver.find_element(By.ID, 'qtyValue-laptop').text.strip() == '1'


# Test Case: Remove a product from cart
def test_remove_product(driver):
    add_product_to_cart(driver, 'laptop', 1)

    driver.find_element(By.ID, 'remove-laptop').click()
    WebDriverWait(driver, 5).until(EC.url_contains('/cart'))

    assert 'cart-item-laptop' not in driver.page_source


# Test Case: Verify total price calculation
def test_cart_total_calculation(driver):
    add_product_to_cart(driver, 'headphones', 2)  # 2000 x 2 = 4000

    total_text = driver.find_element(By.ID, 'cartTotal').text
    assert '4000' in total_text


# Test Case: Empty quantity field defaults to 1 (edge case)
def test_empty_quantity_defaults_to_one(driver):
    driver.get(f'{BASE_URL}/product/laptop')

    wait = WebDriverWait(driver, 8)
    qty_input = wait.until(EC.presence_of_element_located((By.ID, 'quantity')))
    driver.execute_script("arguments[0].value = '';", qty_input)

    add_button = wait.until(EC.presence_of_element_located((By.ID, 'addToCart')))
    driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
    driver.execute_script("arguments[0].click();", add_button)

    wait.until(EC.url_contains('/cart'))

    qty = driver.find_element(By.ID, 'qtyValue-laptop').text.strip()
    assert qty == '1'
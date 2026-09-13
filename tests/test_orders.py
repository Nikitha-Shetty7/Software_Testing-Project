import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = 'http://127.0.0.1:5000'


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    d.implicitly_wait(3)

    # Log in
    d.get(f'{BASE_URL}/login')
    d.find_element(By.ID, 'email').send_keys('test@gmail.com')
    d.find_element(By.ID, 'password').send_keys('password123')
    d.find_element(By.ID, 'login').click()
    WebDriverWait(d, 5).until(EC.url_contains('/home'))

    # Add a product to cart
    d.get(f'{BASE_URL}/product/headphones')
    wait = WebDriverWait(d, 8)
    qty_input = wait.until(EC.presence_of_element_located((By.ID, 'quantity')))
    d.execute_script("arguments[0].value = '1';", qty_input)
    add_button = wait.until(EC.presence_of_element_located((By.ID, 'addToCart')))
    d.execute_script("arguments[0].scrollIntoView(true);", add_button)
    d.execute_script("arguments[0].click();", add_button)
    wait.until(EC.url_contains('/cart'))

    # Fill checkout with valid details, lands on /payment
    d.get(f'{BASE_URL}/checkout')
    d.find_element(By.ID, 'name').send_keys('Test User')
    d.find_element(By.ID, 'phone').send_keys('9876543210')
    d.find_element(By.ID, 'address').send_keys('123 Main St')
    d.find_element(By.ID, 'city').send_keys('Bangalore')
    d.find_element(By.ID, 'pincode').send_keys('560001')
    d.find_element(By.ID, 'continueBtn').click()
    WebDriverWait(d, 5).until(EC.url_contains('/payment'))

    # Complete payment with UPI, creating one order
    d.find_element(By.ID, 'upi').click()
    d.find_element(By.ID, 'payNow').click()
    WebDriverWait(d, 5).until(EC.presence_of_element_located((By.ID, 'successMsg')))

    yield d
    d.quit()


# Test Case: View order history
def test_view_order_history(driver):
    driver.get(f'{BASE_URL}/orders')
    assert 'ORD' in driver.page_source


# Test Case: View order details
def test_view_order_details(driver):
    driver.get(f'{BASE_URL}/orders')
    view_link = driver.find_element(By.CSS_SELECTOR, "a[id^='viewOrder-']")
    order_id = view_link.get_attribute('id').replace('viewOrder-', '')
    view_link.click()

    WebDriverWait(driver, 5).until(EC.url_contains(f'/order/{order_id}'))

    detail_text = driver.find_element(By.ID, 'detailOrderId').text
    assert order_id in detail_text


# Test Case: Cancel an order
def test_cancel_order(driver):
    driver.get(f'{BASE_URL}/orders')
    driver.find_element(By.CSS_SELECTOR, "a[id^='viewOrder-']").click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'cancelOrder')))
    driver.find_element(By.ID, 'cancelOrder').click()

    WebDriverWait(driver, 5).until(
        lambda d: 'Cancelled' in d.find_element(By.ID, 'detailStatus').text
    )
    assert 'Cancelled' in driver.find_element(By.ID, 'detailStatus').text


# Test Case: Cancel button disappears after cancelling
def test_cancel_button_disappears_after_cancel(driver):
    driver.get(f'{BASE_URL}/orders')
    driver.find_element(By.CSS_SELECTOR, "a[id^='viewOrder-']").click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'cancelOrder')))
    driver.find_element(By.ID, 'cancelOrder').click()

    WebDriverWait(driver, 5).until(
        lambda d: 'Cancelled' in d.find_element(By.ID, 'detailStatus').text
    )

    cancel_buttons = driver.find_elements(By.ID, 'cancelOrder')
    assert len(cancel_buttons) == 0
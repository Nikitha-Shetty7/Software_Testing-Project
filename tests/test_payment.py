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
    d.get(f'{BASE_URL}/product/laptop')
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

    yield d
    d.quit()


# Test Case: Pay with UPI -> should be marked Paid
def test_pay_with_upi(driver):
    driver.find_element(By.ID, 'upi').click()
    driver.find_element(By.ID, 'payNow').click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'successMsg')))

    message = driver.find_element(By.ID, 'successMsg').text
    status = driver.find_element(By.ID, 'paymentStatus').text

    assert 'Payment Successful' in message
    assert 'Paid' in status


# Test Case: Pay with Card -> should also be marked Paid
def test_pay_with_card(driver):
    driver.find_element(By.ID, 'card').click()
    driver.find_element(By.ID, 'payNow').click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'successMsg')))

    status = driver.find_element(By.ID, 'paymentStatus').text
    assert 'Paid' in status


# Test Case: Pay with Cash on Delivery -> should be Pending, NOT Paid
def test_pay_with_cod(driver):
    driver.find_element(By.ID, 'cod').click()
    driver.find_element(By.ID, 'payNow').click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'successMsg')))

    message = driver.find_element(By.ID, 'successMsg').text
    status = driver.find_element(By.ID, 'paymentStatus').text

    assert 'Order Placed' in message
    assert 'Pending' in status


# Test Case: Amount shown on payment page matches the cart total
def test_payment_amount_displayed(driver):
    amount_text = driver.find_element(By.ID, 'amount').text
    assert 'Rs.' in amount_text
    assert '50000' in amount_text  # laptop price
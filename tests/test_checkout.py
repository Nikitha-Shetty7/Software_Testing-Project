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

    # Add a product to cart so checkout has something to work with
    d.get(f'{BASE_URL}/product/laptop')
    qty_input = d.find_element(By.ID, 'quantity')
    qty_input.clear()
    qty_input.send_keys('1')
    d.find_element(By.ID, 'addToCart').click()
    WebDriverWait(d, 5).until(EC.url_contains('/cart'))

    yield d
    d.quit()


# Test Case: Checkout with valid address
def test_valid_checkout(driver):
    driver.get(f'{BASE_URL}/checkout')
    driver.find_element(By.ID, 'name').send_keys('Test User')
    driver.find_element(By.ID, 'phone').send_keys('9876543210')
    driver.find_element(By.ID, 'address').send_keys('123 Main St')
    driver.find_element(By.ID, 'city').send_keys('Bangalore')
    driver.find_element(By.ID, 'pincode').send_keys('560001')
    driver.find_element(By.ID, 'continueBtn').click()

    WebDriverWait(driver, 5).until(EC.url_contains('/payment'))
    assert '/payment' in driver.current_url


# Test Case: Empty address fields
def test_empty_fields(driver):
    driver.get(f'{BASE_URL}/checkout')
    driver.find_element(By.ID, 'continueBtn').click()

    errors = driver.find_element(By.ID, 'errorList').text
    assert 'required' in errors


# Test Case: Invalid phone number
def test_invalid_phone_number(driver):
    driver.get(f'{BASE_URL}/checkout')
    driver.find_element(By.ID, 'name').send_keys('Test User')
    driver.find_element(By.ID, 'phone').send_keys('12345')  # not 10 digits
    driver.find_element(By.ID, 'address').send_keys('123 Main St')
    driver.find_element(By.ID, 'city').send_keys('Bangalore')
    driver.find_element(By.ID, 'pincode').send_keys('560001')
    driver.find_element(By.ID, 'continueBtn').click()

    errors = driver.find_element(By.ID, 'errorList').text
    assert '10 digits' in errors


# Test Case: Invalid pincode
def test_invalid_pincode(driver):
    driver.get(f'{BASE_URL}/checkout')
    driver.find_element(By.ID, 'name').send_keys('Test User')
    driver.find_element(By.ID, 'phone').send_keys('9876543210')
    driver.find_element(By.ID, 'address').send_keys('123 Main St')
    driver.find_element(By.ID, 'city').send_keys('Bangalore')
    driver.find_element(By.ID, 'pincode').send_keys('123')  # not 6 digits
    driver.find_element(By.ID, 'continueBtn').click()

    errors = driver.find_element(By.ID, 'errorList').text
    assert '6 digits' in errors


# Test Case: Select delivery option and see live preview update
def test_delivery_option_selection(driver):
    driver.get(f'{BASE_URL}/checkout')
    express_radio = driver.find_element(By.ID, 'express')
    express_radio.click()

    assert express_radio.is_selected()

    preview = driver.find_element(By.ID, 'deliveryPreview').text
    assert 'Estimated delivery' in preview
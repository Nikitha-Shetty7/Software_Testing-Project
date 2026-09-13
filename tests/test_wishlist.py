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

    yield d
    d.quit()


# Test Case: Add product to wishlist
def test_add_to_wishlist(driver):
    driver.get(f'{BASE_URL}/product/laptop')
    driver.find_element(By.ID, 'addToWishlist').click()

    WebDriverWait(driver, 5).until(EC.url_contains('/wishlist'))
    assert driver.find_element(By.ID, 'wishlist-laptop') is not None


# Test Case: Remove product from wishlist
def test_remove_from_wishlist(driver):
    driver.get(f'{BASE_URL}/product/laptop')
    driver.find_element(By.ID, 'addToWishlist').click()
    WebDriverWait(driver, 5).until(EC.url_contains('/wishlist'))

    driver.find_element(By.ID, 'removeWishlist-laptop').click()
    WebDriverWait(driver, 5).until(EC.url_contains('/wishlist'))

    assert 'wishlist-laptop' not in driver.page_source


# Test Case: Move wishlist product to cart
def test_move_wishlist_to_cart(driver):
    driver.get(f'{BASE_URL}/product/headphones')
    driver.find_element(By.ID, 'addToWishlist').click()
    WebDriverWait(driver, 5).until(EC.url_contains('/wishlist'))

    driver.find_element(By.ID, 'moveToCart-headphones').click()
    WebDriverWait(driver, 5).until(EC.url_contains('/cart'))

    assert driver.find_element(By.ID, 'cart-item-headphones') is not None


# Test Case: Empty wishlist shows a friendly message
def test_empty_wishlist_message(driver):
    driver.get(f'{BASE_URL}/wishlist')
    message = driver.find_element(By.ID, 'emptyWishlist').text
    assert 'empty' in message.lower()

import pytest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    d.implicitly_wait(3)

    yield d

    d.quit()


def unique_email():
    return f"user{int(time.time() * 1000)}@gmail.com"


# Test Case 1: Valid Registration
def test_valid_registration(driver):
    driver.get(f"{BASE_URL}/register")
    time.sleep(2)

    email = unique_email()

    driver.find_element(By.ID, "name").send_keys("Test User")
    time.sleep(2)

    driver.find_element(By.ID, "email").send_keys(email)
    time.sleep(2)

    driver.find_element(By.ID, "password").send_keys("mypassword123")
    time.sleep(2)

    driver.find_element(By.ID, "confirm_password").send_keys("mypassword123")
    time.sleep(2)

    driver.find_element(By.ID, "registerBtn").click()
    time.sleep(3)

    wait = WebDriverWait(driver, 5)
    wait.until(EC.url_contains("/login"))

    assert "/login" in driver.current_url


# Test Case 2: Existing Email
def test_existing_email(driver):
    driver.get(f"{BASE_URL}/register")
    time.sleep(2)

    driver.find_element(By.ID, "name").send_keys("Another User")
    time.sleep(1)

    driver.find_element(By.ID, "email").send_keys("test@gmail.com")
    time.sleep(1)

    driver.find_element(By.ID, "password").send_keys("somepassword")
    time.sleep(1)

    driver.find_element(By.ID, "confirm_password").send_keys("somepassword")
    time.sleep(1)

    driver.find_element(By.ID, "registerBtn").click()
    time.sleep(3)

    error = driver.find_element(By.ID, "error").text

    assert "already exists" in error


# Test Case 3: Empty Fields
def test_empty_fields(driver):
    driver.get(f"{BASE_URL}/register")
    time.sleep(2)

    driver.find_element(By.ID, "registerBtn").click()
    time.sleep(3)

    error = driver.find_element(By.ID, "error").text

    assert "required" in error


# Test Case 4: Invalid Email Format
def test_invalid_email(driver):
    driver.get(f"{BASE_URL}/register")
    time.sleep(2)

    driver.find_element(By.ID, "name").send_keys("Test User")
    time.sleep(1)

    driver.find_element(By.ID, "email").send_keys("notanemail")
    time.sleep(1)

    driver.find_element(By.ID, "password").send_keys("mypassword123")
    time.sleep(1)

    driver.find_element(By.ID, "confirm_password").send_keys("mypassword123")
    time.sleep(1)

    driver.find_element(By.ID, "registerBtn").click()
    time.sleep(3)

    error = driver.find_element(By.ID, "error").text

    assert "valid email" in error


# Test Case 5: Password Mismatch
def test_password_mismatch(driver):
    driver.get(f"{BASE_URL}/register")
    time.sleep(2)

    email = unique_email()

    driver.find_element(By.ID, "name").send_keys("Test User")
    time.sleep(1)

    driver.find_element(By.ID, "email").send_keys(email)
    time.sleep(1)

    driver.find_element(By.ID, "password").send_keys("password123")
    time.sleep(1)

    driver.find_element(By.ID, "confirm_password").send_keys("differentpassword")
    time.sleep(1)

    driver.find_element(By.ID, "registerBtn").click()
    time.sleep(3)

    error = driver.find_element(By.ID, "error").text

    assert "do not match" in error

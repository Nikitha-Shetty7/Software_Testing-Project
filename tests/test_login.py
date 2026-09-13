import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    d.implicitly_wait(3)
    yield d
    d.quit()


# Test Case 1: Valid Login
def test_valid_login(driver):
    driver.get(f"{BASE_URL}/login")

    driver.find_element(By.ID, "email").send_keys("test@gmail.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "login").click()

    time.sleep(2)

    assert "/home" in driver.current_url


# Test Case 2: Wrong Password
def test_wrong_password(driver):
    driver.get(f"{BASE_URL}/login")

    driver.find_element(By.ID, "email").send_keys("test@gmail.com")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.ID, "login").click()

    time.sleep(2)

    error = driver.find_element(By.CLASS_NAME, "error").text

    assert "Invalid" in error


# Test Case 3: Wrong Email
def test_wrong_email(driver):
    driver.get(f"{BASE_URL}/login")

    driver.find_element(By.ID, "email").send_keys("notregistered@gmail.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "login").click()

    time.sleep(2)

    error = driver.find_element(By.CLASS_NAME, "error").text

    assert "Invalid" in error


# Test Case 4: Empty Fields
def test_empty_fields(driver):
    driver.get(f"{BASE_URL}/login")

    driver.find_element(By.ID, "login").click()

    time.sleep(2)

    # No separate empty-field validation yet.
    # The application should show invalid credentials.
    error = driver.find_element(By.CLASS_NAME, "error").text

    assert "Invalid" in error


# Test Case 5: Logout
def test_logout(driver):
    driver.get(f"{BASE_URL}/login")

    driver.find_element(By.ID, "email").send_keys("test@gmail.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "login").click()

    wait = WebDriverWait(driver, 5)
    wait.until(EC.url_contains("/home"))

    logout_link = wait.until(EC.element_to_be_clickable((By.ID, "logout")))
    driver.execute_script("arguments[0].scrollIntoView(true);", logout_link)
    logout_link.click()

    try:
        wait.until(EC.url_contains("/login"))
    except Exception:
        driver.save_screenshot("logout_failure.png")
        raise

    assert "/login" in driver.current_url
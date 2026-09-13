
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


# Test Case 1: Search for an existing product
def test_search_existing_product(driver):
    driver.get(f"{BASE_URL}/products")
    time.sleep(2)

    search_box = driver.find_element(By.ID, "search")
    search_box.send_keys("laptop")
    time.sleep(2)

    driver.find_element(By.ID, "searchBtn").click()
    time.sleep(3)

    wait = WebDriverWait(driver, 5)

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "view-laptop")
        )
    )

    result = driver.find_element(By.ID, "view-laptop")

    assert result is not None


# Test Case 2: Search for an unavailable product
def test_search_unavailable_product(driver):
    driver.get(f"{BASE_URL}/products")
    time.sleep(2)

    search_box = driver.find_element(By.ID, "search")
    search_box.send_keys("xyzxyznotaproduct")
    time.sleep(2)

    driver.find_element(By.ID, "searchBtn").click()
    time.sleep(3)

    wait = WebDriverWait(driver, 5)

    message = wait.until(
        EC.presence_of_element_located(
            (By.ID, "noResults")
        )
    )

    assert "No products found" in message.text


# Test Case 3: Filter by category
def test_filter_by_category(driver):
    driver.get(f"{BASE_URL}/products")
    time.sleep(2)

    driver.find_element(
        By.LINK_TEXT,
        "Books"
    ).click()

    time.sleep(3)

    wait = WebDriverWait(driver, 5)

    wait.until(
        EC.url_contains("category=Books")
    )

    product_list = driver.find_element(
        By.ID,
        "productList"
    )

    assert "Mystery Novel" in product_list.text
    assert "Laptop" not in product_list.text


# Test Case 4: All link resets the filter
def test_all_shows_every_product(driver):
    driver.get(
        f"{BASE_URL}/products?category=Books"
    )
    time.sleep(2)

    driver.find_element(
        By.LINK_TEXT,
        "All"
    ).click()

    time.sleep(3)

    wait = WebDriverWait(driver, 5)

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "view-laptop")
        )
    )

    product_list = driver.find_element(
        By.ID,
        "productList"
    )

    assert "Laptop" in product_list.text
    assert "Mystery Novel" in product_list.text


# Test Case 5: Open a product's detail page
def test_open_product_details(driver):
    driver.get(f"{BASE_URL}/products")
    time.sleep(2)

    wait = WebDriverWait(driver, 5)

    view_link = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "view-laptop")
        )
    )

    time.sleep(2)

    view_link.click()

    time.sleep(3)

    wait.until(
        EC.url_contains("/product/laptop")
    )

    product_name = driver.find_element(
        By.ID,
        "productName"
    ).text

    assert "Laptop" in product_name

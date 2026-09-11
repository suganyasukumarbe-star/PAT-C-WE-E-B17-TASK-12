import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


@pytest.fixture(scope="module")
def driver():
    """
    Pytest fixture to initialize and tear down the Chrome WebDriver instance.
    """
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Initialize the driver using webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Navigate to the target web application
    driver.get("https://guvi.in")
    time.sleep(3)  # Initial load wait time

    yield driver

    # Teardown: Close the browser session
    driver.quit()


def test_validate_dynamic_xpath_axes(driver):
    """
    Test case to validate dynamic XPaths and Axes relationships on the GUVI homepage header elements.
    """

    print("\n--- Starting Dynamic XPath & Axes Validations ---")

    # 1. Base Element: Target the 'Courses' anchor link text as our reference point
    base_element_xpath = "//a[contains(text(), 'Courses')]"
    # Specify the visible navbar or container to avoid matching hidden elements
    # base_element_xpath = "//nav//a[contains(text(), 'Courses')] | //div[contains(@class, 'nav')]//a[contains(text(), 'Courses')]"
    base_element = driver.find_element(By.XPATH, base_element_xpath)
    assert base_element.is_displayed(), "Base element 'Courses' not found on the page."
    print(f"Base element verified: {base_element.text}")

    # 2. Relative XPath: Find the parent element, then find its first child element
    # Axis used: parent:: and child::
    parent_child_xpath = "//a[contains(text(), 'Courses')]/parent::li/child::a"
    child_element = driver.find_element(By.XPATH, parent_child_xpath)
    assert child_element is not None, "Failed to locate first child element via parent."
    print(f"Parent-Child evaluation success. Child text matches: {child_element.text}")

    # 3. Relative XPath: Locate the second sibling (If any)
    # Axis used: following-sibling:: using index [2] relative to the parent list item wrapper
    second_sibling_xpath = "//a[contains(text(), 'Courses')]/parent::li/following-sibling::li[2]/descendant::a"
    try:
        second_sibling = driver.find_element(By.XPATH, second_sibling_xpath)
        print(f"Second sibling link text located: {second_sibling.text}")
    except Exception:
        print("Second sibling element not present or structure differs.")

    # 4. Relative XPath: Select the parent element of an element with the attribute "href"
    # Axis used: /parent::* looking upward from an anchor tag that has an href attribute
    href_parent_xpath = "//a[@href and contains(text(), 'Courses')]/parent::*"
    href_parent = driver.find_element(By.XPATH, href_parent_xpath)
    assert href_parent is not None, "Failed to fetch the parent element of the href node."
    print(f"Successfully selected parent element tag: <{href_parent.tag_name}>")

    # 5. Axes: Find all ancestor elements
    # Axis used: ancestor::
    ancestors_xpath = "//a[contains(text(), 'Courses')]/ancestor::*"
    ancestors = driver.find_elements(By.XPATH, ancestors_xpath)
    assert len(ancestors) > 0, "No ancestor elements found."
    print(f"Total ancestor elements discovered for 'Courses': {len(ancestors)}")

    # 6. Axes: Locate all following siblings
    # Axis used: following-sibling::
    following_siblings_xpath = "//a[contains(text(), 'Courses')]/parent::li/following-sibling::li"
    following_siblings = driver.find_elements(By.XPATH, following_siblings_xpath)
    print(f"Number of following sibling elements in header list: {len(following_siblings)}")

    # 7. Axes: Select all preceding elements
    # Axis used: preceding::
    preceding_elements_xpath = "//a[contains(text(), 'Courses')]/preceding::*"
    preceding_elements = driver.find_elements(By.XPATH, preceding_elements_xpath)
    print(f"Number of preceding structural DOM elements found: {len(preceding_elements)}")

    print("--- Dynamic XPath validation complete ---")

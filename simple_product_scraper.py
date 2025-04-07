import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()
driver.maximize_window()  # Maximize the browser window
wait = WebDriverWait(driver, 15)  # Explicit wait for elements

# Open the target URL
driver.get("https://www.glossier.com/en-bd/collections/all")
time.sleep(10)  # Allow page to load

# Automate scrolling to the bottom of the page
scroll_increment = 500
current_position = 0
end_of_scroll = driver.execute_script("return document.body.scrollHeight")

while current_position < end_of_scroll:
    driver.execute_script(f"window.scrollTo(0, {current_position});")
    time.sleep(1)  # Wait for content to load
    current_position += scroll_increment
    end_of_scroll = driver.execute_script("return document.body.scrollHeight")

# Locate product names and prices using XPath
prouct_name = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='pi__details']")))
prouct_price = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//p[@class='pi__price js-product-item-price']")))

# Display the scraped data
for index, (name, price) in enumerate(zip(prouct_name, prouct_price), start=1):
    print(f"\n✅ Product No: {index}")
    print(f"🛑 Name: {name.text}")
    print(f"💰 Price: {price.text}")
    print("-" * 40)

# Close the browser
driver.quit()


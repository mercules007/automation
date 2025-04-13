from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import time

# Create Excel File
wb = Workbook()
ws = wb.active
ws.title = "Amazon Laptops"
ws.append(["Laptop Name", "Price", "Reviews"])

# Launch Browser
driver = webdriver.Firefox()
driver.get("https://www.amazon.in")
driver.maximize_window()
time.sleep(3)

# Search for "laptop" in the search box
search_box = driver.find_element(By.XPATH, "//input[@id='twotabsearchtextbox']")
search_box.send_keys("laptop")
time.sleep(2)
driver.find_element(By.XPATH, "//input[@id='nav-search-submit-button']").click()
time.sleep(2)

# Select the 20th filter option (HP laptops)
hp = driver.find_element(By.XPATH, "//li[@id='p_123/308445']//i")
driver.execute_script("arguments[0].scrollIntoView(true);", hp)
hp.click()
time.sleep(3)

# Loop through pages
page = 1
max_pages = 50  # Set how many pages you want to scrape

while True:
    print(f"📄 Scraping Page: {page}")

    # Get all product listings on current page
    all_products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

    for product in all_products:
        try:
            name = product.find_element(By.XPATH, ".//div[@data-cy='title-recipe']").text
        except:
            name = "N/A"

        try:
            price = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
        except:
            price = "N/A"

        try:
            review = product.find_element(By.XPATH, ".//span[@class='a-size-base s-underline-text']").text
        except:
            review = "0"

        # Write data to Excel
        ws.append([name, price, review])

    # Check if "Next" button exists
    try:
        next_btn = driver.find_element(By.XPATH, "(//li[@class='s-list-item-margin-right-adjustment'])[4]")
        if "disabled" in next_btn.get_attribute("class"):
            print("❌ No more pages.")
            break
        else:
            next_btn.click()
            page += 1
            time.sleep(4)
    except:
        print("❌ Next Button Not Found!")
        break

    if page > max_pages:
        print("✅ Max pages reached.")
        break

# Save Excel File
wb.save("amazon_laptops_hp.xlsx")
driver.quit()

print("✅ All Data Saved to Excel using openpyxl!")

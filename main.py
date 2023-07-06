from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import pandas as pd
import calendar
import time

driver = webdriver.Chrome()


def screenshot(i):
    ts = calendar.timegm(time.gmtime())
    dt = datetime.fromtimestamp(ts)
    my_date_time = dt.strftime("D%dM%mY%Y_H%HM%MS%S")
    screenshot_name = "screenshot_" + my_date_time + "-page_" + str(i + 1) + ".png"
    print(screenshot_name)
    driver.save_screenshot(r"C:\Users\User\PycharmProjects\\amazon_scrapper_selenium\screenshots\\" + screenshot_name)


def amazon_scrapping(key, category, pages):
    driver.get("https://www.amazon.com")
    driver.maximize_window()

    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.clear()
    search_box.send_keys(key)
    driver.find_element(By.ID, "nav-search-submit-button").click()

    driver.find_element(By.XPATH, "//span[text()='" + category + "']").click()

    product_names = []
    product_prices = []
    product_prices_whole = []
    product_prices_fractions = []
    product_reviews = []

    for i in range(pages):
        print('Scraping page', i + 1)
        screenshot(i)

        all_products = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

        for product in all_products:

            names = product.find_elements(By.XPATH, ".//span[@class='a-size-base-plus a-color-base a-text-normal']")
            for name in names:
                product_names.append(name.text)

            prices_whole = product.find_elements(By.XPATH, ".//span[@class='a-price-whole']")
            for price_wh in prices_whole:
                product_prices_whole.append(price_wh.text)

            prices_fractions = product.find_elements(By.XPATH, ".//span[@class='a-price-fraction']")
            for price_fr in prices_fractions:
                product_prices_fractions.append(price_fr.text)

            for str1, str2 in zip(product_prices_whole, product_prices_fractions):
                buf = str1 + "," + str2
                product_prices.append(buf)

            try:
                if len(product.find_elements(By.XPATH, ".//span[@class='a-size-base s-underline-text']")) > 0:
                    reviews = product.find_elements(By.XPATH, ".//span[@class='a-size-base s-underline-text']")
                    for review in reviews:
                        product_reviews.append(review.text.replace(",", " "))
                else:
                    product_reviews.append("0")
            except:
                pass

        driver.find_element(By.XPATH, "//a[text()='Next']").click()
        time.sleep(3)

    df = pd.DataFrame(zip(product_names, product_prices, product_reviews),
                      columns=['product_names', 'product_prices', 'product_reviews'])
    df.to_excel(r"C:\Users\User\PycharmProjects\amazon_scrapper_selenium\xlsx\watches.xlsx", index=False)

    driver.quit()


def main():
    amazon_scrapping("watch for men", "Quartz", 5)


if __name__ == "__main__":
    main()

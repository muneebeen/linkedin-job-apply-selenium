import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


def configure_driver(options_set):
    d = webdriver.Chrome(options=options_set)
    return d


def configure_webdriver_options():
    o = webdriver.ChromeOptions()
    o.add_experimental_option("excludeSwitches", ["enable-automation"])
    o.add_experimental_option('useAutomationExtension', False)
    o.add_argument("--disable-blink-features=AutomationControlled")
    o.add_argument("--window-size=1880,1300")
    o.add_argument("--disable-notifications")
    # o.headless = True
    return o


if __name__ == '__main__':
    # configuring options
    username = "Enter email"
    password = "Enter Password"
    job_title = "Junior Software Engineer"

    options = configure_webdriver_options()

    # configuring driver
    driver = configure_driver(options)
    driver.get('https://www.linkedin.com/')

    for _chr in username:
        driver.find_element(By.CSS_SELECTOR, "input[autocomplete='username']").send_keys(_chr)
        time.sleep(0.1)
    time.sleep(2)

    for _chr in password:
        driver.find_element(By.CSS_SELECTOR, "input[autocomplete='current-password']").send_keys(_chr)
        time.sleep(0.1)
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, "button[data-id='sign-in-form__submit-btn']").click()
    if "https://www.linkedin.com/feed" in driver.current_url:
        print("I am on correct page.")
        time.sleep(1)
        job_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.global-nav__primary-item:nth-of-type(3) > a")))
        job_link.click()
        time.sleep(2)
        search_bar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.jobs-search-box__text-input")))
        search_bar.send_keys(job_title)
        time.sleep(2)
        search_bar.send_keys(Keys.RETURN)
        easy_apply = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.search-reusables__primary-filter:nth-of-type(8)")))
        easy_apply.click()
        time.sleep(2)

        job_list_section = driver.find_element(By.CLASS_NAME, "jobs-search-results-list")
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", job_list_section)

        action_chains = ActionChains(driver)
        action_chains.move_to_element(job_list_section).perform()
        driver.execute_script('arguments[0].scrollTop = 0', job_list_section)

        list_of_jobs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.scaffold-layout__list-container > li")))
        print(len(list_of_jobs))

        for i in range(0, len(list_of_jobs)):
            list_of_jobs = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.scaffold-layout__list-container > li")))
            list_of_jobs[i].click()
            time.sleep(1)
            easy_apply_btn = driver.find_elements(By.CSS_SELECTOR, "div.jobs-s-apply")[0]
            easy_apply_btn.click()
            time.sleep(2)
            phone_no_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.jobs-easy-apply-form-section__grouping:nth-of-type(4) input")))
            phone_no_input.click()
            phone_no_input.send_keys("123456789")
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,"button[aria-label='Continue to next step']").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,"button[aria-label='Choose Resume']").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,"button[aria-label='Review your application']").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,"button[aria-label='Submit application']").click()


    input("Press Enter to close the browser...")
    driver.quit()
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from secrets import login, password, search_text


class Instagram:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.path = f'{os.getcwd()}/chromedriver'
        mobile_emulation = {
            "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "mobileEmulation", mobile_emulation)
        self.driver = webdriver.Chrome(
            self.path, chrome_options=chrome_options)

    def login(self):
        driver = self.driver
        driver.get('https://www.instagram.com/accounts/login/')
        driver.maximize_window()
        time.sleep(2)
        element = driver.find_element_by_name('username')
        element.send_keys(login)
        element = driver.find_element_by_name('password')
        element.send_keys(password)
        element.submit()
        time.sleep(1)

    def cancel_pops(self):
        time.sleep(7)
        not_now = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/div/button')
        not_now.click()
        time.sleep(2)
        try:
            cancel = self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[3]/button[2]')
            cancel.click()
        except NoSuchElementException:
            print('No such element:')
        finally:
            print('Continue...')

    def search_name(self, input_text):
        self.input_text = input_text
        self.driver.get('https://www.instagram.com/explore/')
        search_box = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav[1]/div/header/div/h1/div/div/div/div[1]/label/input')
        search_box.send_keys(input_text)
        try:
            print('Loading page...')
            profile = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="react-root"]/section/main/div/div/ul/li[1]/a')))
        except Exception:
            self.driver.get('https://www.instagram.com/jakobowsky/')
        finally:
            time.sleep(3)
            profile.click()

    def profile_name(self):
        driver = self.driver
        try:
            name_person = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="react-root"]/section/main/div/div[1]/h1')))
            name_interest = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="react-root"]/section/main/div/div[1]/a[1]')))
            name_info = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="react-root"]/section/main/div/div[1]/span')))
        finally:
            name_person = name_person.get_attribute('textContent')
            name_interest = name_interest.get_attribute('textContent')
            name_info = name_info.get_attribute('textContent')
            print(f' \n Account name: {name_person}')
            print(f' \n What am intrested in: {name_interest}')
            print(f' \n More info about account: {name_info}')

    def get_details(self):
        driver = self.driver
        try:
            post = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="react-root"]/section/main/div/ul/li[1]/span/span')))
            followers = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="react-root"]/section/main/div/ul/li[2]/a/span')))
            following = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="react-root"]/section/main/div/ul/li[3]/a/span')))
        finally:
            post = post.get_attribute('textContent')
            followers = followers.get_attribute('textContent')
            following = following.get_attribute('textContent')
            print(f' \n Number of post: {post}')
            print(f' \n Number of followers: {followers}')
            print(f' \n Number of following: {following}')

    def close_driver(self):
        time.sleep(2)
        self.driver.close()


if __name__ == '__main__':
    ig = Instagram(login, password)
    print('Loging in...')
    ig.login()
    print('Cancel unwanted info')
    ig.cancel_pops()
    print('Searching for follower')
    ig.search_name(search_text)
    print('Getting profile info...')
    ig.profile_name()
    print('Getting more about info')
    ig.get_details()
    print('Done ....')
    ig.close_driver()

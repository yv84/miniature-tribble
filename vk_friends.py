import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


wd = webdriver.Firefox() # or add to your PATH
wd.set_window_size(1024, 768) # optional
url = 'https://vk.com'
REQUEST_CONTROLS = re.compile("request_controls_")
wd.get(url)

quick_email = wd.find_element_by_css_selector("#quick_email")
quick_email.send_keys(login)
time.sleep(1)

quick_pass = wd.find_element_by_css_selector("#quick_pass")
quick_pass.send_keys(psw)
time.sleep(1)

quick_login_button = wd.find_element_by_css_selector("#quick_login_button")
quick_login_button.click()
time.sleep(2)

my_freinds = wd.find_element_by_css_selector("#l_fr > a:nth-child(1) > span:nth-child(2)")
my_freinds.click()
time.sleep(2)

followers_page = wd.find_element_by_css_selector("#tab_requests > a:nth-child(1) > b:nth-child(3)")
followers_page.click()
time.sleep(2)

wd.execute_script("window.scrollTo(0, 300)")
wd.execute_script("window.scrollTo(0, 2000)")


def get_visible_followers(page):
    followers = wd.find_element_by_css_selector('#list_content > div:nth-child('+str(page)+')')
    followers_ = followers.find_elements_by_css_selector("div.info_no_actions")
    for follower in followers_:
        name = follower.find_element_by_css_selector("div:nth-child(1)").text
        if len(follower.find_elements_by_css_selector("div")) == 6:
            id = follower.find_element_by_css_selector("div:nth-child(5)").\
                find_element_by_css_selector("div").get_attribute('id') #require scroll
        elif len(follower.find_elements_by_css_selector("div")) == 5:
            id = follower.find_element_by_css_selector("div:nth-child(4)").\
                find_element_by_css_selector("div").get_attribute('id') #require scroll
        id = REQUEST_CONTROLS.sub('', id)
        print(name, id)


has_followers = True
ii = 0
while has_followers:
    try:
        ii += 1
        get_visible_followers(ii)
    except:
        has_followers = False


wd.close()
time.sleep(1)
wd.quit()

























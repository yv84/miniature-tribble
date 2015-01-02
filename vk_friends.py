import time
import re
import os
import random


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import select



class Login():
    def __init__(self):
        self.wd = None

    def __enter__(self):
        self.wd = webdriver.Firefox() # or add to your PATH
        self.wd.set_window_size(1024, 768) # optional
        URL = 'https://vk.com'
        self.wd.get(URL)

        quick_email = self.wd.find_element_by_css_selector("#quick_email")
        quick_email.send_keys(os.environ['VK_LOGIN'])
        time.sleep(1)

        quick_pass = self.wd.find_element_by_css_selector("#quick_pass")
        quick_pass.send_keys(os.environ['VK_PSW'])
        time.sleep(1)

        quick_login_button = self.wd.find_element_by_css_selector("#quick_login_button")
        quick_login_button.click()
        time.sleep(2)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wd.close()
        time.sleep(1)
        self.wd.quit()



def get_followers(wd):
    REQUEST_CONTROLS = re.compile("request_controls_")

    def run(self):
        my_freinds = wd.find_element_by_css_selector("#l_fr > a:nth-child(1) > span:nth-child(2)")
        my_freinds.click()
        time.sleep(2)

        followers_page = wd.find_element_by_css_selector("#tab_requests > a:nth-child(1) > b:nth-child(3)")
        followers_page.click()
        time.sleep(2)

        wd.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        # wd.execute_script("window.scrollTo(0, 2000)")

        # no_of_pagedowns = 20
        # while no_of_pagedowns:
        #     elem.send_keys(Keys.PAGE_DOWN)
        #     time.sleep(0.2)
        #     no_of_pagedowns-=1

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



class New_Random_Friends():

    def __init__(self, wd):
        self.wd = wd

    @staticmethod
    def get_list_from_input_field(element):
        FILTER_CONTAINER = "div > div:nth-child(2) > div:nth-child(1) > ul:nth-child(1)"
        return element.find_element_by_css_selector(FILTER_CONTAINER).\
            find_elements_by_css_selector("* > li")

    def random_input_filed(self, ids):
        element = self.wd.find_element_by_css_selector(ids)
        element.click()
        time.sleep(3)
        items = self.get_list_from_input_field(element)
        time.sleep(3)
        item = random.choice(items)
        item.click()
        time.sleep(3)
        return

    def random_data_input_filed(self, ids, year_min, year_max):
        element = self.wd.find_element_by_css_selector(ids)
        element.click()
        time.sleep(3)
        items = self.get_list_from_input_field(element)
        time.sleep(3)
        desired_item = str(random.choice(range(year_min, year_max)))
        for item in items:
            if item.text == desired_item:
                item.click()
                time.sleep(3)
                return
    
    def named_input_filed(self, ids, desired_item):
        element = self.wd.find_element_by_css_selector(ids)
        element.click()
        time.sleep(3)
        items = self.get_list_from_input_field(element)
        time.sleep(3)
        for item in items:
            if item.text == desired_item:
                item.click()
                time.sleep(3)
                return


    def select_region(self, desired_country):
        self.named_input_filed("#cCountry", desired_country)


    def select_city(self, desired_town):
        self.named_input_filed("#cCity", desired_town)


    def select_random_school(self):
        try:
            self.random_input_filed("#cSchool")
        except:
            pass
        try:
            self.random_input_filed("#cSchClass")
        except:
            pass
        try:
            self.random_input_filed("#cSchYear")
        except:
            pass
        return



    def select_random_university(self):
        try:
            self.random_input_filed("#cUniversity")
        except:
            pass
        try:
            self.random_input_filed("#cFaculty")
        except:
            pass
        try:
            self.random_data_input_filed("#cUniYear", 1995, 2012)
        except:
            pass
        # self.random_input_filed("#cEduForm")
        # self.random_input_filed("#cEduStatus")
        return  


    def get_new_friends(self):
        top_search = self.wd.find_element_by_css_selector("#top_search")
        top_search.click()
        time.sleep(2)

        select_region("Russia") # russia
        select_city("Moscow")
        select_random_school()
        select_random_university()




if __name__ == "__main__":
    with Login() as login:
        get_followers(login.wd)
        # new_random_friends = New_Random_Friends(login.wd)
        # new_random_friends.get_new_friends()














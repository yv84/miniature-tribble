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

        quick_login_button = self.wd.find_element_by_css_selector(
            "#quick_login_button")
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
        my_freinds = wd.find_element_by_css_selector(
            "#l_fr > a:nth-child(1) > span:nth-child(2)")
        my_freinds.click()
        time.sleep(2)

        followers_page = wd.find_element_by_css_selector(
            "#tab_requests > a:nth-child(1) > b:nth-child(3)")
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
        followers = wd.find_element_by_css_selector(
            '#list_content > div:nth-child('+str(page)+')')
        followers_ = followers.find_elements_by_css_selector(
            "div.info_no_actions")
        for follower in followers_:
            name = follower.find_element_by_css_selector(
                "div:nth-child(1)").text
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



class NewRandomFriends():

    def __init__(self, wd):
        self.wd = wd
        self.INVITE_BUTTON = re.compile("search_sub")

    @staticmethod
    def get_list_from_input_field(element):
        FILTER_CONTAINER = "div > div:nth-child(2) >" +\
            " div:nth-child(1) > ul:nth-child(1)"
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

    def random_data_input_filed(self, ids, year_min, year_max, prefix=None):
        element = self.wd.find_element_by_css_selector(ids)
        element.click()
        time.sleep(3)
        items = self.get_list_from_input_field(element)
        time.sleep(3)
        desired_item = str(random.choice(range(year_min, year_max+1)))
        for item in items:
            if item.text == prefix+desired_item:
                item.click()
                time.sleep(3)
                return desired_item

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

    def text_input_filed(self, ids, text):
        element = self.wd.find_element_by_css_selector(ids)
        element.click()
        time.sleep(3)
        input_text_field = element.find_element_by_tag_name("input")
        input_text_field.clear()
        input_text_field.send_keys(text)
        time.sleep(3)
        items = self.get_list_from_input_field(element)
        time.sleep(2)
        item = random.choice(items)
        try:
            item.click()
        except:
            pass
        time.sleep(2)

    def random_radiobtns(self, ids):
        element = self.wd.find_element_by_css_selector(ids)
        n = str(random.choice(range(1,
            len(element.find_elements_by_css_selector("div.radiobtn"))+1)
        ))
        element.find_element_by_css_selector(
            "div.radiobtn:nth-child(" + n + ")") \
            .click()

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


    def select_age(self, year_min=18, year_max=40):
        age_filter_min = "#cAge > div:nth-child(1)"
        age_filter_max = "#cAge > div:nth-child(3)"
        # 2 times
        min = int(self.random_data_input_filed(age_filter_min,
            year_min, year_max, prefix="from "))
        min = int(self.random_data_input_filed(age_filter_min,
            year_min, year_max, prefix="from "))
        self.random_data_input_filed(age_filter_max, min, year_max, "to ")
        self.random_data_input_filed(age_filter_max, min, year_max, "to ")
        return

    def select_sex(self):
        self.random_radiobtns("#cSex")


    def select_random_university(self, year_min=1995, year_max=2012):
        try:
            self.random_input_filed("#cUniversity")
        except:
            pass
        try:
            self.random_input_filed("#cFaculty")
        except:
            pass
        try:
            self.random_data_input_filed("#cUniYear", year_min, year_max)
        except:
            pass
        # self.random_input_filed("#cEduForm")
        # self.random_input_filed("#cEduStatus")
        return  

    def invite_random_people_in_search_list(self):
        ppls_ids = self.wd.find_elements_by_css_selector(
            "#results > div > div:nth-child(2) > button:first-of-type")
        if not ppls_ids:
            return
        ppls_names = self.wd.find_elements_by_css_selector(
            "#results > div > div:nth-child(2) > div.name")
        ppls = list(zip(ppls_ids, ppls_names))
        ppl = random.choice(ppls)
        print("Invite -> ",
            self.INVITE_BUTTON.sub('id', ppl[0].get_attribute('id')),
            ' / ', ppl[1].text)
        ppl[0].click() # Invite
        return int(self.INVITE_BUTTON.sub('', ppl[0].get_attribute('id')))


    def get_new_friends(self):
        top_search = self.wd.find_element_by_css_selector("#top_search")
        top_search.click()
        time.sleep(2)

        self.select_sex()
        self.select_age(18, 40)
        self.select_region("Russia")
        self.select_city("Moscow")
        self.select_random_school()
        self.select_random_university()
        self.invite_random_people_in_search_list()





if __name__ == "__main__":
    with Login() as login:
        get_followers(login.wd)
        new_random_friends = NewRandomFriends(login.wd)
        new_random_friends.get_new_friends()














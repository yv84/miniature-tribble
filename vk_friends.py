import time
import re
import os
import random


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import select



def login():
    wd = webdriver.Firefox() # or add to your PATH
    wd.set_window_size(1024, 768) # optional
    URL = 'https://vk.com'
    wd.get(URL)

    quick_email = wd.find_element_by_css_selector("#quick_email")
    quick_email.send_keys(os.environ['VK_LOGIN'])
    time.sleep(1)

    quick_pass = wd.find_element_by_css_selector("#quick_pass")
    quick_pass.send_keys(os.environ['VK_PSW'])
    time.sleep(1)

    quick_login_button = wd.find_element_by_css_selector("#quick_login_button")
    quick_login_button.click()
    time.sleep(2)
    return wd


def get_followers(wd):
    REQUEST_CONTROLS = re.compile("request_controls_")
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


    wd.close()
    time.sleep(1)
    wd.quit()




class New_Random_Friends():
    def __init__(self, wd):
        self.wd = wd
        self.FILTER_CONTAINER = "div > div:nth-child(2) > div:nth-child(1) > ul:nth-child(1)"


    def select_region(self, desired_country):
        region_sel = self.wd.find_element_by_css_selector("#cCountry")
        region_sel.click()
        time.sleep(1)
        countries = region_sel.find_element_by_css_selector(self.FILTER_CONTAINER).find_elements_by_css_selector("* > li")
        for country in countries:
            if country.text == desired_country:
                country.click() 
                return


    def select_city(self, desired_town):
        city_sel = self.wd.find_element_by_css_selector("#cCity")
        city_sel.click()
        time.sleep(1)
        towns = city_sel.find_element_by_css_selector(self.FILTER_CONTAINER).find_elements_by_css_selector("* > li")
        for town in towns:
            if town.text == desired_town:
                town.click() 
                return


    def select_random_school(self):
        school_sel = self.wd.find_element_by_css_selector("#cSchool")
        school_sel.click()
        time.sleep(1)
        schools = school_sel.find_element_by_css_selector(self.FILTER_CONTAINER).find_elements_by_css_selector("* > li")
        school = random.choice(schools)
        school.click()
        #cSchClass
        #cSchYear
        return



    def select_random_university(self):
        university_sel = self.wd.find_element_by_css_selector("#cUniversity")
        university_sel.click()
        time.sleep(1)
        universities = university_sel.find_element_by_css_selector(self.FILTER_CONTAINER).find_elements_by_css_selector("* > li")
        university = random.choice(universities)
        university.click()
        #cUniversity
        #cFaculty
        #cChair
        #cUniYear
        #cEduForm
        #cEduStatus
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
    wd = login()
    new_random_frineds = New_Random_Friends(wd)
    new_random_frineds.get_new_friends()














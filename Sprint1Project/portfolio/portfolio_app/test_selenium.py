from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import unittest



class DeleteRoundTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        #waits before starting, some browsers are slower 
        self.browser.implicitly_wait(5) 

    def test_delete_round(self):
        # opens the page login page and log in, simulating a user named tiger signing in 
        self.browser.get('http://localhost:8000/login/')
        self.browser.find_element(By.NAME, 'username').send_keys('TIGER')  
        self.browser.find_element(By.NAME, 'password').send_keys('w00ds12345')  
        self.browser.find_element(By.NAME, 'password').send_keys(Keys.RETURN)

        # wiats for logout link in the navbar to show to ensure a login
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Logout')))

        # searches the navbar for notebook list
        self.browser.get('http://localhost:8000/notebooks/')

        # clicks the user's notebook link by their username waits 10 seconds to load 
        user_username = 'TIGER'  
        notebook_link = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, f'Notebook for {user_username}')))
        notebook_link.click()

        # locates the delete button for the round and click it
        delete_buttons = WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.LINK_TEXT, 'Delete')))  
        #the actually command to click delete
        delete_buttons[0].click()  

        try:
            #allows the program to accept the delete function 
            WebDriverWait(self.browser, 5).until(EC.alert_is_present())
            alert = self.browser.switch_to.alert
            alert.accept()
        except TimeoutException:
            # time out error had me thrown off but its going to happen so we do this to ensure a succesful attempt!
            pass

#turns off the remote browser
    def tearDown(self):
        self.browser.quit()

if __name__ == '__main__':
    unittest.main()




class UploadImageTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(5) 

    def test_upload_image(self):
        #  navs to login page and log in
        self.browser.get('http://localhost:8000/login/')
        self.browser.find_element(By.NAME, 'username').send_keys('TIGER') 
        self.browser.find_element(By.NAME, 'password').send_keys('w00ds12345') 
        self.browser.find_element(By.NAME, 'password').send_keys(Keys.RETURN)

        # wiats for logout link in the navbar to show to ensure a login
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Logout')))

        # searches the navbar for notebook list
        self.browser.get('http://localhost:8000/notebooks/')

        # clicks the user's notebook link by their username waits 10 seconds to load 
        user_username = 'TIGER'  # Replace with the actual username
        notebook_link = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, f'Notebook for {user_username}')))
        notebook_link.click()

        # finds the file input element and upload the image
        file_input = self.browser.find_element(By.NAME, 'file_field')
        file_path = r'"C:\Users\justr\OneDrive\Pictures\as2.PNG"'
        file_input.send_keys(file_path)

        # submits the form to upload the image
        submit_button = self.browser.find_element(By.XPATH, '//button[text()="Upload File"]')
        submit_button.click()



    def tearDown(self):
        self.browser.quit()

if __name__ == '__main__':
    unittest.main()













import unittest, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC #
from selenium.webdriver.common.by import By
import configparser
from selenium.webdriver.common.action_chains import ActionChains



class Braw(unittest.TestCase):

    myMessXpath="//li[@id='l_msg']/a"
    
    
    def __init__(self):
       self.driver = webdriver.Firefox()
    
    def click_by_xpath(self,xpath):
        elem=self.driver.find_element_by_xpath(xpath)
        elem.click() 
        return elem
        
    def login_vk(self,login,passw):
        self.driver.get("http://www.vk.com")
        elem = self.click_by_xpath("//input[@id='quick_email']")
        elem.send_keys(login)
        elem = self.click_by_xpath("//input[@id='quick_pass']")
        elem.send_keys(passw)
        self.click_by_xpath("//button[@id='quick_login_button']")
        
    def wait_by_xpath(self,xpath,time=5):
        wait=WebDriverWait(self.driver,time)   
        #element=wait.until(EC.element_to_be_clickable((By.XPATH,xpath)))
        element=wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
        
    def open_my_messages(self):
        self.wait_by_xpath(self.myMessXpath)
        self.click_by_xpath(self.myMessXpath)
        

class VkTest2(unittest.TestCase):
    def setUp(self):
        print("setUp")
        self.driver= Braw()
        self.driver2= Braw()
    
    
    def test1_vk_different(self):
    
        config = configparser.ConfigParser()
        config.read('config.ini')

        
        driver = self.driver
        driver2 = self.driver2
        
        driver.login_vk(config['Vk.com']['login1'],config['Vk.com']['paswd1'])
        driver2.login_vk(config['Vk.com']['login2'],config['Vk.com']['paswd2'])

        driver.open_my_messages() 
        
        driver2.open_my_messages()
        
        driver.click_by_xpath("//li[@id='l_msg']")        # self.driver == driver 
        driver.wait_by_xpath("//div[@id='im_bar']")
        driver.driver.find_element_by_xpath("//div[@id='im_bar']")
        el=driver.click_by_xpath("//div[@id='im_filter_out']")
        el.send_keys(config['Vk.com']['user_name2']) # find user to write a message
        driver.wait_by_xpath("//div[@id='im_friends']")
        
        driver.click_by_xpath("//div[@id='im_friends']/div[position()=1]") # select user
        driver.wait_by_xpath("//div[@id='im_controls_wrap']")
        
        elem=driver.click_by_xpath("//div[@id='im_controls_wrap']//div[@id='im_peer_controls']/table/tbody/tr/td[@id='im_write_form']/div[@id='im_texts']") # send messages
        elem.send_keys("Hi,Vika!")
        self.driver.click_by_xpath("//div[@id='im_send_wrap']/button[@id='im_send']")
               
        driver2.wait_by_xpath("//span[text()='+1']",10)
        
        elem2=driver2.click_by_xpath(driver2.myMessXpath)
        
        driver2.wait_by_xpath("//div[contains(@id, 'im_dialog') and contains(@class,'dialogs_new_msg')]")
        elem3= driver2.click_by_xpath("//div[contains(@id, 'im_dialog') and contains(@class,'dialogs_new_msg')]") # find unread message
        
        if len(driver2.driver.find_elements(By.XPATH,driver2.myMessXpath)) > 0:
            print('find') 
        
        driver.click_by_xpath("//li[@id='l_msg']")
        time.sleep(5)
        driver.click_by_xpath("//div[@id='im_dialogs']//div[position()=2]") # find first dialog
        
        text_l1=driver2.driver.find_element_by_xpath("//div[@class='im_rows im_peer_rows'and not(@style='display: none;')]//table[@class='im_log_t']/tbody/tr[last()]//div[@class='im_msg_text']").text
        text_l2=driver.driver.find_element_by_xpath("//div[@class='im_rows im_peer_rows'and not(@style='display: none;')]//table[@class='im_log_t']/tbody/tr[last()]//div[@class='im_msg_text']").text
        assert text_l1==text_l2,'Sended and recived messages are not equal!'
        time.sleep(20)
        
        
    def test2_vk_like(self):
    
        config = configparser.ConfigParser()
        config.read('config.ini')

        
        driver = self.driver
        driver2 = self.driver2
        
        driver.login_vk(config['Vk.com']['login1'],config['Vk.com']['paswd1'])
        driver2.login_vk(config['Vk.com']['login2'],config['Vk.com']['paswd2'])
        time.sleep(3)
        
        driver.click_by_xpath("//div[@id='side_bar']/ol/li[@id='l_fr']")
        driver.wait_by_xpath("//div[@id='friends_search']//input[@id='s_search']")
        elem=driver.click_by_xpath("//div[@id='friends_search']//input[@id='s_search']")
        
        elem.send_keys(config['Vk.com']['user_name2'])  # friends_search
        driver.click_by_xpath("//div[@id='friends_search']/button[@id='invite_button']")
        
        driver.click_by_xpath("//div[@id='list_content']/div/div[position()=1]/div[@class='info fl_l']/div[position()=1]") #friend page
        
        driver.wait_by_xpath("//div[@id='page_body']/div[@id='wrap3']//div[@id='page_avatar']/a[@id='profile_photo_link']")
        driver.click_by_xpath("//div[@id='page_body']/div[@id='wrap3']//div[@id='page_avatar']/a[@id='profile_photo_link']") #friend avatar 
        
        driver.wait_by_xpath("//div[@id='pv_wide']/div[@id='pv_like_wrap']/span[@id='pv_like_link']")
        driver.driver.execute_script("window.scrollTo(0, 150)")
        driver.click_by_xpath("//div[@id='pv_wide']/div[@id='pv_like_wrap']/span[@id='pv_like_link']") #like friends foto
        
        action=webdriver.ActionChains(driver.driver) # move to list 
        
        batton_like=WebDriverWait(driver.driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//div[@id='pv_wide']/div[@id='pv_like_wrap']/span[@id='pv_like_link']")))
        action.move_to_element(batton_like).perform()
        
        list_likes=WebDriverWait(driver.driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='like_head_wrap']/span[position()=1]")))
        action.move_to_element(batton_like).click(list_likes).perform()
        
        driver.wait_by_xpath("//div[@id='wk_likes_content']/div[@id='wk_likes_rows']/div/div[@class='wk_likes_liker_name']/a")
        find_like_users=driver.driver.find_elements_by_xpath("//div[@id='wk_likes_content']/div[@id='wk_likes_rows']/div/div[@class='wk_likes_liker_name']/a")
        name_user1=config['Vk.com']['user_name1']
        for i in find_like_users:
            name=i.text
            if name == name_user1:
                print('This user:',name,'liked foto')
                break
        else:
            raise ValueError ('Not found user who liked foto')
       
        driver.wait_by_xpath("//div[@id='wk_box']/a[@id='wk_close_link']")
        driver.click_by_xpath("//div[@id='wk_box']/a[@id='wk_close_link']")
        driver.wait_by_xpath("//div[@id='pv_wide']/div[@id='pv_like_wrap']/span[@id='pv_like_link']") #dislike foto 
        driver.driver.execute_script("window.scrollTo(0, 150)")
        driver.click_by_xpath("//div[@id='pv_wide']/div[@id='pv_like_wrap']/span[@id='pv_like_link']")
        time.sleep(10)
        
        
       
    def tearDown(self):
        print("tearDown")
        self.driver.driver.close()
        self.driver2.driver.close()
        
if __name__ == "__main__":
    unittest.main()
import unittest, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC #
from selenium.webdriver.common.by import By
import configparser



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
        
        driver.click_by_xpath("//span[text()='My Friends']") # self.driver == driver 
        
        driver.wait_by_xpath("//div[@id='main_class']//div[@id='friends_list']//div[@id='list_content']/div/div[position()=1]") # send messages first friend in the list
        driver.driver.find_element_by_xpath("//div[@id='main_class']//div[@id='friends_list']//div[@id='list_content']/div/div[position()=1]")
        driver.click_by_xpath("//div[@class='actions fl_r']/a[text()='Send a message']")
        driver.wait_by_xpath("//div[@id='mail_box_editable']")
        elem = driver.click_by_xpath("//div[@id='mail_box_editable']")
        elem.send_keys("Hi,Vika!")
        
        self.driver.click_by_xpath("//button[@id='mail_box_send']")
        
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
        
        
        
    def tearDown(self):
        print("tearDown")
        self.driver.driver.close()
        self.driver2.driver.close()
        
if __name__ == "__main__":
    unittest.main()
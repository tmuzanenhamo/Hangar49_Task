from selenium import webdriver
from getpass import getpass
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

email = "tawasdev@gmail.com"
password = "@Tawanda14"

driver = webdriver.Chrome("C:\\Dev\\ChromeDriver\\chromedriver.exe")
driver.get("https://app.woodpecker.co/login")

email_textbox = driver.find_element_by_name("login")
email_textbox.send_keys(email)
password_textbox = driver.find_element_by_name("password")
password_textbox.send_keys(password)

login_button = driver.find_element_by_class_name("w-button")
login_button.submit()

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#prospects?r=t')]")))
element.click()


span =wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Add prospects']")))
span.click()

el2 = wait.until(EC.element_to_be_clickable((By.XPATH, ("(//div[@class='MenuItem-value'])[position()=1]"))))
el2.click()

file_upload = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "gwt-FileUpload")))
file_upload.send_keys('C:\\Users\\tmuza\\Downloads\\HNGTASK\\Tech Test.xlsx')

el3 = wait.until(EC.element_to_be_clickable((By.XPATH, ("(//div[@class='gwt-Label inLineLeft fontBook16 clientAddML'])[position()=2]"))))
el3.click()

el4 = wait.until(EC.element_to_be_clickable((By.XPATH, ("(//div[@class='gwt-Label buttonGreen hand GOU11VWDI'])"))))
el4.click()

el5= wait.until(EC.element_to_be_clickable((By.XPATH, ("(//div[@class='gwt-Label buttonGreen hand GOU11VWDD'])"))))
el5.click()

el6= wait.until(EC.element_to_be_clickable((By.XPATH, ("(//div[@class='gwt-Label buttonGreen goProsBtn'])"))))
el6.click()










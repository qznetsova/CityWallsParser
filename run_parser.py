from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from data_collector import DataCollector


driver = webdriver.Chrome(ChromeDriverManager().install())
DataCollector(driver).make_address_list()
driver.close()

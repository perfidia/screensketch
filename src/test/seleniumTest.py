#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from seleshot import create
   
driver = webdriver.Firefox()    
driver.get('http://127.0.0.1:8000/webApp/')
linkControls = driver.find_elements_by_tag_name('a')
links = []

for linkControl in linkControls:
    links.append(linkControl.get_attribute('href'))

driver.close()
s = create()
s.get_screen(url='http://127.0.0.1:8000/webApp/')

for link in links:
    s.get_screen(url = link)
    
s.close()
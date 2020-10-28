from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import os

def createFolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print('Error: Creating directory. '+dir)


search = input("키워드를 입력하시오. ")
url = f'https://www.google.co.kr/search?tbm=isch&q={quote_plus(search)}'

driver = webdriver.Chrome('./driver/chromedriver')
driver.implicitly_wait(3)
driver.get(url)

num=2
for i in range(num):
    driver.execute_script("window.scrollBy(0,1000)")

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

img = soup.select('.rg_i.Q4LuWd')

n=1
imgurl = []

for i in img:
    try:
        imgurl.append(i.attrs["src"])
    except KeyError:
        imgurl.append(i.attrs["data-src"])
                      
for i in imgurl:
    dir="./images/"+search
    createFolder(dir)
    urlretrieve(i, dir+"/"+search+str(n)+".jpg")
    n+=1

driver.close()
                      


'''
Don't know what it stands for, but the tbm URL parameter appears to indicate the filter used.

For example:

Applications: tbm=app
Blogs: tbm=blg
Books: tbm=bks
Discussions: tbm=dsc
Images: tbm=isch
News: tbm=nws
Patents: tbm=pts
Places: tbm=plcs
Recipes: tbm=rcp
Shopping: tbm=shop
Video: tbm=vid
'''

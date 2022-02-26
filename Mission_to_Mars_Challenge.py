#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)
#wait_time gives the browser 1 second to load the page
#is-element_present_by_css directs to combination of <div> and <list_text> instead of separate directions


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
#Note the . between div and list_text. It sets up the different classes of <div>
# select_one shows that only 1 example will be chosen


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title
#.get_text() makes sure we download only the text we're looking for


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
#get('src') gets the link to the pic. Note that this doesn't include the full link


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url
#This is how to get the full address


# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df
#read_html goes to the correct site to look for tables [0] is the 1st table
#df.columns assigns 3 columns for the new df
#set_index sets 'description' as the index


# In[14]:


df.to_html()
#this will put the df back into html format


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[16]:


# 2. Create a list to hold the images and titles.
hemisphere_titles = []
hemisphere_image_url = []


# In[17]:


# 3a. Write code to retrieve the titles for each hemisphere.
hemisphere_titles = browser.find_by_css('h3')
#Seems lik3 h3 would be mentioned here, somewhere

for h in hemisphere_titles:    
    print(h.text)


# In[18]:


# #b) navigate to the full-resolution image page
# hemisphere_url = img_soup.find("div", class_="downloads").find("li").find("a")['href']

# #c)retrieve the full-resolution image URL string and title for the hemisphere image,
# hemisphere_image_urls = f'https://marshemispheres.com/{hemisphere_url}'
# #Add url to list hemisphere_image_urls

# hemisphere_image_urls


# In[19]:


links = browser.find_by_css('a.product-item img')

hemispheres = {}

html = browser.html
img_soup = soup(html, 'html.parser')

# 3b. Write code to retrieve the image urls for each hemisphere.
for link in range(len(links)):

    hemisphere_titles = browser.find_by_css('h3')[link].text

    #a) click on each hemisphere link    
    browser.find_by_css('a.product-item img')[link].click()

    #b) navigate to the full-resolution image page
#    hemisphere_url = img_soup.find("div", class_="downloads").find("li").find("a")['href']
    hemisphere_url = browser.find_by_text("Sample")['href']

    #c)retrieve the full-resolution image URL string and title for the hemisphere image,
#    hemisphere_url = f'https://marshemispheres.com/{hemisphere_url}'
    #Add url to list hemisphere_image_urls
    
    #get a new set of titles to insert in the dictionary
    hemispheres[hemisphere_titles] = hemisphere_url
    # Dictionary to be inserted as a MongoDB document
#     hemispheres = {
#         'title': hemisphere_titles,
#         'url': hemisphere_url
#     }
        
#     hemisphere_image_urls.append()
#     hemisphere_titles.append()
        
    
    #d) use browser.back() to navigate back to the beginning to get the next hemisphere image
    browser.back()

print(hemispheres)
    #Use print statements to observe
    #List of dictionaries


# In[20]:


browser.quit()


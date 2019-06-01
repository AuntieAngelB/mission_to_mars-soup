
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd
from flask_pymongo import PyMongo

################# Scrape Nasa.gov Mars for latest news #############
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path)

def scrape():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    #assign the variables
    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find('div', class_='content_title')

    news_title = results.text.lstrip()

    results2 = soup.find('div', class_='article_teaser_body')

    news_p = results2.text.lstrip()

    # Add results to mars dictionary

##### JPL URL ##############################################j


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    # timing to allow the page to load 
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, "html.parser")

    result=soup.find('figure',class_="lede")
    feat_image="https://www.jpl.nasa.gov"+result.a.img["src"]

######## URL for Mars Weather-Twitter ############################


    url ='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")
    result=soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars_weather_report = result

######## URL for Space Facts about Mars #######################

    url ='https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(1)

    import pandas as pd
    import requests
    html = browser.html
    soup = bs(html, "html.parser")


    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    df = tables[0]

    df.columns = ['Measurement', 'Value']

    #Set index to Measurement Column
    df.set_index('Measurement', inplace=True)
    facts = df.to_html(classes="table table-striped")

######### URL for Hemispheres of Mars ... astrogeology.usgs.gov #############
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'lxml')
    base_url ="https://astrogeology.usgs.gov"

    image_list = hemisphere_soup.find_all('div', class_='item')

    # Create list to store dictionaries of data
    hemisphere_image_urls = []

    # Loop through each hemisphere and click on link to find large resolution image url
    for image in image_list:
        hemisphere_dict = {}
        
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        browser.visit(link)
        
        time.sleep(1)
    
        hemisphere_html2 = browser.html
        hemisphere_soup2 = bs(hemisphere_html2, 'lxml')
        
        img_title = hemisphere_soup2.find('div', class_='content').find('h2', class_='title').text
        hemisphere_dict['title'] = img_title
        
        img_url = hemisphere_soup2.find('div', class_='downloads').find('a')['href']
        hemisphere_dict['url_img'] = img_url
    
        # Append dictionary to list
        hemisphere_image_urls.append(hemisphere_dict)
      


            # Store data in a dictionary
    mars_data = {
        "news_header": news_title,
        "news_body": news_p,
        "featured_image": feat_image,
        "tweet": mars_weather_report,
        "table": facts,
        "hemisphere": hemisphere_image_urls
    }

    # Return results
    return mars_data

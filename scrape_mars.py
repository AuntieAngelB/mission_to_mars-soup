import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd
from selenium import webdriver

def init_browser():
   def scrape_all():
        browser = Browser("chrome", executable_path="chromedriver", headless=True)
        news_title, news_paragraph = mars_news(browser)

def scrape_info():
    browser = init_browser()
    
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data

def mars_news(browser):
    # URL
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # timing to allow the page to load 
    time.sleep(1)

    #assign the variables
    html = browser.html
    soup = bs(html, "html.parser")

    #quit browser
    browser.quit()
    ###collect the latest News Title and Paragraph Text. 
    results = soup.find('div', class_='content_title')
    ###Assign the text to variables 
    news_title = results.text.lstrip()

    results2 = soup.find('div', class_='article_teaser_body')

    news_p = results2.text.lstrip()
    costa_data = {
        "news_title": news_title,
        "teaser_paragraph": news_p,
    }
    return costa_data

def featured_image(browser):
    # URL
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
    featured_image_url="https://www.jpl.nasa.gov"+result.a.img["src"]
    featured_image_url

    return featured_image_url

def twitter_weather(browser):

    # URL
    url ='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    result=soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    mars_weather_report = result
        mars_weather = {
        "Mars Weather Report": mars_weather_report,
    }
    return mars_weather

def mars_facts():

    # URL
    url ='https://space-facts.com/mars/'
    browser.visit(url)

    import pandas as pd
    import requests
    html = browser.html
    soup = bs(html, "html.parser")

    url = 'https://space-facts.com/mars/'

    mars_facts = pd.read_html(url)
    mars_facts

    df = mars_facts[0]
    df.columns = ['Measurement', 'Value']

    #Set index to Measurement Column
    df.set_index('Measurement', inplace=True)

    mars_facts = pd.read_html(url)

    #to_html() also can be used to create html string
    str_io = io.StringIO()

    df.to_html(buf=str_io, classes='table table-striped')

    html_str = str_io.getvalue()

    return html_str




def hemispheres(browser):

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'lxml')
    base_url ="https://astrogeology.usgs.gov"

    images = hemisphere_soup.find_all('div', class_='item')

    # Create list to store dictionaries of data
    hemisphere_image_urls = []

    # Loop through each hemisphere and click on link to find large resolution image url
    for image in images:
        hemisphere_dict = {}
        #<a href="/search/map/Mars/Viking/cerberus_enhanced" class="itemLink product-item"><h3>Cerberus Hemisphere Enhanced</h3></a>   
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

        return hemisphere_image_urls

    if __name__ == "__main__":

    # If running as script, print scraped data
###for html page https://coldplay.com/song/moving-to-mars/

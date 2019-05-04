#!/usr/bin/env python
# coding: utf-8

# # Step 1 - Scraping
#     - NASA Mars News
#         scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
#     - assign the text tp variables that you can reference later




#dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
from splinter import Browser
import time

def scrape():
   

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    mars_data = {}








#url to be scraped
    mars_news_url = "https://mars.nasa.gov/news/"

    #retrieve page with requests module
    response = requests.get(mars_news_url)
    soup = BeautifulSoup(response.text, 'html.parser')



    mars_data["mars_news_title"] = soup.find('div', class_ ='content_title').text



    nasacontent = soup.find_all('div', class_ ='rollover_description_inner')
    mars_data["mars_news_content"] = nasacontent[0].text


    #JPL Mars Space Images-Featured Image
        #use splinter to navigate the site and find the image url for the current Featured Mars image
        #assign the url string to a variable called "featured_image_url"
        #make sure to find the image url to the full size .jpg image
        #make sure to save a complete url string for this image
        
    space_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(space_image_url)

    response2 = requests.get(space_image_url)
    soup2 = BeautifulSoup(response2.text, 'html.parser')

    featured_image = soup2.find('article', class_='carousel_item')
    url = featured_image['style']

    splitter=url.split(" ")

    url_split = splitter[1]

    url_split2 = url_split.split("'")

    image_url = url_split2[1]
    image_url

    mars_data["featured_image_url"] = f"https://www.jpl.nasa.gov{image_url}"
   


 


    #Mars Weather
        #Scrape the latest Mars weather tweet. Save the tweet text from the weather report as a variable called "mars_weather"

    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    response3 = requests.get(twitter_url)
    soup3 = BeautifulSoup(response3.text, 'html.parser')
    mars_weather = soup3.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_data["mars_weather_tweet"] = mars_weather.text





    #Mars Facts
        #Use pandas to scrape the table containing facts about the planet including Diameter, Mass, etc
        #Use pandas to convert data to a HTML table string
    facts_url = "https://space-facts.com/mars/"
    mars_data["facts_table"] = pd.read_html(facts_url)
    



    df = mars_data["facts_table"][0]
    df.columns=['description','value']
    df.set_index('description', inplace=True)

    mars_data["facts_table"] = df.to_html()



    #Mars Hemispheres
        #Obtain high resolution images for each of Mars' hemispheres
        #Save both image url string for the full resolution image and title containg hemisphere name
        #Use Python dictionary to store the data using the keys img_url and title
        #Append dictionary w/image url string and hemisphere title to a list

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    response4 =requests.get(hemisphere_url)
    soup4 = BeautifulSoup(response4.text, 'html.parser')
    hemisphere_images = soup4.find_all('img', class_="thumb")
    hemisphere_images



    hemisphere_image_urls=[]
    for image in hemisphere_images:
        temp = {}
        img=image['alt'].split()[:-2]
        temp['title']=" ".join(img)
        temp['img_url']=f"https://astrogeology.usgs.gov{image['src']}"
        hemisphere_image_urls.append(temp)

    print(hemisphere_image_urls)

    mars_data['hemisphere_images'] = hemisphere_image_urls

    return mars_data

if __name__ == "__main__":
    scrape()




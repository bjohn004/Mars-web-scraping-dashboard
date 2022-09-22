# import splinter and bs4
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape():
    # NASA Mars News Scraping w/SPLINTER
    #----------------------------------------------------------------------------------
    # Set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # define soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Generate results based on list_text class
    results = soup.find_all('div', class_='list_text')

    # create empty list for all the articles
    dates=[]
    titles=[]
    paragraphs=[]

    # run loop to see all of the results of article on the home page
    for result in results:
        date = result.find('div', class_='list_date').text
        title = result.find('div', class_='content_title').text
        paragraph = result.find('div', class_='article_teaser_body').text

        # fill in empty lists
        dates.append(date)
        titles.append(title)
        paragraphs.append(paragraph)

    # the first item of each list is the most recent article
    most_recent_title=titles[0]
    most_recent_paragraph=paragraphs[0]

    browser.quit()
    #----------------------------------------------------------------------------------

    # JPL MARS SPACE IMAGES SCRAPING w/SPLINTER
    #----------------------------------------------------------------------------------
    # setup splint/browser info
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # define soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Generate results based on list_text class
    results = soup.find_all('img', class_='headerimage')
    url_tag = results[0]['src']
    jpl_img_url = url + url_tag
    browser.quit()
    #----------------------------------------------------------------------------------


    # MARS FACTS SCRAPING w/PANDAS
    #----------------------------------------------------------------------------------
    # define url
    url = 'https://galaxyfacts-mars.com/'

    # read in html as tables and define as DF
    tables = pd.read_html(url)
    mars_info = tables[0]

    # convert table to html
    mars_html = mars_info.to_html(index=False, header=False)
    
    #----------------------------------------------------------------------------------

    # MARS HEMISPHERES SCRAPING w/SPLINTER
    #----------------------------------------------------------------------------------
    # setup splinter/browser info
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = "https://marshemispheres.com/"
    browser.visit(url)
    hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']
    hemisphere_img = []
    hemi_dict ={}

    # loop through hemispheres to complete lists
    for hemisphere in hemispheres:
        # from home page find first hemisphere and go to page
        browser.links.find_by_partial_text(hemisphere).click()  
        # define soup for that page
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        # find url for the image
        results = soup.find_all('img', class_='wide-image')
        #define url
        img_url = results[0]['src']
        # go back to home page
        browser.back()
        # fill in empty dictionary and lists
        hemi_dict = dict()
        hemi_dict['title'] = hemisphere + " Hemisphere"    
        hemi_dict['img_url'] = url + img_url
        hemisphere_img.append(hemi_dict)

    browser.quit()
    #----------------------------------------------------------------------------------

    #define dictionary containing all scraped elements
    mars_dictionary = {"mars_news_title": most_recent_title, 
                    "mars_news_text": most_recent_paragraph,
                    "jpl_featured_image": jpl_img_url,
                    "mars_table": mars_html,
                    "mars_hemispheres": hemisphere_img}

    return mars_dictionary
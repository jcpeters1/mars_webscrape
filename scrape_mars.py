from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=True)

def scrape_info():
    #mars news
    mars_data = {}

    mars_data['news'] = mars_news_data()

    mars_data['featured_img_url'] = featured_img()

    mars_data['fact_table'] = mars_table()

    mars_data['hemisphere_imgs'] = hemisphere_imgs()

    return mars_data

def mars_news_data():
    news_data = {}
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(2)
    news = soup.find_all('div', class_='content_title')
    news_para = soup.find_all('div', class_="article_teaser_body")
    browser.quit()

    news_title = news[1].text
    news_p = news_para[0].text

    #news_data['title'] = news_title
    #news_data['para'] = news_p

    return news_title, news_p

def featured_img():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    click_url = browser.url
    browser.visit(click_url)
    click_html = browser.html
    click_soup = bs(click_html, 'html.parser')
    featured_img = click_soup.find('figure')
    browser.quit()
    featured_img_path = featured_img.a.img['src']
    featured_img_url = base_url + featured_img_path

    return featured_img_url

def mars_table():
    pd_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(pd_url)
    mars_info = mars_table[0]
    html_table = mars_info.to_html(header=False, index=False)

    return html_table

def hemisphere_imgs():
    browser = init_browser()
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    title = soup.find_all('h3')
    links = soup.find_all('a', class_='itemLink product-item')
    browser.quit()

    base_url = 'https://astrogeology.usgs.gov'
    link_urls = []
    i=1
    for link in links:
        link_urls.append(base_url + link['href'])

    for x in range(4):
        link_urls.remove(link_urls[x])

    titles = []
    for item in title:
        titles.append(item.text)

    browser = init_browser()
    time.sleep(1)
    images = []
    for link in link_urls:
        browser.visit(link)
        time.sleep(1)
        url = browser.url
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        img = soup.find('img', class_='wide-image')['src']
        img_url = base_url + img
        images.append(img_url)
    
    browser.quit()

    hemisphere_img_urls = []
    for x in range(4):
        dict = {}
        title = titles[x]
        image = images[x]
        dict['title'] = title
        dict['img_url'] = image
        hemisphere_img_urls.append(dict)

    print(hemisphere_img_urls)

    return hemisphere_img_urls


    if __name__ == "__main__":
        app.run(debug=True)
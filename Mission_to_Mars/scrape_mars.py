from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import urllib


######################
def init_browser():
    executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
    return Browser("chrome",**executable_path, headless = True)


######################################
def scrape_nasa():
    browser = init_browser()
    
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    grid = soup.find('div',{'class':'grid_layout'})
    
    article = grid.find_all('div', {'class':'list_text'})[0]
    
    news_title = article.find('div',{'class':'content_title'}).get_text()
    
    news_p = article.find('div',{'class':'article_teaser_body'}).get_text()
    
    return news_title, news_p


########################################
def scrape_jpl():
    browser = init_browser()
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    container = soup.find('div', class_ = 'carousel_container')
    image = container.find_all('article', class_ = 'carousel_item')[0]['style']
    
    featured_image_url = image.split('url(')[1]
    
    featured_image_url = featured_image_url.strip(')')
    featured_image_url = featured_image_url.strip("'")
    featured_image_url = featured_image_url.strip(';')
    featured_image_url = featured_image_url.strip(')')
    featured_image_url = featured_image_url.strip("'")
    
    return featured_image_url


################################
def scrape_twitter():
    browser = init_browser()
    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    soup = soup.find('div', {'class':'css-1dbjc4n'})
    article = soup.find_all('article')[0]
    tweets = article.find_all('span', class_ = 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    
    for item in tweets:
        if len(item.get_text()) > 50:
            return item.get_text()


###################################
def scrape_facts():
    url = 'https://space-facts.com/mars/'

    facts_data = pd.read_html(url)
    new_data = []
    for frame in facts_data:
        new_dict = {}
        for index, row in frame.iterrows():
            new_dict[row[0]] = row[1]
        new_data.append(new_dict)
    return new_data

###############################
def find_hemi(browser, link):
    url = f'https://astrogeology.usgs.gov{link}'
    
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    soup = soup.find_all('li')[0]
    image_url = soup.find('a',{'target':'_blank'})['href']
    
    return image_url

def scrape_hemis():
    browser = init_browser()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    container = soup.find('div',{'class':'container'})
    table = container.find('div',{'class':'collapsible results'})
    hemispheres = table.find_all('div',{'class':'description'})
    new_hemispheres = []
    for hemi in hemispheres:
        new_hemispheres.append(hemi.find('a',{'class':'itemLink product-item'})['href'])
    image_links = []
    for hemi in new_hemispheres:
        image_links.append(find_hemi(browser, hemi))
    for url in image_links:
        urllib.request.urlretrieve(url, f"Resources/{url.split('/')[-1].split('.')[0]}.jpg")
    return image_links


######################
def scrape_master():
    data_dict = {}

    data_dict['nasa_data'] = scrape_nasa()
    data_dict['jpl_data'] = 'https://www.jpl.nasa.gov' + scrape_jpl()
    data_dict['weather_data'] = scrape_twitter()
    data_dict['facts_data'] = scrape_facts()
    data_dict['hemisphere_images'] = scrape_hemis()

    return data_dict

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_images(browser)
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

   # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

   # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p


def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemisphere_images(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    hemi_soup = soup(html, 'html.parser')


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    testy=[]
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    res_collapse=hemi_soup.find('div', class_='collapsible')
    pages=res_collapse.find_all('div', class_='item')
    try:
        for page in pages:
            p_rel_url=page.find('a',href=True)
            p_url=(url+p_rel_url['href'])
            #print(p_url)
            browser.visit(p_url)
            browser.is_element_present_by_css('div.list_text', wait_time=1)
            new_html=browser.html
            ima_soup=soup(new_html,'html.parser')
            ima_spot=ima_soup.find('img',class_='wide-image')
            ima_url=(url+ima_spot['src'])
            title_spot=ima_soup.find('h2', class_='title').get_text()
            hemisphere_image_urls.append({'img_url':ima_url,
                        'title':title_spot})
    except:
        return None

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


# # Visit the mars nasa news site
# url = 'https://redplanetscience.com'
# browser.visit(url)
# # Optional delay for loading the page
# browser.is_element_present_by_css('div.list_text', wait_time=1)

# #Convert the browser html to a soup object
# html = browser.html
# news_soup = soup(html, 'html.parser')
# slide_elem = news_soup.select_one('div.list_text')

# #slide_elem.find('div', class_='content_title').get_text()
# news_title = slide_elem.find('div', class_='content_title').get_text()
# news_title

# #find paragraph text
# news_p=slide_elem.find('div', class_='article_teaser_body').get_text()
# news_p


# ## Featured Images

# # Visit URL
# url = 'https://spaceimages-mars.com'
# browser.visit(url)



# # Find and click the full image button
# full_image_elem = browser.find_by_tag('button')[1]
# full_image_elem.click()


# # Parse the resulting html with soup
# html = browser.html
# img_soup = soup(html, 'html.parser')


# # Find the relative image url
# img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
# img_url_rel

# # Use the base URL to create an absolute URL
# img_url = f'https://spaceimages-mars.com/{img_url_rel}'
# img_url

# ## Mars Facts

# df = pd.read_html('https://galaxyfacts-mars.com')[0]
# df.columns=['description', 'Mars', 'Earth']
# df.set_index('description', inplace=True)
# df


# df.to_html()



# browser.quit()


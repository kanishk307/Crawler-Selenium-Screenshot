import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

# Set to uniquely store internal and external urls
internal_urls = set()
external_urls = set()


def is_url_valid(url):
   #Checks if the url is valid or not
    parsedURL = urlparse(url)
    return bool(parsedURL.netloc) and bool(parsedURL.scheme)

#The above function works as follows. We check if the scheme is present and there is a value in the network location part
# url = "https://umd.edu/virusinfo"
# urlparse(url)
# ParseResult(scheme='https', netloc='umd.edu', path='/virusinfo', 
# params='', query='', fragment='')


#The function gives all urls
def get_all_urls(url):
    urls = set()
    # domain name of the URL without the protocol (umd.edu in this case)
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            #href is empty and we don't need that a element
            continue
        #if the link is not absolute, make it by joining relative to the base
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        #constructing an absolute URL from parsed data
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_url_valid(href):
            #in valid url
            continue
        if href in internal_urls:
            #it is already in the set, so we don't need to add
            continue
        if domain_name not in href:
            #it is an external link. i.e
            # Check if it is already there 
            if href not in external_urls:
                print(f"[EXT] External link: {href}")
                external_urls.add(href)
            continue
        print(f"[INT] Internal link: {href}")
        urls.add(href)
        internal_urls.add(href)
    return urls


total_urls_visited = 0

def crawl(url, max_urls=50):
    #Max URL is just to decrease the time if there are a lot of pages.
    #The following code was openly available of github and I found this
    #idea useful to inhibit crawling time
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_urls(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)


#base_url = "https://umd.edu/virusinfo"
base_url = input("Enter the URL : ")
#getting the netloc+path
parsedurl = urlparse(base_url)
# base_url_text = base_url.split("//",1)[1]
base_url_text = parsedurl.netloc+parsedurl.path ##umd.edu/virusinfo
# base_url_text_domain = base_url_text.split("/",1)[0]
base_url_text_domain = parsedurl.netloc ##umd.edu


crawl(base_url)
print("[EXT] Total External links:", len(external_urls))
print("[INT] Total Internal links:", len(internal_urls))
print("[TOT] Total:", len(external_urls) + len(internal_urls))


immediate_urls = [] #Linked Associated with the current page, https://umd.edu/virusinfo/ in this case

for url in internal_urls:
    if base_url_text in url:
        immediate_urls.append(url)

for immediate_url in immediate_urls:
    print(f'{immediate_url}\n') #To see which URLs will be crawled

count = 0
name_of_folder = f'{base_url_text_domain}_Screenshots'
for i in immediate_urls:
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options,executable_path='chromedriver.exe') # #Local Path of chrome driver
    url = i
    file_name = url.replace(base_url,'')
    file_name = file_name.replace('/','')
    print(f'Visiting {base_url_text}/{file_name}')
    print(f'...Taking a screenshot')
    driver.get(url)
    if not os.path.exists(name_of_folder):
        os.makedirs(name_of_folder)
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment                                                                                                                
    driver.find_element_by_tag_name('body').screenshot(f'{name_of_folder}\\{base_url_text_domain}-{file_name}.png')
    print(f'Screenshot of {file_name} page taken! \n')
    driver.quit()

print(f'Task Completed! Files stored in the {name_of_folder} Folder')
    
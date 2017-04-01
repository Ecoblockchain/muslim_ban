from xvfbwrapper import Xvfb                                                    
from selenium import webdriver                                                  
from selenium.common.exceptions import NoSuchElementException                   



def get_youtube_links(query, max_videos=10, virtuald=False):

    if virtuald:                                                                
        vdisplay = Xvfb()                                                       
        vdisplay.start()

    driver = webdriver.Firefox()
    url = 'https://www.youtube.com/results?search_query='
    url = url + query.replace(' ', '+')
    driver.get(url)                                                     

    links = []
    while len(links)<max_videos:
        try:
            driver.implicitly_wait(3)
        
            # get video links
            videos = driver.find_elements_by_xpath(
                '//h3[@class="yt-lockup-title "]/a')
            for video in videos:
                links.append( video.get_attribute('href') )

            # go to next page
            next_page = driver.find_elements_by_xpath(
                '//div[@class="branded-page-box search-pager  spf-link "]/a')
            next_page[-1].click()

        except NoSuchElementException as e:
            continue

    driver.close()
    if virtuald:
        vdisplay.stop()
    return links

if __name__=='__main__':

    query = 'naruto singing'
    get_youtube_links(query, max_videos=10, virtuald=False)

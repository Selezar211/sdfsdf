

from robobrowser import RoboBrowser


global Front_Page_Urls 
global Front_Page_Img 


def nhentai(keyword, PageNum):

    global Front_Page_Urls
    global Front_Page_Img

    Front_Page_Urls = []
    Front_Page_Img = []

    domain = 'https://nhentai.net'
    base_url = 'https://nhentai.net/search/?q=english+-yaoi+-lolicon+'+keyword +'&page=' + PageNum
    print (base_url)

    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(base_url)

    container = browser.find('div', {'class':'container index-container'})
    all_links = container.find_all('a', href=True)

    count = 0
    while (count<len(all_links)):
        full_string = domain+all_links[count]['href']
        #print (full_string)
        Front_Page_Urls.append(full_string)
        count+=1
    print ('Finished collecting all urls. Now getting front images..')

    for url in Front_Page_Urls:
        ExtractFirstImage(url)

    return (Front_Page_Urls, Front_Page_Img)



def ExtractFirstImage(url):

    global Front_Page_Urls
    global Front_Page_Img

    domain = 'https://nhentai.net'
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')

    #print ('Extracting img from URL: '+url)
    while True:

        browser.open(url)

        thumbnail_container = browser.find('div', {'id':'thumbnail-container'}) 

        if thumbnail_container==None:
            print ('REDOING LOOP')
        else:
            break

    all_links = thumbnail_container.find_all('a', href=True)
    

    First_page_link = domain + str(all_links[0]['href'])

    OpenComic(First_page_link)



def OpenComic(url):

    global Front_Page_Urls
    global Front_Page_Img

    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    res = 'NOTHING'
    while True:
        print ('Opening comic with url: ' + url)

        browser.open(url)

        IMG_ = browser.find_all('img', src=True)

        for walao in IMG_:
            if 'logo' not in walao['src'] and 'galleries' in walao['src']:
                res = walao['src']

        print (res)

        if res=='NOTHING':
            pass
        else:
            break

    Front_Page_Img.append(res)




if __name__ == '__main__':
    result = nhentai('shota', '1')

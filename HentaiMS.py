


from robobrowser import RoboBrowser


def HentaiMS(keyword, PageNum):

    all_comic_links = []

    base_URL = 'http://search.hentai.ms/?tag=' + keyword + '&num=' + PageNum +'8&related=&pages=&box=14&es=14'
    print (base_URL)
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')

    browser.open(base_URL)

    td = browser.find_all('td', {'id':'search_gallery_item'})
    print (len(td))


    for line in td:

        this_link = line.find_all('a', href=True)
        
        try:
            if 'tags' not in this_link[1]['href']:
                print (this_link[1]['href'])
                all_comic_links.append(this_link[1]['href'])
        except:
            pass

    return all_comic_links

def OpenFirstImage(url):

    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(url)

    table = browser.find('table', {'class':'search_gallery'})

    links = table.find_all('a', href=True)

    FirstPage = links[0]['href']

    print (FirstPage)

    return FirstPage

def ExtractImageURL(url):

    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(url)

    center = browser.find_all('center')

    nested_center = center[1].find('center')

    Img_SRC = nested_center.find('img', src=True)

    print (Img_SRC['src'])

    return Img_SRC['src']

def GetThumbnailsANDLinks(keyword, PageNum):
    '''this will be called to fetch the pages comic links and their first image'''

    this_keyword = keyword
    this_PageNum = PageNum

    result_list = []

    Collected_Comic_Links = HentaiMS(this_keyword, this_PageNum)

    for comic in Collected_Comic_Links:
        my_url = OpenFirstImage(comic)
        fin_img = ExtractImageURL(my_url)
        result_list.append(comic + '|' + fin_img)

    return result_list


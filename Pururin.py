

from robobrowser import RoboBrowser


def Pururin():

    Front_Page_URLS = []
    Front_Page_Img = []

    base_URL = 'http://pururin.us'
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(base_URL)

    gallery = browser.find('ul', {'class':'gallery-list'})

    all_links = gallery.find_all('a', href=True)
    all_image = gallery.find_all('img', src=True)

    count = 0
    while (count<len(all_links)):

        if 'gallery' in all_links[count]['href']:
            Front_Page_URLS.append(base_URL+all_links[count]['href'])
            Front_Page_Img.append(base_URL+all_image[count]['src'])

        count+=1

    return (Front_Page_URLS,Front_Page_Img)


def GetFirstComicImage(url = 'http://pururin.us/gallery/32609/hakusen-to-sumizome.html'):
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(url)

    container = browser.find('ul', {'class':'thumblist shit'})
    Link_list = container.find_all('a',href=True)

    Img_Big_Url = 'http://pururin.us'+str(Link_list[0]['href'])

    return (Img_Big_Url)

def ExtractBigImage(url='http://pururin.us/view/32338/1/kimi-wa-kanojo-no-kanrika-ni-iru.html'):
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(url)

    All_img = browser.find_all('img',src=True)

    for line in All_img:
        print (fix_bad_unicode(line))



def fix_bad_unicode(el):  
    return el.decode(None, 'utf8').encode('iso2022_jp').decode('utf8')



if __name__ == '__main__':
    ExtractBigImage()

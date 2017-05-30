 

from robobrowser import RoboBrowser
from Utility import *
import multiprocessing

def GetAllComics(keyword, PageNum):

    split_keyword = keyword.split(' ')

    new_keyword = split_keyword[0]
    icount = 1
    while len(split_keyword)>icount:
        new_keyword += '%20' + split_keyword[icount]
        icount+=1

    with open('LUSCIO.txt', 'w') as f: 
        pass

    domain = 'https://luscious.net'
    Base_URL = 'https://luscious.net/c/hentai_manga/albums/text/' + new_keyword + '/page/' + PageNum + '/'

    print (Base_URL)

    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(Base_URL)

    all_comic_containers = browser.find_all('div', {'class':'item_cover'})

    jobs = []
    for each_comic in all_comic_containers:
        half_link = each_comic.find('a', href=True)
        full_link = domain+(half_link['href'])
        name = half_link['title']
        p = multiprocessing.Process(target=MultiProcDelegate, args=(full_link, name, ))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    with open('LUSCIO.txt', 'r') as f: 
        data = f.read().splitlines()

    return data

def MultiProcDelegate(full_link, name):

    try:
        print ('Starting job for comic: '+name)
    except UnicodeError:
        print ('Starting job for comic with weird name lul')
    Thumbnail = FetchFirstImage(full_link)
    Full_String = Thumbnail + '|' + full_link + '|' + name

    with open('LUSCIO.txt', 'a') as f: 
        try:
            f.write(Full_String +'\n') 
        except UnicodeEncodeError:
            print ('Ran into unicode encoding error. Passing it cause aint nobody got time for dat.')
            pass

def FetchFirstImage(url):

    domain = 'https://luscious.net'
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(url)

    wrapper = browser.find('div', {'class':'album_cover_item'})

    link = domain + wrapper.find('a', href=True)['href']

    browser.open(link)

    container = browser.find('div', {'class':'ic_container'})

    img_link = container.find('img', src=True)

    return img_link['src']

def FetchImagesForOneComic(BASE_URL):

    with open('LUSCIO_One_Comic.txt', 'w') as f: 
        print (f)

    Split_URL = BASE_URL.split('/')

    Craft_Input_Url = 'https://luscious.net/c/hentai_manga/pictures/album/'+Split_URL[4]+'/page/'

    print (Craft_Input_Url)

    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')

    jobs = []
    counter = 1
    while True:
        index = 0
        print ('Searching for number of pages')
        Working_URL = Craft_Input_Url + str(counter) +'/'
        print (Working_URL)
        browser.open(Working_URL)

        Thumbnail_Container = browser.find_all('div', {'class':'item thumbnail ic_container'})

        if (len(Thumbnail_Container)==0):
            break

        for item in Thumbnail_Container:
            img_link = item.find('a', href=True)['href']

            p = multiprocessing.Process(target=MProcess, args=(index, counter, img_link, ))
            index+=1
            jobs.append(p)
            p.start()

        counter+=1

    for proc in jobs:
        proc.join()

    with open('LUSCIO_One_Comic.txt', 'r') as f: 
        data = f.read().splitlines()

    result = (sorted(data, key=ExtractNumberFromURLforLuscio))

    return result


def MProcess(index, counter, url):

    domain = 'https://luscious.net'
    print ('Starting job on index: ' + str(index))
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(domain+url)

    container = browser.find('div', {'class':'ic_container'})

    img_link = container.find('img', src=True)

    string_to_write = 'Index:' + str(index) + '|' + 'Counter:' + str(counter) + '|' + img_link['src']
    with open('LUSCIO_One_Comic.txt', 'a') as f: 
        f.write(string_to_write +'\n') 


if __name__ == '__main__':
    # walao = GetAllComics('Apron Naruto', '1')

    walao = FetchImagesForOneComic('https://luscious.net/albums/naruto-saboten-nindou-2-deutschgerman_280789/')

    for line in walao:
        print (line)









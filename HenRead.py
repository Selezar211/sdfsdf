

from robobrowser import RoboBrowser
import multiprocessing
import math
import time
from Utility import *


def HenRead(genre, PageNum):

    with open('HenR.txt', 'w') as f: 
        pass

    Comic_URLS = []

    if 'shota' in genre:
        base_url = 'http://hentairead.com/hentai-list/male/'+str(genre)+'/last-updated/'+str(PageNum)+'/'
    else:
        base_url = 'http://hentairead.com/hentai-list/female/'+str(genre)+'/last-updated/'+str(PageNum)+'/'

    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    print ('BASE URL IS: ' + base_url)
    browser.open(base_url)

    table = browser.find('ul', {'class':'mng-list-thumb'})

    all_links = table.find_all('a', href=True)

    for line in all_links:
        print (line['href'])
        Comic_URLS.append(line['href'])

    print ('Starting collection of image thumnails..')

    jobs = []
    for walao in Comic_URLS:
        p = multiprocessing.Process(target=ExtractFirstImg, args=(walao,))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    with open('HenR.txt', 'r') as f: 
        data = f.read().splitlines()

    return data

def ExtractFirstImg(url):

    final_res = ''

    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(url)

    read_button = browser.find('div', {'class':'read-now'})

    link = read_button.find('a', href=True)

    ComicFirstPage = link['href']

    browser.open('http://tools.prowebguru.com/free-online-image-extractor/free_online_image_extractor_tool.php')

    form = browser.get_forms({'class':'form-horizontal'})

    this_form = form[0]

    this_form["website"] = ComicFirstPage

    browser.submit_form(this_form)

    img_links = browser.find_all('img', src=True)

    for line in img_links:
        if '/tbn/' not in line['src']:
            final_res = line['src'] + '|' + url

    print (final_res)

    with open('HenR.txt', 'a') as f: 
        f.write(final_res+'\n') 
    

def ExtractAllComicImages(url):

    with open('HenRUniqueComic.txt', 'w') as f: 
        print (f)

    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(url)

    read_button = browser.find('div', {'class':'read-now'})

    link = read_button.find('a', href=True)

    ComicFirstPage = link['href']

    browser.open(ComicFirstPage)

    Select_element = browser.find('select', {'class':'cbo_wpm_pag'})
    options = Select_element.find_all('option')

    page_numbers = (options[-1].text)

    All_Pages = CraftAllComicPages(url, page_numbers)

    '''figure out how many segments we need to split all the pages, 35 pages is one block download'''
    print (len(All_Pages))
    Segments = int(math.ceil(len(All_Pages)/35))
    print (Segments)

    '''split the list'''
    Segment_list_container = GeneralSplitList(All_Pages, Segments)

    for unique_segment in Segment_list_container:
        jobs = []
        for page in unique_segment:
            print ('Starting job for page '+ str(page))
            p = multiprocessing.Process(target=ExtractONEPAGE, args=(page,))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()

        time.sleep(2)

    print ('Finished all jobs. Now returning them all as unsorted list..')

    with open('HenRUniqueComic.txt', 'r') as f: 
        data = f.read().splitlines()

    print ('Now sorting them and returning that..')

    sorted_result = SortHenRUniqueComic(data)

    return sorted_result



def ExtractONEPAGE(page):

    final_res = ''
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')

    while True:
        print ('loop')
        browser.open('http://tools.prowebguru.com/free-online-image-extractor/free_online_image_extractor_tool.php')

        form = browser.get_forms({'class':'form-horizontal'})

        if len(form)!=0:
            print ('broke')
            break

    this_form = form[0]

    this_form["website"] = page

    browser.submit_form(this_form)

    img_links = browser.find_all('img', src=True)

    for line in img_links:
        if '/tbn/' not in line['src'] and '.wp.com' in line['src']:
            final_res = line['src'] 
            print (final_res)

    if final_res!='':
        with open('HenRUniqueComic.txt', 'a') as f: 
            f.write(final_res+'\n') 


def CraftAllComicPages(Base_Comic_URL, Number_Of_Pages):
    func_url = Base_Comic_URL + '1/'

    All_Pages_List = []

    for i in range(1,(int(Number_Of_Pages)+1)):
        this_page = func_url + str(i) +'/'
        All_Pages_List.append(this_page)

    return All_Pages_List


if __name__ == '__main__':
    lul = ExtractAllComicImages('http://hentairead.com/natsumitsu_x_harem/')

    #lul = ExtractAllComicImages('http://hentairead.com/accelerando/')


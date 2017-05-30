

from robobrowser import RoboBrowser
import multiprocessing
import random
import TMemory as TM
import requests
import os


def main(keyword):
    domain_name = 'http://rule34.paheal.net'
    print (domain_name)
    keyword = keyword

    '''create folder in current working directory with keyword name'''
    if not os.path.exists(keyword):
        os.makedirs(keyword)

    '''now change current working directory to this pathway'''
    current_directory = os.getcwd()
    new_directory = str(current_directory) + '\\' + str(keyword)
    os.chdir(new_directory) # Provide the path here

    web_address = 'http://rule34.paheal.net/post/list/' + str(keyword) + '/1'
    print (web_address)
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    browser.open(web_address)

    '''find how many pages this keyword has'''
    print ('Finding number of pages contained by this keyword..')
    page_nav = browser.find('section', {'id':'paginator'})
    if page_nav==None:
        print ('Could not find any with matching keyword. Please research with changed parameters..')
    links = page_nav.find_all('a', href=True)

    for line in links:
        if line.text=='Last':
            split = line['href'].split('/')
            number_of_pages = split[-1]

    print ('This keyword has ' + str(number_of_pages) + ' number of pages..')

    '''Generate all the pages with the page number'''
    Pages_To_Traverse = []

    for i in range(1, (int(number_of_pages)+1)):
        crafted_urls = 'http://rule34.paheal.net/post/list/' + str(keyword) + '/' + str(i)
        print (crafted_urls)
        Pages_To_Traverse.append(crafted_urls)

    '''store list to download in TMemory'''
    TM.Store_List_Data('FrontPagesToTraverse', Pages_To_Traverse)

    '''before multiprocessing will segment all the web pages into groups of 30 to not overwhelm processor'''
    Starting_point_of_array = 0
    Number_of_segments = round((len(Pages_To_Traverse)+1)/30)

    '''START MULTIPROCESSING HERE TO PARALLELY DOWNLOAD ALL THESE FRONT PAGES'''
    for segment in range(0, Number_of_segments):
        jobs = []

        Ending_point_of_array = (Starting_point_of_array+30)
        if Ending_point_of_array>len(Pages_To_Traverse):
            '''if ending point goes over length of array then reset it to length'''
            Ending_point_of_array = len(Pages_To_Traverse)

        for i in range(Starting_point_of_array, Ending_point_of_array):
            print ('Starting job number: ' + str(i))
            p = multiprocessing.Process(target = Download_Images_From_This_Link, args=(Pages_To_Traverse[i],))
            jobs.append(p)
            p.start()

        Starting_point_of_array+=30
        TM.Store_Single_Data(str(segment), 'Finished')

    print ('All jobs have been started..')

def Download_Images_From_This_Link(Link):
    domain_name = 'http://rule34.paheal.net'
    all_img_links = []
    print ('Working on current page: ' + str(Link))
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')
    try:
        browser.open(Link)
    except:
        print ('Failed to open link: ' + str(Link))
        print ('Trucking on..')
        pass

    image_link = browser.find_all('a', {'class':'shm-thumb-link'}, href=True)

    for line in image_link:
        full_link = domain_name + line['href'] 
        print (full_link)
        all_img_links.append(full_link)

    '''now open each of these image links and download the image in them'''
    name = random.randint(0,1000000)
    for img in all_img_links:
        try:
            browser.open(img)
            main_img = browser.find('img', {'id':'main_image'} , src=True)
            print (main_img['src'])

            img_data = requests.get(main_img['src']).content
            with open(str(name) +'.jpg', 'wb') as handler:
                handler.write(img_data)

            name+=1

        except:
            pass

    print ('This job has finished..')


if __name__ == '__main__':
    main('Tsunade')


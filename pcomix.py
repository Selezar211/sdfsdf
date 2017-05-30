

from robobrowser import RoboBrowser
import requests

def main():
    url = 'http://www.porncomix.info/milky-milk-2-dragon-ball-z-english/'
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')

    browser.open(url)

    wrapper = browser.find('div', {'id':'gallery-1'})
    imgs = wrapper.find_all('a', href=True)

    img_list = []

    for line in imgs:
        img_list.append(line['href'])


    name = 1
    for line in img_list:
        browser.open(line)
        wrapper_div = browser.find('div', {'class':'attachment-image'})
        my_img = wrapper_div.find('img', src=True)

        img_data = requests.get(my_img['src']).content
        with open(str(name) +'.jpg', 'wb') as handler:
            handler.write(img_data)

        name+=1

        with open('Walao.txt', 'a') as f:
            f.write(my_img['src'] + '\n')

            print (my_img['src'])



if __name__ == '__main__':
    with open('Walao.txt', 'w') as f:
        print ('deleted walao')
    main()



from robobrowser import RoboBrowser




def FenHen(keyword):

    result_urls = []

    base_URL = 'http://fenhentai.blogspot.co.uk/search?q='+keyword
    browser = RoboBrowser(history=True,parser='html.parser',user_agent='Chrome/41.0.2228.0')

    while True:
        browser.open(base_URL)

        post_body_list = browser.find_all('div', {'class':'post-body entry-content'})

        for post in post_body_list:
            this_image = post.find('img',src=True)
            print (this_image['src'])
            result_urls.append(this_image['src'])

        Next_Post_Link = browser.find('a', {'class':'blog-pager-older-link'}, href=True)

        if (Next_Post_Link==None):
            break
        else:
            base_URL=Next_Post_Link['href']


    return result_urls    
 

if __name__ == '__main__':
    walao = FenHen('sakura')


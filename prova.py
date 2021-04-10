import os
import time

url= 'https://www.amazon.com/s?k=welder&page=3&qid=1617181389&ref=sr_pg_3'

"""urlPath= urlsplit(url)
values = parse_qs(urlsplit(url).query)
print(values)
#anche questo per ricomporre l'url
o = urlparse(url)
query = parse_qs(o.query)
# extract the URL without query parameters
urlz = o._replace(query=None).geturl()
print(urlz)

if (urlz in url):
    print(True)
    """

def scroll(driver , timeout,safetytime):
        scroll_pause_time = timeout
        beginTime= time.time()

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            print(time.time()-beginTime)
            if(time.time()-beginTime >= safetytime):
                return
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            try:
                time.sleep(scroll_pause_time)
            except:
                print("need more timeout")
                return

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            print(new_height, last_height)
            if abs(new_height - last_height)<=5:#fixing?
                # If heights are the same it will exit the function
                return
            last_height = new_height

def pagination(driver,urlPath):
    try:
        """
        prova = driver.find_elements_by_partial_link_text("Next")
        for pv in prova:
            if pv:
                pv.click()"""
    except:
        print("here")
    netloc = urlPath.netloc
    scheme =urlPath.scheme
    path = urlPath.path
    par = urlPath.params
    link =scheme+"://"+netloc+path
    print(link)
    linkLen= len(link)
    elems = driver.find_elements_by_xpath(('//a[contains(@href, "%s")]' % path) or ('//a[contains(text(), "%s")]' % "Next") or ('//a[contains(text(), "%s")]' %"Show more"))
    print("lens" + str(len(elems)))
    for elem in elems:
        href = elem.get_attribute("href")
        print(href)
        if href[:linkLen] == link:
            try:
                y = elem.click()
                return 
            except:
                print(y)
                break
    return driver.page_source





"""
def HTMLparser(page,url):
    print("Beginning html parsing")
    htmlPath = set()
    alts = set()
    folder=parseUrl(url)
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(), folder))
    soup = BeautifulSoup(page, 'html.parser')
    i=0
    if(url.endswith("/")):
        url=url[:-1]
        print("urlll",url)
    
    tags = soup.findAll(['video','img','a','iframe'],recursive=True)
    for tag in tags:
        link='None'
        alt=''
        dataSrc =tag.get('data-src')
        print(tag.has_attr('src'),tag.get('src'),'src' in tag)
        if tag.has_attr('href'):
            print("href ",tag['href'])
        elif dataSrc!=None:
            print(dataSrc)
            alt = tag.get('alt','')
            print(alt)
        elif tag.has_attr('src'):
            print("src ",tag['src'])
            alt = tag.get('alt','')
            print(alt)
        elif tag.get('src')!=None:
            print('ok')
            print(tag.get('src'))
        elif 'src' in tag:
            print(tag['src'])
            print(tag.get('alt',''))
        elif tag.get('href')!=None:
            print('ok2')
            print(tag.get('href'))
        else:
            print('new tag')
        
    images = soup.find_all('img',alt=True,recursive=True)
    for image in images:
        link=None
        alt=''
        dataSrc =image.get('data-src')
        if dataSrc!=None:
            link= dataSrc
            alt = image.get('alt','')
        elif 'src' in image:
            link = image['src']
            alt = image.get('alt','')
        else:
            print('new tag')
        #formatting url
        link = checkURLformat(url,link)
        print('link:',link)
        print('alt',alt)
        htmlPath.add(link)
        alts.add(alt)

    #funzioni
    aTags = soup.findAll(href=True)
    print(aTags)
    for aTag in aTags:
        href = aTag['href']
        print("href: "+ str(href))
        href = checkURLformat(url,href)
        htmlPath.add(href)
    
    videoTags = soup.findAll('video')
    print(videoTags)
    for videoTag in videoTags:
        vdSrc=videoTag.get('src')
        if vdSrc:
            videoAlt= videoTag.get('alt','')
        elif vdSrc==None:
            continue
        else:
            print('new video tag')
        #per i video?
        vdSrc = checkURLformat(url,vdSrc)
        print("videooooo: ",vdSrc)
        htmlPath.add(vdSrc)
        alts.add(videoAlt)

    return htmlPath,alts
    """

    
import os
import time
import selenium
from urllib.parse import urlparse
from selenium.common.exceptions import WebDriverException
import csv
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
#metodo che in base all'usage impostato torna indietro fintanto che è possibile(verosimilmente prima pagina) e successivamente scorre pagina per pagina
#da testare
def pagination(driver,url,usage):
    parsedURL = urlparse(url)
    netloc = parsedURL.netloc
    scheme =parsedURL.scheme
    path = parsedURL.path
    par = parsedURL.params
    link =scheme+"://"+netloc+path
    print(link)
    linkLen= len(link)
    elems = driver.find_elements_by_xpath(('//a[contains(@href, "%s")]' % path) or ('//a[contains(text(), "%s")]' % "Next") or ('//a[contains(text(), "%s")]' %"Show more"))
    print("lens" + str(len(elems)))
    if(len(elems)==0):
        return "NoElements"
    for elem in elems:
        href = elem.get_attribute("href")
        text = elem.text
        text =str(text).lower()
        print("text "+ text)
        #bisognerebbe tradurre in base alla lingua della pagina aperta attraverso altri tipi di analisi
        if usage=="goBack":
            if href[:linkLen] == link and "prev" in text:
                try:
                    elem.click()
                    print("click")
                    return True
                except WebDriverException:
                    print( "Elemento non cliccabile")
                    pass
        elif usage=="goNext":
            if href[:linkLen] == link and "next" in text:
                try:
                    elem.click()
                    return True
                except WebDriverException:
                    print( "Elemento non cliccabile")
                    pass
            #testare
            elif "more" in text or "altro" in text:
                try:
                    elem.click()
                    return True
                except WebDriverException:
                    print( "Elemento non cliccabile")
                    pass
    return False

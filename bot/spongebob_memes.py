import requests
from lxml import html,etree
import time
#floors=[1,241,242,243]
floors=[1,241]
def find_all_meme_name():
    for floor in floors:
        url='https://forum.gamer.com.tw/C.php?bsn=60076&snA=5491441'
        response=requests.get(url+f"&to={floor}")
        tree=etree.HTML(response.text)

        titles=tree.xpath('//font[contains(translate(@color, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"#ff0000")]')
        for title in titles:
            print(etree.tostring(title,method='text',encoding='utf-8').decode('utf-8'))
            # print(etree.tostring(title,encoding='utf-8').decode('utf-8'))
class SearchQueryNotValidError(Exception):
    pass
def find_meme(text):
    if text.find('"')!=-1 or text.find("'")!=-1:
        raise SearchQueryNotValidError(f"text {repr(text)} has quote inside.")
    for floor in floors:
        now = time.time()
        url='https://forum.gamer.com.tw/C.php?bsn=60076&snA=5491441'
        response=requests.get(url+f"&to={floor}")
        tree=etree.HTML(response.text)
        #xpath=f'//div[//font[contains(translate(@color, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"#ff0000")] and normalize-space(.)="{text}"][1]/ancestor-or-self::div/following-sibling::div//a[contains(@class,"photoswipe-image")][1]'
        xpath = f'//div[//font[contains(translate(@color, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"#ff0000")] and normalize-space(.)="{text}"][1]/ancestor-or-self::div[1]'
        print(xpath)

        for ancestor_div in tree.xpath(xpath):#from descendant to ancestor
            xpath="/following-sibling::div"
            for sibling_div in ancestor_div.xpath(xpath):
                xpath='//a[contains(@class,"photoswipe-image")][1]'
                title=sibling_div.xpath(xpath) #type(title) == list
                #print(repr(etree.tostring(title[0],method='text',encoding='utf-8').decode('utf-8')))
                if title:#'title' is [] if the meme is not found
                    #the correct tag is the first one in list([0]), hence getting the first element
                    print(repr(etree.tostring(title[0], method='text', encoding='utf-8').decode('utf-8')))#print the content of the tag
                    print('meme url:', meme_url:=title[0].get('href'))
                    print('spent time:', time.time() - now, 's')
                    return meme_url
        print('spent time:', time.time() - now, 's')
    return None

    """
    old version:
    for floor in floors:
        url='https://forum.gamer.com.tw/C.php?bsn=60076&snA=5491441'
        response=requests.get(url+f"&to={floor}")
        tree=etree.HTML(response.text)
        xpath=f'//div[//font[contains(translate(@color, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"#ff0000")] and normalize-space(.)="{text}"][1]/ancestor-or-self::div/following-sibling::div//a[contains(@class,"photoswipe-image")][1]'
        print(xpath)
        title = tree.xpath(xpath) #type(title) == list
        #print(repr(etree.tostring(title[0],method='text',encoding='utf-8').decode('utf-8')))
        if title:#'title' is [] if the meme is not found
            #the correct tag is the first one in list([0]), hence getting the first element
            print(repr(etree.tostring(title[0], method='text', encoding='utf-8').decode('utf-8')))#print the content of the tag
            print('meme url:', meme_url:=title[0].get('href'))
            return meme_url
    return None
    """

#find_meme('我警告你sdv')
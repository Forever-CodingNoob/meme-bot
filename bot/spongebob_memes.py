import requests
from lxml import html,etree
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

def find_meme(text):
    for floor in floors:
        url='https://forum.gamer.com.tw/C.php?bsn=60076&snA=5491441'
        response=requests.get(url+f"&to={floor}")
        tree=etree.HTML(response.text)
        xpath=f'//div[font[contains(translate(@color, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"#ff0000")] and normalize-space()="{text}"][1]/following-sibling::div//a[contains(@class,"photoswipe-image")][1]'
        print(xpath)
        title = tree.xpath(xpath)
        #print(repr(etree.tostring(title[0],method='text',encoding='utf-8').decode('utf-8')))
        if title:
            print('meme url:', meme_url:=title[0].get('href'))
            return meme_url
    return None

#find_meme('你叫誰尖頭啊')
import requests
from lxml import html,etree
import time
from threading import Thread
from multiprocessing.pool import ThreadPool
from queue import Queue
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED,as_completed
import eventlet
import bot.test as test
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
def get_all_memes_with_url():
    pass
class SearchQueryNotValidError(Exception):
    pass
def find_meme(text):
    MAX_ANCESTOR_SEARCH=3
    MAX_SIBLING_SEARCH=15
    if text.find('"')!=-1 or text.find("'")!=-1:
        raise SearchQueryNotValidError(f"text {repr(text)} has quote inside.")
    for floor in floors:
        now = time.time()
        url='https://forum.gamer.com.tw/C.php?bsn=60076&snA=5491441'
        response=requests.get(url+f"&to={floor}")
        tree=etree.HTML(response.text)
        #xpath=f'//div[//font[contains(translate(@color, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"#ff0000")] and normalize-space(.)="{text}"][1]/ancestor-or-self::div/following-sibling::div//a[contains(@class,"photoswipe-image")][1]'
        xpath = f'//div[@id="BH-background"]/div[@id="BH-wrapper"]/div[@id="BH-master"]/section[contains(@class,"c-section")]/div[contains(@class,"c-section__main")]/div[contains(@class,"c-post__body")]/article/div[contains(@class,"c-article__content")]//div[//font[contains(translate(@color, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"#ff0000")] and normalize-space(.)="{text}"][1]/ancestor-or-self::div'
        print(xpath)

        ancestor_count=0

        print('hola')
        #ancestors=tree.xpath(xpath)#from ancestor to descendant

        '''
        pool=ThreadPool(processes=1)
        result=pool.apply_async(test.test,args=(None,))
        ancestors=result.get()
        print('result',ancestors)
        '''

        '''
        ancestors=[]
        with ThreadPoolExecutor() as executor:
            future=executor.submit(tree.xpath,xpath)
            for future in as_completed([future]):
                ancestors=future.result()
                break
        '''

        def FindElementByXpath(q):
            results=tree.xpath(xpath)
            q.put(results)

        q=Queue()
        thread=Thread(target=FindElementByXpath,args=(q,))
        thread.start()
        thread.join()
        ancestors=q.get()

        ancestors.reverse()
        print('hola again')
        print('ancestors:',ancestors)
        for ancestor_div in ancestors:#from descendant to ancestor
            if ancestor_count<MAX_ANCESTOR_SEARCH:
                ancestor_count+=1
            else:
                break

            xpath="following-sibling::div"

            sibling_count=0
            siblings=ancestor_div.xpath(xpath)
            print('siblings:',siblings)
            for sibling_div in siblings:
                if sibling_count <MAX_SIBLING_SEARCH:
                    sibling_count += 1
                else:
                    break

                xpath='descendant::a[contains(@class,"photoswipe-image")][1]'
                title=sibling_div.xpath(xpath) #type(title) == list
                #prettry print:print(repr(etree.tostring(title[0],method='text',encoding='utf-8').decode('utf-8')))
                if title:#'title' is [] if the meme is not found
                    #the correct tag is the first one in list([0]), hence getting the first element
                    print(repr(etree.tostring(title[0], method='text', encoding='utf-8').decode('utf-8')))#print the content of the tag
                    print('meme url:', meme_url:=title[0].get('href'))
                    print(f'time spent on floor {floor}:', time.time() - now, 's')
                    return meme_url
        print(f'time spent on floor {floor}:', time.time() - now, 's')
        eventlet.sleep(0) #temporarily halt the thread and  yield the CPU to allow other waiting tasks to run.
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

#find_meme('明天再來')
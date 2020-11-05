from .spongebob_memes import find_meme,SearchQueryNotValidError
from threading import Thread,enumerate
from abc import ABC,abstractmethod
import time
import eventlet
from flask_socketio import emit
class Meme(ABC):
    def __init__(self,meme_text):
        self.meme_text=meme_text
        self.start_time=None
        self.process_time=None

    def send_meme(self,notify_regularly=False):
        self.start_time=time.time()
        self.thread=Thread(target=self.__get_meme__)
        self.thread.start()
        if notify_regularly:
            notify_thread=Thread(target=self.__notify_regularly)
            notify_thread.start()
        print('start to find meme...')
        return
    def __get_meme__(self):
        try:
            meme_url = find_meme(self.meme_text)
        except SearchQueryNotValidError as e:
            print(e.__class__, ":", e)
            meme_url = None
        self.meme_url=meme_url
        self.process_time = time.time() - self.start_time
        if meme_url:
            print(f'found meme at {meme_url}')
            self._success()
        else:
            print('meme not found!')
            self._fail()
        self._react_after()
    def __notify_regularly(self,interval=10):
        eventlet.sleep(interval)
        while self.thread.is_alive():
            self._notify()
            eventlet.sleep(interval)

    @abstractmethod
    def _react_after(self):
        pass
    @abstractmethod
    def _success(self):
        pass
    @abstractmethod
    def _fail(self):
        pass
    @abstractmethod
    def _notify(self):
        pass

class MemeBot(Meme):
    def __init__(self,meme_text,*args,bot,sender_id,**kwargs):
        super(MemeBot, self).__init__(meme_text,*args,**kwargs)
        self.bot=bot
        self.sender_id=sender_id
    def _react_after(self):
        pass
    def _success(self):
        self.bot.send_image_url(self.sender_id, self.meme_url)
    def _fail(self):
        pass
    def _notify(self):
        pass
class MemeSOCKET(Meme):
    def __init__(self,meme_text,*args,socket,session_id,**kwargs):
        super(MemeSOCKET, self).__init__(meme_text,*args,**kwargs)
        self.session_id=session_id
        self.socket=socket
    def _react_after(self):
        self.socket.emit('system_msg',{'data':'execution time: %.3f s'%self.process_time},room=self.session_id)
    def _success(self):
        self.socket.emit('meme_result',{'data':self.meme_url},room=self.session_id)
    def _fail(self):
        self.socket.emit('system_msg',{'data':'meme not found!'},room=self.session_id)
    def _notify(self):
        self.socket.emit('system_msg',{'data':'loading.............'},room=self.session_id)
#old test: print(Meme(2323,'派欸').send_meme())

def print_all_threads():
    log='executing threads:\n<ul>\n'
    for thread in enumerate():
        log+="\t<li>"+thread.getName()+"</li>\n"
    log+='</ul>\n'
    return log

'''test functions'''
def _test_send(socket,id):
    import time
    time.sleep(30)
    socket.emit('system_msg',{'data':'hihihi!'},room=id)


def _hola():
    while True:
        time.sleep(1)
        print('hi')
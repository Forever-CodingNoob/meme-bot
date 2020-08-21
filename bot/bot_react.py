from .spongebob_memes import find_meme,SearchQueryNotValidError
from threading import Thread,enumerate
from abc import ABC,abstractmethod
import time
from flask_socketio import emit
class Meme(ABC):
    def __init__(self,meme_text):
        self.meme_text=meme_text
        self.start_time=None
        self.process_time=None

    def send_meme(self):
        self.start_time=time.time()
        thread=Thread(target=self.__get_meme__)
        thread.start()
        print('start to find meme...')
        return "started"
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
            self.__success__()
        else:
            print('meme not found!')
            self.__fail__()
        self.__react_after__()
    @abstractmethod
    def __react_after__(self):
        pass
    @abstractmethod
    def __success__(self):
        pass
    @abstractmethod
    def __fail__(self):
        pass

class MemeBot(Meme):
    def __init__(self,meme_text,*args,bot,sender_id,**kwargs):
        super(MemeBot, self).__init__(meme_text,*args,**kwargs)
        self.bot=bot
        self.sender_id=sender_id
    def __react_after__(self):
        pass
    def __success__(self):
        self.bot.send_image_url(self.sender_id, self.meme_url)
    def __fail__(self):
        pass
class MemeSOCKET(Meme):
    def __init__(self,meme_text,*args,socket,session_id,**kwargs):
        super(MemeSOCKET, self).__init__(meme_text,*args,**kwargs)
        self.session_id=session_id
        self.socket=socket
    def __react_after__(self):
        self.socket.emit('system_msg',{'data':'execution time: %.3f s'%self.process_time},room=self.session_id)
    def __success__(self):
        self.socket.emit('meme_result',{'data':self.meme_url},room=self.session_id)
    def __fail__(self):
        self.socket.emit('system_msg',{'data':'meme not found!'},room=self.session_id)

#old test: print(Meme(2323,'派欸').send_meme())

def print_all_threads():
    log='executing threads:'
    for thread in enumerate():
        log+="\n\t"+repr(thread)
    return log
def test_send(socket,id):
    import time
    time.sleep(30)
    socket.emit('system_msg',{'data':'hihihi!'},room=id)
import subprocess, threading # , queue, os
from time import sleep
from PyQt5.Qt import QObject

class pinger(QObject):
    
    def __init__(self, address, messages, timeout = 1):
        super(pinger, self).__init__()
        self.__address = address
        self.__messages = messages
        self.state = False
        self.enabled = True
        self.__timeout = timeout
        self.__dnsResolved = 'unresolved'
        
        
        
    def __ping(self):
        """
        Returns True if host responds to a ping request
        """
        import platform
        ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
        ping_string = "ping " + ping_str + " " + self.__address
        if platform.system().lower() != "windows":
            result = subprocess.call(ping_string, stdout = subprocess.DEVNULL, shell = True) == 0
        else:
            result = False
            p = subprocess.Popen(ping_string, shell = True, stdout = subprocess.PIPE)
            lines = []
            for i in p.stdout:
                lines.append(str(i, 'cp866'))
            for i in lines:
                if i[:(17 + len(self.__address) + 2)] == 'Обмен пакетами с ' + self.__address + ' [': 
                    self.__dnsResolved = ''
                    a = True
                    k = 19 + len(self.__address)
                    while a:
                        if i[k] != ']': 
                            self.__dnsResolved += i[k]
                            k += 1
                        else: a = False
                if i[:(9 + len(self.__address))] == 'Ответ от ' + self.__address or i[:(9 + len(self.__dnsResolved))] == 'Ответ от ' + self.__dnsResolved:
                    result = True
        return result    
        
    
    
    def __mainloop(self):
        while self.enabled:
            state = self.__ping()
            if self.state != state:
                self.stateChanged(state)
            sleep(self.__timeout)
    
    def stateChanged(self, state):
        self.__messages.put([self.__address, state])
        self.state = state
        
    def start(self, delay = 0):
        sleep(delay)
        self.t = threading.Thread(target = self.__mainloop, args = ())
        self.t.daemon = True
        self.t.start()
        
    def stop(self):
        if self.state: self.__messages.put([self.__address, False])
        self.enabled = False

    
    





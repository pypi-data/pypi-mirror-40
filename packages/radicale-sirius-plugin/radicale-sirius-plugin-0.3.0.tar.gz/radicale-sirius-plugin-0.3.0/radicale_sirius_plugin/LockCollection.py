from threading import Lock,RLock

class LockCollection():
    '''
    Object which provides Lock by name
    for same name return same lock
    '''

    def __init__(self):
        '''
        Init object
        '''

        self.main_lock = Lock()
        self.dict = {}

    def get_lock(self,name):
        '''Get Unique lock by name
        
        :param name: lock's name
        :type name: any
        :return: Lock
        '''

        with self.main_lock:
            if name not in self.dict:
                self.dict[name] = RLock()
            return self.dict[name]
    
    def remove_lock(self,name):
        '''Remove lock from collection
        
        :param name: lock's name
        :type name: any
        '''

        with self.main_lock:
            return self.dict.pop(name,None)
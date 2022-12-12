from abc import ABCMeta, abstractmethod

class IAnimation(metaclass=ABCMeta):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass

    def teardown(self):
        pass


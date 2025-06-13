from abc import ABC, abstractmethod

class InterfaceGtG(ABC):

    @abstractmethod
    def show_me(self, gt_hinban:str)->None:
        pass

    @abstractmethod
    def calc_multiple(self)->float:
        pass

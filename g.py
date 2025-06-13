"""
interfaceを読み込む
"""
from interface_gt_g import InterfaceGtG

class G(InterfaceGtG):

    def __init__(self, hinban: str, qty: float, tani: str, oya_hinban: str)-> None:
        self.__hinban = hinban
        self.__qty = qty
        self.__tani = tani
        self.__oya_hinban = oya_hinban

    def show_me(self, gt_hinban)-> None:
        print(f'{gt_hinban} => {self.__oya_hinban} : {self.__hinban} : {self.__qty}')

    def calc_multiple(self)->float:
        return 0.0

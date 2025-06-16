"""
親品番が存在しない子品番のクラス
"""
from interface_material import InterfaceMaterial

class MaterialNotExistsInParent(InterfaceMaterial):
    """
    親品番が存在しない子品番のInterfaceMaterial型の
    MaterialNotExistsInParentのクラス
    """

    def __init__(self, hinban: str, qty: float,
                 parent_hinban: str, sekiyurui:str, sg:float)-> None:
        self.__hinban = hinban
        self.__qty = qty
        self.__parent_hinban = parent_hinban
        self.__sekiyurui = sekiyurui
        self.__sg = sg

        self.__multiple:float = 0
        if self.__sekiyurui == 'ｱﾙｺｰﾙ類':
            self.__multiple = (self.__qty / self.__sg) / 400
            return
        if self.__sekiyurui == '4石':
            self.__multiple = (self.__qty / self.__sg) / 6000
            return
        if self.__sekiyurui == '3石':
            self.__multiple = (self.__qty / self.__sg) / 2000
            return
        if self.__sekiyurui =='2石（水）' or self.__sekiyurui =='2石(水)':
            self.__multiple = (self.__qty / self.__sg) / 2000
            return
        if self.__sekiyurui == '2石':
            self.__multiple = (self.__qty / self.__sg) / 1000
            return
        if self.__sekiyurui == '1石':
            self.__multiple = (self.__qty / self.__sg) / 200
            return


    def show_me(self, zaiko_hinban)-> None:
        """
        確認用メソッド。本番では使用しない。
        """
        print(f'{zaiko_hinban} => {self.__parent_hinban} : {self.__hinban} : {self.__qty}')

    def calc_multiple(self, zaiko_hinban:str, 
                      dic_zaiko_hinban_multiple:dict[str, float])->None:
        if zaiko_hinban not in dic_zaiko_hinban_multiple:
            dic_zaiko_hinban_multiple[zaiko_hinban] = self.__multiple 
        else:
            dic_zaiko_hinban_multiple[zaiko_hinban] += self.__multiple 


        #print(f'{zaiko_hinban} => {self.__parent_hinban} : {self.__hinban} : {self.__multiple}')


import pandas as pd
from interface_material import InterfaceMaterial
from material_exists_in_parent import MaterialExistsInParent

class Material(InterfaceMaterial):

    def __init__(self, zaiko_hinban:str, qty: float, tani: str,
                 df_ps:pd.DataFrame, dic_parent_num:dict[str, int], 
                 dic_hinban_tani:dict[str, str], 
                 dic_gs_hinban:dict[str, str],
                 dic_sekiyurui:dict[str, list[str]])-> None:

        self.zaiko_hinban = zaiko_hinban
        self.__material:InterfaceMaterial = (
        MaterialExistsInParent(
                  zaiko_hinban,
                  qty,
                  tani,
                  df_ps,
                  dic_parent_num,
                  dic_hinban_tani,
                  dic_gs_hinban,
                  dic_sekiyurui))


    def show_me(self, zaiko_hinban) -> None:
        if zaiko_hinban == self.zaiko_hinban:
            self.__material.show_me(zaiko_hinban)


    def calc_multiple(self, zaiko_hinban:str, 
                      dic_zaiko_hinban_multiple:dict[str,float]) -> None:
        if zaiko_hinban == self.zaiko_hinban:
            self.__material.calc_multiple(zaiko_hinban, dic_zaiko_hinban_multiple)
       # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

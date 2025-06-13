import pandas as pd

from gt import Gt

class Factory:
    """
    インスタンスを生成する
    """

    def __init__(self, df_zaiko: pd.DataFrame)-> None:
        self.__df_zaiko = df_zaiko


    def create_gt_instance(self, df_ps:pd.DataFrame, dic_oya_num:dict[str, int], 
                           dic_hinban_tani:dict[str, str])->list[Gt]:
        #zaiko_gt = self.__df_zaiko.loc[self.__df_zaiko['ZaiHinCD'].str.startswith('GT-'), :]
        zaiko_gt = self.__df_zaiko
        gt_s:list[Gt] = []
        for i in range(len(zaiko_gt)): # Seriesにしてから取り出す
            hinban:str    = zaiko_gt.iloc[i,:]['ZaiHinCD']
            qty:float  = zaiko_gt.iloc[i,:]['qty']
            tani:str = dic_hinban_tani[hinban]
            gt:Gt = Gt(hinban, qty, tani, df_ps, dic_oya_num, dic_hinban_tani)
            gt_s.append(gt)
        return gt_s

        



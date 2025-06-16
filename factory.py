"""
InterfaceMaterial型のMaterialExistsInParentのインスタンスを生成します   
"""
from typing import Optional
import pandas as pd
from material import Material

from material_exists_in_parent import MaterialExistsInParent
from interface_material import InterfaceMaterial

class Factory:
    """
    InterfaceMaterial型のMaterialExistsInParentのインスタンスを生成します   
    """

    def __init__(self, df_zaiko: pd.DataFrame)-> None:
        self.__df_zaiko = df_zaiko


    def create_material_instance(
            self, zaiko_hinban:str, qty:float, df_ps:pd.DataFrame, 
            dic_parent_num:"dict[str, int]",
            dic_hinban_tani:"dict[str, str]",
            dic_gs_hinban:"dict[str, str]",
            dic_sekiyurui:"dict[str, list[str]]")->Optional[InterfaceMaterial]:
        """
        親品番が存在する原料(GT, GTS, GS, 製品も)のインスタンスを生成する
        args:
            df_ps (pd.DataFrame) : psマスタ
            dic_parent_num (dict[str, int]) : {親品番:df_zaikoのindexnumber}
            dic_hinban_tani (dict[str, str]) : {品番:単位}
        return:
            material (InterfaceMaterial) : インスタンス
        """

        material:Optional[InterfaceMaterial] = None
        tani:str = dic_hinban_tani[zaiko_hinban]
        material = Material(
                   zaiko_hinban, qty, tani, df_ps, dic_parent_num, 
                   dic_hinban_tani, dic_gs_hinban, dic_sekiyurui)
        return material


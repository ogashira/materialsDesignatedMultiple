"""
dictionaryなどのオブジェクトを作るクラス
"""
import pandas as pd
from factory import *


class CreateObject:
    """
    dictionaryなどのオブジェクトを作るクラス
    """

    def create_dic_gs_hinban(self, df:pd.DataFrame)-> dict:
        """
        品番マスタデータフレームから{GS-*: S6-*,....}の辞書を作る
        データフレームの品目コード01, 02を1, 2に変換してS1- S2-を作りたい
        しかし、品目コードの中にC4など、数値変換できない文字があるのでis_int
        で判定してデータを取り除く
        gs_to_hinbanでは'GS-SV3800-U'を'S6-SV3800-U'に変換する

        args:
            df (pd.DataFrame) : 品番マスタのデータフレーム
        return:
            dic_gs_hinban(dict) : {GS品番:品番}の辞書
        """
        pd.options.mode.copy_on_write = True

        def is_int(s:str) -> bool:
            try:
                int(s)
            except ValueError:
                return False
            else:
                return True

        def gs_to_hinban(line:pd.Series)-> str:
            gs:str = str(line['HinFree10'])
            no:int = int(line['HinMokCD1'])
            head_char:str = 'S' + str(no) + '-'
            return gs.replace('GS-', head_char)

        #gs:pd.DataFrame = df[df['HinFree10'].str.startswith('GS-')]
        gs:pd.DataFrame = df.loc[df['HinFree10'].str.startswith('GS-'),:]
        gs['is_int'] = gs['HinMokCD1'].map(is_int)
        gs_num_code:pd.DataFrame = gs.loc[gs['is_int'],:]
        gs_num_code['gs_to_hinban'] = gs_num_code.apply(gs_to_hinban, axis = 1)

        dic:dict[str, str] =  dict(zip(gs_num_code['HinFree10'], 
                                                     gs_num_code['gs_to_hinban']))

        return dic
    
    def create_dic_gs_hinban2(self, df:pd.DataFrame)-> dict:

        dic:dict[str, str] = {}
        for i in range(len(df)):
            if df.iloc[i,:]['HinFree10'] == '' or df.iloc[i,:]['HinFree10'] == ' ':
                continue
            dic[df.iloc[i,:]['HinFree10']] = df.iloc[i, :]['HinHinCD']

        return dic

    def create_dic_parent_num(self, df:pd.DataFrame)-> dict:
        """
        psマスタデータフレームから{親品番:number}の辞書を作る。
        args:
            df (pd.DataFrame) : psマスタのデータフレーム
        return:
            dic_parent_num (dict) : {親品番:number}の辞書
        """

        dic:dict[str, int] = {}
        for i  in range(len(df)):
            dic[df.iloc[i,:]['PsmHinCDO']] = i

        return dic


    def create_dic_hinban_tani(self, df:pd.DataFrame)-> dict:
        """
        品番マスタデータフレームから{品番:単位}の辞書を作る。
        args:
            df (pd.DataFrame) : 品番マスタのデータフレーム
        return:
            dic_hinban_tani (dict) : {品番:単位}の辞書
        """

        dic:dict[str, int] = {}
        for i  in range(len(df)):
            dic[df.iloc[i,:]['HinHinCD']] = df.iloc[i,:]['HinTniCD']

        return dic


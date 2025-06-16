"""
プログラムの流れ。Mainから呼ばれる
"""
import csv
import platform
from typing import Optional
import pandas as pd
from factory import Factory
from sql_query import SqlBZAIKO, SqlMHINCD, SqlMPSMST
from create_object import CreateObject
from interface_material import InterfaceMaterial
from material import Material


class ProgramFlow:

    def start(self, is_a:bool)-> None:

        sql:SqlBZAIKO = SqlBZAIKO()
        df_zaiko:pd.DataFrame = sql.fetch_sqldata()
        sql_ps:SqlMPSMST = SqlMPSMST()
        df_ps:pd.DataFrame = sql_ps.fetch_sqldata()
        sql_hinban:SqlMHINCD = SqlMHINCD()
        df_hinban:pd.DataFrame = sql_hinban.fetch_sqldata()

        create_object:CreateObject = CreateObject()
        dic_gs_hinban:"dict[str,str]" = create_object.create_dic_gs_hinban2(df_hinban)
        dic_parent_num:"dict[str,int]" = create_object.create_dic_parent_num(df_ps)
        dic_hinban_tani:"dict[str,str]" = create_object.create_dic_hinban_tani(df_hinban)


        os_name:str = platform.system()
        path:str = r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/sekiyurui_sg.csv'
        if os_name == 'Linux':
            path = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/sekiyurui_sg.csv'
        elif os_name == 'Darwin':
            path = r'/Volumes/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/sekiyurui_sg.csv'

        with open(path, encoding='cp932') as f:
            reader = csv.reader(f)
            l = [row for row in reader]

        # dic_sekiyurui = { 'G-TOL' : [ '1石', '0.860'], .....}
        # G- のみの辞書
        dic_sekiyurui:"dict[str,list[str]]" = {}
        for line in l:
            if not line[0].startswith('G-'):
                continue
            tmp:"list[str]" = []
            tmp.append(line[4])
            tmp.append(line[5])
            dic_sekiyurui[line[0]] = tmp



        materials:"list[InterfaceMaterial]" = []
        factory:Factory = Factory(df_zaiko)
        for i in range(len(df_zaiko)):
            zaiko_hinban:str = df_zaiko.iloc[i,:]['ZaiHinCD']
            qty:float = df_zaiko.iloc[i,:]['qty']
            material:Optional[InterfaceMaterial] = (
                    factory.create_material_instance(
                        zaiko_hinban, qty, df_ps, dic_parent_num,
                        dic_hinban_tani, dic_gs_hinban, dic_sekiyurui)
                    )
            materials.append(material)

        dic_zaiko_hinban_multiple:"dict[str, list[float]]" = {}
        for i in range(len(df_zaiko)):
            zaiko_hinban = df_zaiko.iloc[i,:]['ZaiHinCD']
            #materials[i].show_me(zaiko_hinban)
            materials[i].calc_multiple(zaiko_hinban, dic_zaiko_hinban_multiple, is_a)

        total_qty:float = 0
        total_muultiple:float = 0
        for k, v in dic_zaiko_hinban_multiple.items():
            print(f'{k:<20} => 在庫量: {v[0]:8.2f} kg  指定数量倍数: {v[1]:8.5f}')
            total_qty += v[0]
            total_muultiple += v[1]
        print()
        print('***************************************************')
        print(f' Total : 在庫量: {total_qty:10.2f} kg  指定数量倍数: {total_muultiple:8.5f}')










import pandas as pd
from factory import *
from sql_query import SqlBZAIKO, SqlMHINCD, SqlMPSMST
from create_object import *

sql:SqlBZAIKO = SqlBZAIKO()
df_zaiko:pd.DataFrame = sql.fetch_sqldata()
sql_hinban:SqlMHINCD = SqlMHINCD()
df_hinban:pd.DataFrame = sql_hinban.fetch_sqldata()
sql_ps:SqlMPSMST = SqlMPSMST()
df_ps:pd.DataFrame = sql_ps.fetch_sqldata()
sql_hinban:SqlMHINCD = SqlMHINCD()
df_hinban:pd.DataFrame = sql_hinban.fetch_sqldata()

create_object:CreateObject = CreateObject()
dic_gs_hinban:dict = create_object.create_dic_gs_hinban(df_hinban)
dic_oya_num:dict = create_object.create_dic_oya_num(df_ps)
dic_hinban_tani:dict = create_object.create_dic_hinban_tani(df_hinban)


factory:Factory = Factory(df_zaiko)
gt_s:list = factory.create_gt_instance(df_ps, dic_oya_num, dic_hinban_tani)

#zaiko_gt = df_zaiko.loc[df_zaiko['ZaiHinCD'].str.startswith('GT-'),:]
zaiko_gt = df_zaiko
print(len(gt_s))
for i in range(len(zaiko_gt)):
    gt_hinban = zaiko_gt.iloc[i,:]['ZaiHinCD']
    gt_s[i].show_me(gt_hinban)




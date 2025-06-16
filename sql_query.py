"""
SqlServerからfetchするデータのSqｌ文
"""
import warnings
import pandas as pd
from dateutil.relativedelta import relativedelta
from sql_server import SqlServer


class SqlBZAIKO:
    """
    在庫データ取得
    """

    def __init__(self)->None:
        pass

    def fetch_sqldata(self)->pd.DataFrame:
        warnings.filterwarnings("ignore", category=UserWarning)
        sql_server:SqlServer = SqlServer()
        cnxn = sql_server.get_cnxn()

        sql_query:str = ("SELECT ZaiHinCD, SUM(ZaiZaiSuG) AS qty" 
                         " FROM dbo.BZAIKO"
                         " WHERE ZaiBuCD = 'S0024'"
                         " AND ZaiZaiSuG > 0"
                         " GROUP BY ZaiHinCD"
                         " ORDER BY ZaiHinCD"
                        )
        zaiko_data:pd.DataFrame = pd.read_sql(sql_query, cnxn)

        return zaiko_data


class SqlMPSMST:
    """
    ＰＳマスタ取得
    """
   
    def __init__(self)->None:
        pass

    def fetch_sqldata(self)->pd.DataFrame:
        warnings.filterwarnings("ignore", category=UserWarning)
        sql_server:SqlServer = SqlServer()
        cnxn = sql_server.get_cnxn()

        sql_query:str = ("SELECT PsmHinCDO, PsmHinCDK, PsmInsS" 
                         " FROM dbo.MPSMST"
                         " ORDER BY PsmHinCDO"
                        )
        ps_master:pd.DataFrame = pd.read_sql(sql_query, cnxn)

        return ps_master


class SqlMHINCD:
    """
    品番マスタ取得
    """
   
    def __init__(self)->None:
        pass

    def fetch_sqldata(self)->pd.DataFrame:
        warnings.filterwarnings("ignore", category=UserWarning)
        sql_server:SqlServer = SqlServer()
        cnxn = sql_server.get_cnxn()

        sql_query:str = ("SELECT HinHinCD, HinSeiKBN, HinMokCD1, HinTniCD," 
                         " HinFree10"
                         " FROM dbo.MHINCD"
                         " ORDER BY HinHinCD"
                        )
        ps_master:pd.DataFrame = pd.read_sql(sql_query, cnxn)

        return ps_master

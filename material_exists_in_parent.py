"""
親品番に存在している子品番のクラスです
"""
import pandas as pd
from material_not_exists_in_parent import MaterialNotExistsInParent
from interface_material import InterfaceMaterial

class MaterialExistsInParent(InterfaceMaterial):
    """
    親品番に存在している子品番のクラスです
    __init__で子品番の原料が親品番に存在していなかったら、
    materialNotExistsInParentクラスのインスタンスをつくる。
    存在していたら、MaterialExistsInParent（自分）のインスタンス
    を再帰的い作る。
    """
    def __init__(self, hinban:str, qty: float, tani: str,
                 df_ps:pd.DataFrame, dic_parent_num:dict[str, int],
                 dic_hinban_tani:dict[str, str],
                 dic_gs_hinban:dict[str, str],
                 dic_sekiyurui:dict[str, list[str]])-> None:
        """
        渡ってきた品番がG-などで親品番に存在しなければ、initの中で
        MaterialNotExistsInParentクラスのインスタンスを作って終了
        """
        self.__hinban = hinban
        if hinban.startswith('GS-'):
            if hinban in dic_gs_hinban:
                self.__hinban = dic_gs_hinban[hinban]
        self.__qty = qty
        if tani == 'G':
            self.__qty = qty / 1000
        self.__df_ps = df_ps
        self.__dic_parent_num = dic_parent_num
        self.__dic_hinban_tani = dic_hinban_tani
        self.__dic_gs_hinban = dic_gs_hinban
        self.__dic_sekiyurui = dic_sekiyurui

        self.__materials:list[InterfaceMaterial] = []
        self.__df_parent:pd.DataFrame = (
            self.__df_ps.loc[self.__df_ps['PsmHinCDO']== self.__hinban,:])
        # G-など、親品番が存在しなかったら、Gのインスタンスを作って終了
        self.__sekiyurui:str = ''
        self.__sg:float = 0.0
        if not len(self.__df_parent):
            if self.__hinban in self.__dic_sekiyurui:
                self.__sekiyurui = self.__dic_sekiyurui[self.__hinban][0]
                try:
                    self.__sg = float(self.__dic_sekiyurui[self.__hinban][1])
                except:
                    self.__sg = 0.0
            self.__materials.append(
                    MaterialNotExistsInParent(self.__hinban,
                                              self.__qty,
                                              self.__hinban,
                                              self.__sekiyurui,
                                              self.__sg) 
                                   )
            return None


        self.__sum:float = 0 
        self.sum_qty()

        self.component_down() # 配合をmaterialsに詰める


    def to_kg(self, hinban:str, qty:float)->float:
        """
        単位がGの子品番の重量をkgに変換する
        """
        if self.__dic_hinban_tani[hinban] == 'G':
            return qty / 1000
        return qty

    def sum_qty(self)-> float:
        """
        Gt-品番(親品番)のトータル重量を求める
        """
        for i in range(len(self.__df_parent)):
            child:str = self.__df_parent.iloc[i,:]['PsmHinCDK']
            if self.__dic_hinban_tani[child] == 'CN':
                continue
            qty:float = self.__df_parent.iloc[i,:]['PsmInsS']
            qty_kg:float = self.to_kg(child, qty)
            self.__sum += qty_kg
        return self.__sum

    def is_exists_in_parents(self, child)-> bool:
        """
        親品番が存在するかを判定
        """
        if child in self.__dic_parent_num:
            return True
        return False

    def component_down(self):
        """
        親品番の配合を子品番に展開していく
        展開した子品番が親品番に存在しなかったら、
        material_not_exists_in_parentのインスタンスを生成して 
        self.__materialsリストにアペンドする。
        展開した子品番が親品番に存在したら、material_exists_in_parentの
        インスタンスを生成して、 self.__materialsリストにアペンドする。
        この時、material_exists_in_parentのコンストラクタが 再帰的に呼び出される。
        """
        for i in range(len(self.__df_parent)):
            child:str = self.__df_parent.iloc[i,:]['PsmHinCDK']
            if self.__dic_hinban_tani[child] == 'CN': #缶は無視する
                continue
            qty:float = self.__df_parent.iloc[i,:]['PsmInsS']
            qty_kg:float = (self.to_kg(child, qty) / self.__sum) * self.__qty
            if self.is_exists_in_parents(child):
                self.__materials.append(MaterialExistsInParent(
                               child, qty_kg, 'KG', self.__df_ps,
                               self.__dic_parent_num, self.__dic_hinban_tani,
                               self.__dic_gs_hinban,
                               self.__dic_sekiyurui)
                                       )
            else:
                if child in self.__dic_sekiyurui:
                    self.__sekiyurui = self.__dic_sekiyurui[child][0]
                    try:
                        self.__sg = float(self.__dic_sekiyurui[child][1])
                    except:
                        self.__sg = 0.0
                    
                self.__materials.append(MaterialNotExistsInParent(
                                   child, qty_kg, self.__hinban,
                                   self.__sekiyurui, self.__sg)
                                       )

    def show_me(self, zaiko_hinban)->None:
        """
        確認用メソッド。本番では呼び出さない。
        GT品番の中にGT品番があるケースだと、一番上の階層のGT品番が分からなく
        なってしまうので、GT品番を外からもらう事にした。
        例えば、GT-AL-P300-25の場合
        ['GT-V-120SOL', 'G-14LLB', 'G-TOL'] <- のようにリストに入り、
        GT-V-120SOL インスタンスには
        ['G-XOL', 'G-V-120'] を持っている。
        G-14LLB, G-TOLは親品番はGT-AL-P300-25を持っているが、
        G-XOL, G-V-120の親品番はGT-V-120SOLとなり、GT-AL-P300-25との関連が
        わからなくなるため
        """
        for material in self.__materials:
            material.show_me(zaiko_hinban)

    def calc_multiple(self, zaiko_hinban:str, 
                      dic_zaiko_hinban_multiple:dict[str,float])-> None:
        for material in self.__materials:
            material.calc_multiple(zaiko_hinban, dic_zaiko_hinban_multiple)


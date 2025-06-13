import pandas as pd
from g import G
from interface_gt_g import InterfaceGtG

class Gt(InterfaceGtG):
    def __init__(self, hinban:str, qty: float, tani: str,
                 df_ps:pd.DataFrame, dic_oya_num:dict[str, int],
                 dic_hinban_tani:dict[str, str])-> None:
        self.__hinban = hinban
        self.__qty = qty
        if tani == 'G':
            self.__qty = qty / 1000
        self.__tani = tani
        self.__df_ps = df_ps
        self.__dic_oya_num = dic_oya_num
        self.__dic_hinban_tani = dic_hinban_tani

        self.__gt_g_s:list[InterfaceGtG] = []
        self.__df_gt:pd.DataFrame = (
            self.__df_ps.loc[self.__df_ps['PsmHinCDO']== self.__hinban,:])
        # G-など、親品番が存在しなかったら、Gのインスタンスを作って終了
        if not len(self.__df_gt):
            self.__gt_g_s.append(
                    G(self.__hinban,
                      self.__qty,
                      self.__tani,
                      self.__hinban) 
                    )
            return


        self.__sum:float = 0 
        self.sum_qty()

        self.component_down() # 配合をgt_g_sに詰める


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
        for i in range(len(self.__df_gt)):
            ko:str = self.__df_gt.iloc[i,:]['PsmHinCDK']
            if self.__dic_hinban_tani[ko] == 'CN':
                continue
            qty:float = self.__df_gt.iloc[i,:]['PsmInsS']
            qty_kg:float = self.to_kg(ko, qty)
            self.__sum += qty_kg
        return self.__sum

    def is_exists_in_oyas(self, ko)-> bool:
        if ko in self.__dic_oya_num:
            return True
        return False

    def component_down(self):
        """
        親品番の配合を子品番に展開していく
        展開した子品番が親品番に存在しなかったら、Gのインスタンスを生成して
        self.__gt_g_sリストにアペンドする。
        展開した子品番が親品番に存在したら、Gtのインスタンスを生成して、
        self.__gt_g_sリストにアペンドする。この時、Gtのコンストラクタが
        再帰的に呼び出される。
        """
        for i in range(len(self.__df_gt)):
            ko:str = self.__df_gt.iloc[i,:]['PsmHinCDK']
            if self.__dic_hinban_tani[ko] == 'CN': #缶は無視する
                continue
            qty:float = self.__df_gt.iloc[i,:]['PsmInsS']
            qty_kg:float = (self.to_kg(ko, qty) / self.__sum) * self.__qty
            if self.is_exists_in_oyas(ko):
                self.__gt_g_s.append(Gt(ko, qty_kg, 'KG', self.__df_ps, 
                               self.__dic_oya_num, self.__dic_hinban_tani))
            else:
                self.__gt_g_s.append(G(ko, qty_kg, 'KG', self.__hinban))

    def show_me(self, gt_hinban)->None:
        """
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
        for gt_g in self.__gt_g_s:
           gt_g.show_me(gt_hinban)

    def calc_multiple(self)-> float:
        return 0.0

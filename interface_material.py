"""
インターフェース
MaterialExistsInParent, MaterialNotExistsInParentで
実装する
"""
from abc import ABC, abstractmethod

class InterfaceMaterial(ABC):
    """
    インターフェース
    MaterialExistsInParent, MaterialNotExistsInParentで
    実装する
    """

    @abstractmethod
    def show_me(self, zaiko_hinban:str)->None:
        """
        抽象メソッド
        """

    @abstractmethod
    def calc_multiple(self, zaiko_hinban:str, 
                      dic_zaiko_hinban_multiple:"dict[str, list[float]]",
                      is_a: bool)->None:
        """
        抽象メソッド
        """

from abc import abstractclassmethod,ABCMeta
from typing import NoReturn
import subprocess
class SysAPI(object,metaclass=ABCMeta):
    def __init__(self,packages:list,**kwargs):
        self.packages:list = packages
        self.kwargs = kwargs
    @abstractclassmethod
    def install(self)->NoReturn: pass
    @abstractclassmethod
    def uninstall(self)->NoReturn: pass
    @abstractclassmethod
    def update(self)->NoReturn: pass
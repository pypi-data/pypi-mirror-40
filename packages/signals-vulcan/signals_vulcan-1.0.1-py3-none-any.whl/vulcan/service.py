from abc import ABC, abstractclassmethod
import pandas as pd

HTTP_SERVICE = 'http'
SQL_SERVICE = 'sql'


class VulcanService(ABC):
    @abstractclassmethod
    def init(self):
        pass

    @abstractclassmethod
    def fetchAll(self):
        pass

    @abstractclassmethod
    def fetchOne(self):
        pass

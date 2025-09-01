import pandas as pd


class SqlDataSetLoader:
    def __init__(self, path:str):
        self.df=pd.read_csv(path, header=0)
        pass
    def getDataFrame(self):
        return self.df


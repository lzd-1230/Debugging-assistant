import pandas as pd


def get_data_from_file(path: str) -> pd.DataFrame:
    if(path.split(".")[-1] == "csv"):
        dataframe = pd.read_csv(path,header=0,encoding="gbk")
        data_set = dataframe.iloc[:,0]
        # print(type(data_set))
        return data_set

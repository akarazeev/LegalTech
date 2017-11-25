import pandas as pd


def get_data():
    """
    Load .xlsx file as dataframe
    :return:
    """
    return pd.read_excel('data.xlsx', sheetname='Sheet2')
import pandas as pd
import json

def get_data():
    """
    Load .xlsx file as dataframe.
    :return:
    """
    return pd.read_excel('data.xlsx', sheetname='Sheet2')


def get_jsdata():
    """
    Load .json file as dict.
    :return:
    """
    with open('json_1', 'r') as f:
        jsdata = json.load(f)
    return jsdata

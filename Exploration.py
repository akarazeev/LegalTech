import numpy as np
import pandas as pd

ls

df = pd.read_excel('FilteredViewTransactionsExpensesAll_CSILakiMIesNet_Eng.xlsx')


df.head(2)

for colname in df.columns:
    # print(df['Principal / Toimeksiantaja'].value_counts()()
    value_counts = df[colname].value_counts()
    print(colname, '\n', 'n different values is\n', len(value_counts), 'most popular is', value_counts.head(10))






df.info()







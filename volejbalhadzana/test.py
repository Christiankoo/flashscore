import pandas as pd

df_check = pd.read_csv(r'checked.csv')
print(df_check)
df_check.to_csv(r'checked.csv',index=False)

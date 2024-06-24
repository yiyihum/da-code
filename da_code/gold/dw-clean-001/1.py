import pandas as pd

df = pd.read_csv('../parking_violation.csv')

df['Violation Location'] = df['Violation Location'].astype(str).str.zfill(4)

df['Vehicle Body Type'] = df['Vehicle Body Type'].str.replace('P-U', 'TRK')

df['Street Name'] = df['Street Name'].str.title()

df['Plate ID'] = df['Plate ID'].str.replace(r'[A-Z]', '-', regex=True)

df.to_csv('updated_parking_violation.csv', index=False)
import pandas as pd
import duckdb

df_books=pd.read_csv("../Books.csv")
df_ratings=pd.read_csv("../Ratings.csv")
df_users=pd.read_csv("../Users.csv")

# 重命名列
df_ratings=df_ratings.rename(columns={"User-ID": "ID", "Book-Rating":"Rating"})
df_users=df_users.rename(columns={"User-ID": "ID"})
df_books=df_books.rename(columns={"Book-Title":"Title","Book-Author":"Author", "Year-Of-Publication":"Publication"})

#rating in books 
df1=duckdb.query("SELECT a.ID,a.Rating,b.* FROM df_ratings as a left join df_books as b on a.ISBN=b.ISBN ").df()
#users in df1
df=duckdb.query("SELECT a.*,b.Location, b.Age FROM df1 as a left join df_users as b on a.ID=b.ID ").df()

df.isna().sum()

df=df.drop(['Image-URL-S', 'Image-URL-M','Image-URL-L'], axis=1)
df['Age']=df.Age.fillna(30)
df['Age'] = pd.cut(x=df['Age'], bins=[0, 13, 19, 25, 65, 300], labels=['child', 'teenager', 'young','adult', 'old'])

query_result = duckdb.query("SELECT Age,count(*) AS total FROM df group by age ").df()

query_result.to_csv('./result.csv')
import pandas as pd
import os
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio

df = pd.read_csv('../Spotify_Youtube.csv')
# Remove unused columns
df = df.drop(['Unnamed: 0','Uri','Url_spotify', 'Url_youtube', 'Description'], axis=1)
# Check null values
df.isna().sum()
# Remove null values
df.dropna(inplace=True)
# Check duplicates
duplicates = df.duplicated(subset='Track', keep=False)
duplicates.value_counts()
# Delete duplicates
df= df.drop_duplicates(subset='Track')
album_types = df.groupby('Album_type', as_index=False)['Album'].count()

fig = px.pie(album_types, values='Album', names='Album_type',color_discrete_sequence=[ '#057fdc','green', 'orange'])
fig.update_traces(textinfo='percent+label', textfont_size=18, marker=dict(line=dict(color='white', width=1.5)))
fig.update_layout(title = 'Type of Albums', title_x =0.5, width=1000, height=600)
# Calculate mean values
mean_Danceability = np.mean(df['Danceability'])
mean_Energy = np.mean(df['Energy'])

fig = make_subplots(rows=1, cols=2)

# Left graph
fig.add_trace(px.histogram(df, x='Danceability').data[0], row=1, col=1)
fig.update_xaxes(title_text='Danceability', row=1, col=1)
fig.update_yaxes(title_text='Tracks', row=1, col=1)
fig.add_annotation(x=0,y=1.05, text=f"Mean: {mean_Danceability:.2f}", showarrow=False, xref="paper", yref="paper", font=dict(size=15))

# Right graph
fig.add_trace(px.histogram(df, x='Energy').data[0], row=1, col=2)
fig.update_xaxes(title_text='Energy', row=1, col=2)
fig.add_annotation(x=1,y=1.05, text=f"Mean: {mean_Energy:.2f}", showarrow=False, xref="paper", yref="paper", font=dict(size=15))

fig.update_layout(title='Distribution of Danceability and Energy', title_x=0.5, title_xanchor = 'center',width=1000, height=600)
# Calculate mean values
mean_Liveness = np.mean(df['Liveness'])
mean_Valence = np.mean(df['Valence'])

fig = make_subplots(rows=1, cols=2)

#Left graph
fig.add_trace(px.histogram(df, x='Liveness').data[0], row=1, col=1)
fig.update_xaxes(title='Liveness', row=1, col=1)
fig.update_yaxes(title='Tracks', row=1, col=1)
fig.add_annotation(x=0,y=1.05, text=f"Mean: {mean_Liveness:.2f}", showarrow=False, xref="paper", yref="paper", font=dict(size=15))

# Right graph
fig.add_trace(px.histogram(df, x='Valence').data[0], row=1, col=2)
fig.update_xaxes(title='Valence', row=1, col=2)
fig.add_annotation(x=1,y=1.05, text=f"Mean: {mean_Valence:.2f}", showarrow=False, xref="paper", yref="paper", font=dict(size=15))

fig.update_layout(title='Distribution of Liveness and Valence', title_x=0.5, title_xanchor= 'center',width=1000, height=600)
# Calculate mean value
mean_Loudness = np.mean(df['Loudness'])

fig = px.histogram(df, x = 'Loudness')
fig.update_layout(title ='Distribution of Loudness', title_x=0.5, title_xanchor= 'center',width = 1000, height = 600)
fig.add_annotation(x=0,y=1.05, text=f"Mean: {mean_Loudness:.2f}", showarrow=False, xref="paper", yref="paper", font=dict(size=15))
fig.update_xaxes(title_text='Loudness')
fig.update_yaxes(title_text='Tracks')
views = df.groupby(['Views','Stream'], as_index=False)['Track'].sum().sort_values('Views', ascending= False)[:10]
views['Views (millions)'] = views['Views'] / 1000000
views['Stream (millions)'] = views['Stream'] / 1000000
stream = views.sort_values('Stream', ascending=False)[:10]
# Create subplot figure with two horizontal subplots
fig = make_subplots(rows=1, cols=2)
# Left graph
fig.add_trace(px.bar(views, x='Views', y='Track', orientation='h',color_discrete_sequence=['#057fdc']).data[0], row=1, col=1)
fig.update_xaxes(title='Views (billions) on YouTube',row=1, col=1)
fig.update_yaxes(categoryorder='total ascending', row=1, col=1)
# Right graph
bar2 =fig.add_trace(px.bar(stream, x='Stream', y='Track', orientation='h',color_discrete_sequence=['#057fdc']).data[0],row=1, col=2)
fig.update_xaxes(title='Stream (billions) on Spotify', row=1, col=2)
fig.update_yaxes(categoryorder='total ascending', row=1, col=2)
fig.update_layout(title = 'Top Ten Songs By Most Views on YouTube and Stream on Spotify', title_x=0.5,
                  showlegend=False, height= 600)
top_artist_views = df.groupby('Artist', as_index =False)['Views'].sum().sort_values('Views', ascending=False)[:10]
top_artist_stream= df.groupby('Artist', as_index =False)['Stream'].sum().sort_values('Stream', ascending=False)[:10]
fig = make_subplots(rows =1, cols =2) 
#Left graph
fig.add_trace(px.bar(top_artist_views, x = 'Artist', y='Views').data[0], row = 1, col =1)
fig.update_xaxes(title='Artist', row =1, col=1)
fig.update_yaxes(title='Views (billions) on YouTube', row =1, col=1)
# Right graph
fig.add_trace(px.bar(top_artist_stream, x = 'Artist', y='Stream').data[0], row = 1, col =2)
fig.update_xaxes(title='Artist', row =1, col=2)
fig.update_yaxes(title='Stream (billions) on Spotify', row =1, col=2)
fig.update_layout(title = 'Top Ten Artists on YouTube and Spotify by Total Views and Streams', title_x=0.5, width = 1000, height =600)
# Correlation coefficient
corr = np.corrcoef(df['Loudness'], df['Energy'])[0,1]
fig = px.scatter(df, x='Loudness', y='Energy')
fig.update_layout(title = 'Loudness vs Energy', title_x = 0.5, title_xanchor = 'center',width= 1000, height = 600)
fig.update_xaxes(title ='Loudness (db)')
fig.add_annotation(x=0,y=1.05, text=f"Correlation: {corr:.2f}", showarrow=False, xref="paper", yref="paper", font=dict(size=16))
fig.show()
# Correlation coefficient
corr2 = np.corrcoef(df['Acousticness'], df['Energy'])[0,1]
corr3 = np.corrcoef(df['Acousticness'], df['Loudness'])[0,1]
# Left graph
fig =make_subplots(rows=1, cols =2)
fig.add_trace(px.scatter(df, x='Acousticness', y='Energy').data[0], row=1, col=1)
fig.update_xaxes(title = 'Energy', row=1, col = 1)
fig.update_yaxes(title = 'Acousticnes', row =1, col =1)
fig.add_annotation(x=0,y=1.05, text=f"Correlation: {corr2:.2f}", showarrow=False, xref="paper", yref="paper", font=dict(size=15))
# Right graph
fig.add_trace(px.scatter(df, x='Acousticness', y='Loudness').data[0], row=1, col=2)
fig.update_yaxes(title = 'Loudness', row =1, col =2)
fig.update_xaxes(title = 'Acousticnes', row =1, col =2)
fig.add_annotation(x=1,y=1.05, text=f"Correlation: {corr3:.2f}", showarrow=False, xref="paper", yref="paper", font=dict(size=15))

fig.update_layout(title = 'Acousticness vs Energy and Loudness', title_x = 0.5, title_xanchor = 'center',width= 1000, height = 600)

fig.show()

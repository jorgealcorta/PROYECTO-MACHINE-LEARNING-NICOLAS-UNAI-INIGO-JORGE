import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#LOAD DATA
df = pd.read_csv("datasets_kaggle/dataset_unido_anyadidos.csv", sep=";")
df.describe()

#COLORS
colors = ["#5AC953"]
sns.set(rc={'axes.facecolor':'F6F6F6', 'figure.facecolor':'FFFFFF'})
sns.set_palette(sns.color_palette(colors))

#DISTRIBUTION PLOT
sns.distplot(df['popularity']).set_title('Popularity Distribution')

#DISTRIBUTIONS FOR SONGS WITH MORE THAN 50 POPULARITY
df_gt50 = df.loc[df['popularity'] >= 50]
sns.distplot(df_gt50['acousticness'])
plt.show()
#DISTRIBUTIONS FOR SONGS WITH LESS THAN 50 POPULARITY
df_lt50 = df.loc[df['popularity'] < 50]
sns.distplot(df_lt50['acousticness'])

sns.pairplot(df)

plt.show()
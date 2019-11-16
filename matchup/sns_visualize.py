#!/usr/bin/env python
# coding: utf-8

# In[79]:


import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[125]:


df_league = pd.read_csv('points.csv')
div1 = pd.read_csv('div1.csv')
div2 = pd.read_csv('div2.csv')

# import point-data player
scc = pd.read_csv('points-scc.csv')
kev = pd.read_csv('points-kev.csv')
lazn = pd.read_csv('points-lazn.csv')
janis = pd.read_csv('points-janis.csv')
ct = pd.read_csv('points-ct.csv')
maxi = pd.read_csv('points-max.csv')

au_scc = pd.read_csv('janissam.csv')

# In[126]:


print(df_league.head(10))


# In[127]:


player = df_league['manager_name']
print(player)


# In[128]:


# points = []
# players = []
# week = ['1','2','3','4']

# for player in df['player_name']:
#     players.append(player)
# for point in df['points']:
#     points.append(point)

# print(players) 
# print(points)     

# In[129]:


sns.catplot(x='week', y="points", hue="team", data=df_league, kind="swarm")


# In[130]:


sns.catplot(x='week', y="points", hue="manager_name", data=div1, kind="swarm")
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[131]:


sns.catplot(x='week', y="points", hue="manager_name", data=div2, kind="swarm")
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[176]:


sns.lineplot(x="week", y="points", hue="team", data=au_scc)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[178]:


sns.lineplot(x="week", y="points", hue="team", data=div2)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[182]:


sns.catplot(x='week', y="points", hue="player_name", data=scc, kind="swarm")
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[183]:


sns.catplot(x='week', y="points", hue="player_name", data=kev, kind="swarm")


# In[184]:


sns.catplot(x='week', y="points", hue="player_name", data=janis, kind="swarm")


# In[185]:


sns.catplot(x='week', y="points", hue="player_name", data=ct, kind="swarm")


# In[186]:


sns.catplot(x='week', y="points", hue="player_name", data=lazn, kind="swarm")


# In[187]:


sns.catplot(x='week', y="points", hue="player_name", data=maxi, kind="swarm")


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[14]:


import plotly as py
import plotly.express as px
import plotly as py
import pandas as pd

df = pd.read_csv('points.csv')
div1 = pd.read_csv('div1.csv')
div2 = pd.read_csv('div2.csv')

league = px.scatter(df, x='week', y='points',color='team', hover_data=['player_name'])
league.show()


# In[15]:


league = px.line(div1, x="week", y="points", color="team",
              line_group="player_name", hover_name="player_name")
league.show()


# In[24]:


league = px.line(div2, x="week", y="points", color="team",
              line_group="player_name", hover_name="player_name")
league.show()


# In[ ]:





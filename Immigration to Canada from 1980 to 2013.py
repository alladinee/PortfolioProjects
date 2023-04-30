#!/usr/bin/env python
# coding: utf-8

# ### Importing libraries 

# In[6]:


import numpy as np
import pandas as pd


# ### Importing Data 

# In[42]:


df_can = pd.read_excel('excel_file.xlsx',
    sheet_name='Canada by Citizenship',
    skiprows=range(20),
    skipfooter=2)
df_can.head()


# ### Some informations about our Data

# In[44]:


# get a short summary of the dataframe.
df_can.info(verbose=False)


# In[45]:


# get the list of column headers
df_can.columns


# In[46]:


#get the list of indices
df_can.index


# In[47]:


print(type(df_can.columns))
print(type(df_can.index))


# Note: The default type of intance variables `index` and `columns` are **NOT** `list`.
# 

# In[51]:


#get the index and columns as lists
df_can.columns.to_list()
df_can.index.tolist()


# In[52]:


# the dimensions of the dataframe
df_can.shape


# ### Let's clean the data set to remove a few unnecessary columns.

# In[53]:


# in oandas axis=0 represent rows (default) and axis=1 represent columns
df_can.drop(['AREA','REG','DEV','Type','Coverage'],axis=1, inplace=True)
df_can.head(2)


# In[55]:


# Rename the columns so that they make sense
df_can.rename(columns={'OdName':'Country','AreaName':'Continent','RegName':'Region'},inplace=True)
df_can.columns


# In[64]:


# We will also add a 'Total' column that sums up the total immigrants by country over the entire period 1980 - 2013
df_can['Total'] = df_can.sum(axis=1)


# #### We can check to see how many null objects we have in the dataset

# In[66]:


df_can.isnull().sum()


# In[67]:


#let's view a quick summary of each column in our dataframe
df_can.describe()


# ***
# ### Select Column
# 
# **There are two ways to filter on a column name:**
# 
# Method 1: Quick and easy, but only works if the column name does NOT have spaces or special characters.
# 
# ```python
#     df.column_name               # returns series
# ```
# 
# Method 2: More robust, and can filter on multiple columns.
# 
# ```python
#     df['column']                  # returns series
# ```
# 
# ```python
#     df[['column 1', 'column 2']]  # returns dataframe
# ```
# 
# ***
# 

# In[68]:


# Let's try filtering on the list of countries ('Country')
df_can.Country # Returns a series


# In[69]:


# Let's try filtering on the list of countries ('Country') and the data for years: 1980 - 1985.
df_can[['Country',1980,1981,1982,1983,1984,1985]] # Returns a dataframe
# Notice that 'Country' is string, and the years are integers.
# For the sake of consistency, we will convert all column names to string Later on. 


# In[70]:


# Notice that the default index of the dataset is a numeric range from 0 to 194
# This can be fixed very easily by setting the 'Country' column as the index
df_can.set_index('Country',inplace=True)


# In[71]:


df_can.head(2)


# <p> Let's view the number of immigrants from Japan (row 87) for the following scenarios: 1. The full row data (all columns) 2. For year 2013 3. For years 1980 to 1985 </p>

# In[72]:


# 1. The full row data
df_can.loc['Japan']


# In[73]:


# Alternate Methods
df_can.iloc[87]


# In[77]:


df_can.loc[df_can.index=='Japan']


# In[78]:


# 2. for year 2013
df_can.loc['Japan',2013]


# In[79]:


# Alrtenate Method
# year 2013 is the last column, with a positional index of 36
df_can.iloc[87,36]


# In[80]:


# 3. For years 1980 to 1985
df_can.loc['Japan',[1980,1981,1982,1983,1984,1985]]


# In[81]:


# Alternate Mathod
df_can.iloc[87,[3,4,5,6,7,8]]


# Column names that are integers (such as the years) might introduce some confusion. For example, when we are referencing the year 2013, one might confuse that when the 2013th positional index.
# 
# To avoid this ambuigity, let's convert the column names into strings: '1980' to '2013'.

# In[85]:


df_can.columns=list(map(str,df_can.columns))
#[print (type(x)) for x in df_can.columns.values] #<-- uncomment to check type of column headers


# Since we converted the years to string, let's declare a variable that will allow us to easily call upon the full range of years

# In[86]:


# This is useful for plotting later on
years=list(map(str,range(1980,2014)))


# #### Let's filter the dataframe to show the data on Asian countries (AreaName = Asia).

# In[92]:


#1. Create the condition boolean series
condition=df_can['Continent']=='Asia'
print(condition)


# In[93]:


# 2. Pass this condition into the dataframe
df_can[condition]


# In[94]:


# we can pass multiple criteria in the same line.
# let's filter for AreaNAme = Asia and RegName = Southern Asia

df_can[(df_can['Continent']=='Asia') & (df_can['Region']=='Southern Asia')]


# let's review the changes we have made to our dataframe

# In[95]:


print('data dimensions:', df_can.shape)
print(df_can.columns)
df_can.head(2)


# ***
# 
# # Visualizing Data<a id="8"></a>
# 

# In[96]:


# Let's start by importing matplotlib and matplotlib.pyplot
get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib as mpl
import matplotlib.pyplot as plt


# In[98]:


# apply a style to Matplotlib
print(plt.style.available)
mpl.style.use(['ggplot']) # optional: for ggplot-like style


# # Line Pots (Series/Dataframe) <a id="12"></a>

# **Let's start with a case study:**
# 
# In 2010, Haiti suffered a catastrophic magnitude 7.0 earthquake. The quake caused widespread devastation and loss of life and aout three million people were affected by this natural disaster. As part of Canada's humanitarian effort, the Government of Canada stepped up its effort in accepting refugees from Haiti. We can quickly visualize this effort using a `Line` plot

# In[99]:


# First, we will extract the data series for Haiti.
haiti = df_can.loc['Haiti',years]
haiti.head()


# In[100]:


#Next, we will plot a line plot 
haiti.plot()


# In[101]:


# let's label the x and y axis
haiti.index = haiti.index.map(int) #change the index values of Haiti to type integer for plotting
haiti.plot(kind='line')

plt.title('Immigration from haiti')
plt.ylabel('Number of immigrants')
plt.xlabel('Years')

plt.show()


# We can clearly notice how number of immigrants from Haiti spiked up from 2010 as Canada stepped up its efforts to accept refugees from Haiti.

# In[108]:


# Let's annotate this spike in the plot
haiti.plot(kind='line')

plt.title('Immigration from Haiti')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')

# annotate the 2010 Earthquake. 
# syntax: plt.text(x, y, label)
plt.text(2000, 6000, '2010 Earthquake') # see note below

plt.show() 


# #### Let's compare the number of immigrants from India and China from 1980 to 2013.

# In[109]:


df_CI = df_can.loc[['India','China'], years]
df_CI


# In[113]:


# We must first transpose the dataframe
df_CI = df_CI.transpose()

#  Plot graph
df_CI.plot(kind='line')

plt.title('Immigration India and China')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')

# annotate the 2010 Earthquake. 
# syntax: plt.text(x, y, label)
#plt.text(2000, 6000, '2010 Earthquake') # see note below

plt.show() 


# <br>From the above plot, we can observe that the China and India have very similar immigration trends through the years.

# ### Compare the trend of top 5 countries that contributed the most to immigration to Canada.

# In[119]:


#Step 1: Get the dataset

#We will sort on this column to get our top 5 countries
df_can.sort_values(by='Total', ascending=False, axis=0,inplace =True)

# Get the top 5 entries
df_top5 = df_can.head(5)

# Transpose the dataframe
df_top5 = df_top5[years].transpose()

print(df_top5)


# In[118]:





# In[120]:


#Step 2: Plot the dataframe
df_top5.index=df_top5.index.map(int) # Change the index Values of df_top5 to type integer for plotting
df_top5.plot(kind='line',figsize=(14,8)) 

plt.title('Immigration Trend of Top 5 Countries')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')

plt.show()


# ### Thank you
# 
# ## By
# 
# <a href="https://www.linkedin.com/in/n-lardjn/">LARDJANE Noufe Aladdine</a>

# In[ ]:





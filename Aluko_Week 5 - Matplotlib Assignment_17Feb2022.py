#!/usr/bin/env python
# coding: utf-8

# Title: Week 5 - Matplotlib Assignment
# 
# Date: 17FFEB2022 
# 
# Author: Olumide Aluko 
# 
# Purpose: Write the matplotlib code and push to GitHub, submit link

# Input:
# 
# Output:
# 
# Notes: Week 5 - Project

# Import the relevant libraries:

# In[1]:


# %matplotlib inline
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
plt.style.use('seaborn')


# # Import Dataset
# 
# The Food Demand Forcasting dataset has three dataframes: df_meal describing the meals, df_center describing the food centers, and df_food describing the overall food order. Lets take a look at dataset below.
# 
# Source: https://www.kaggle.com/kannanaikkal/food-demand-forecasting

# In[2]:


df_meal = pd.read_csv("meal_info.csv")
df_meal.head()


# In[3]:


df_center = pd.read_csv("fulfilment_center_info.csv")
df_center.head()


# In[4]:


df_food = pd.read_csv("train_food.csv")
df_food.head()


# I will first merge all the three dataframes into a single dataframe. This will make it easier to manipulate the data while plotting it:

# In[5]:


df = pd.merge(df_food,df_center,on='center_id') 
df = pd.merge(df,df_meal,on='meal_id')


# # Lets plot a Bar Graph using matplotlib.
# 
# First, we want to find the most popular food item that customers have bought from the company. I will be using the Pandas pivot_table function to find the total number of orders for each category of the food item:

# In[6]:


table = pd.pivot_table(data=df,index='category',values='num_orders',aggfunc=np.sum)
table


# Now, lets visualize this using a bar graph.

# In[7]:


#bar graph
plt.bar(table.index,table['num_orders'])

#xticks 
plt.xticks(rotation=70) 

#x-axis labels 
plt.xlabel('Food item') 

#y-axis labels 
plt.ylabel('Quantity sold') 

#plot title 
plt.title('Most popular food') 

#display 
plt.show()


# While analyzing the plot, one can see that Beverages were the most popular food item sold by the company. Was Rice Bowl the most popular food item?
# Let’s divide the total food item order by the number of unique meals it is present in.

# In[8]:


#dictionary for meals per food item
item_count = {}

for i in range(table.index.nunique()):
    item_count[table.index[i]] = table.num_orders[i]/df_meal[df_meal['category']==table.index[i]].shape[0]

#bar plot 
plt.bar([x for x in item_count.keys()],[x for x in item_count.values()],color='orange')

#adjust xticks
plt.xticks(rotation=70)

#label x-axis
plt.xlabel('Food item')

#label y-axis
plt.ylabel('No. of meals')

#label the plot
plt.title('Meals per food item')

#display plot
plt.show();


# From the Bar Chart above, Rice Bowl was indeed the most popular food item sold by the company.

# # Box Plot using matplotlib
# 
# Let’s check out which one is the most expensive cuisine! For this, I will be using a Box Plot.

# In[9]:


#dictionary for base price per cuisine
c_price = {}
for i in df['cuisine'].unique():
    c_price[i] = df[df['cuisine']==i].base_price


# Plotting the boxplot below:

# In[11]:


#plotting boxplot 
plt.boxplot([x for x in c_price.values()],labels=[x for x in c_price.keys()]) 

#x and y-axis labels 
plt.xlabel('Cuisine') 
plt.ylabel('Price') 

#plot title 
plt.title('Analysing cuisine price') 

#save and display  
plt.show();


#  Continental cuisine was the most expensive cuisine served by the company! Even its median price is higher than the maximum price of all the cuisines.

# # Histogram using matplotlib
# 
# Since base_price is a continuous variable, we will inspect its range in different distinct orders using a histogram. We can do this using plt.hist().

# In[12]:


#plotting histogram 
plt.hist(df['base_price'],rwidth=0.9,alpha=0.3,color='blue',bins=15,edgecolor='red') 

#x and y-axis labels 
plt.xlabel('Base price range') 
plt.ylabel('Distinct order') 

#plot title 
plt.title('Inspecting price effect') 

#save and display the plot 
plt.show();


# I have selected the number of bins as 15 and it is evident that most of the orders had a base price of ~300.

# # Scatter Plot using matplotlib
# 
# I will try to evaluate whether the center type had any impact on the number of orders from different center types. I will do this by comparing a scatter plot, a boxplot and a bar graph in the same figure below.

# In[14]:


center_type_name = ['TYPE_A','TYPE_B','TYPE_C'] 

#relation between op area and number of orders 
op_table=pd.pivot_table(df,index='op_area',values='num_orders',aggfunc=np.sum) 

#relation between center type and op area 
c_type = {} 
for i in center_type_name: 
    c_type[i] = df[df['center_type']==i].op_area 

#relation between center type and num of orders 
center_table=pd.pivot_table(df,index='center_type',values='num_orders',aggfunc=np.sum) 

#subplots 
fig,ax = plt.subplots(nrows=3,ncols=1,figsize=(8,12)) 

#scatter plots 
ax[0].scatter(op_table.index,op_table['num_orders'],color='pink') 
ax[0].set_xlabel('Operation area') 
ax[0].set_ylabel('Number of orders') 
ax[0].set_title('Does operation area affect num of orders?') 
ax[0].annotate('optimum operation area of 4 km^2',xy=(4.2,1.1*10**7),xytext=(7,1.1*10**7),arrowprops=dict(facecolor='black', shrink=0.05),fontsize=12) 

#boxplot 
ax[1].boxplot([x for x in c_type.values()], labels=[x for x in c_type.keys()]) 
ax[1].set_xlabel('Center type') 
ax[1].set_ylabel('Operation area') 
ax[1].set_title('Which center type had the optimum operation area?') 

#bar graph 
ax[2].bar(center_table.index,center_table['num_orders'],alpha=0.7,color='orange',width=0.5) 
ax[2].set_xlabel('Center type') 
ax[2].set_ylabel('Number of orders') 
ax[2].set_title('Orders per center type') 

#show figure 
plt.tight_layout() 

plt.show();


# The scatter plot makes it instantly visible that the optimum operation area of a center is 4 km sq. The boxplot shows that the TYPE_A center type had the most number of optimum size centers because of a compact box with a median around 4 km sq. Because of this, they had more orders placed by customers than any other center type.

# # Line Plot and Subplots using matplotlib
# 
# A line plot is useful for visualizing the trend in a numerical value over a continuous time interval.
# 
# How are the weekly and monthly sales of the company varying? This is a critical business question that makes or breaks the marketing strategy.
# 
# Before exploring that, I will create two lists for storing the week-wise and month-wise revenue of the company:

# In[16]:


#new revenue column 
df['revenue'] = df.apply(lambda x: x.checkout_price*x.num_orders,axis=1) 

#new month column 
df['month'] = df['week'].apply(lambda x: x//4) 

#list to store month-wise revenue 
month=[] 
month_order=[] 

for i in range(max(df['month'])):
    month.append(i) 
    month_order.append(df[df['month']==i].revenue.sum()) 
    
#list to store week-wise revenue 
week=[] 
week_order=[] 

for i in range(max(df['week'])): 
    week.append(i) 
    week_order.append(df[df['week']==i].revenue.sum())


# In[17]:


#subplots returns a Figure and an Axes object 
fig,ax=plt.subplots(nrows=1,ncols=2,figsize=(20,5)) 

#manipulating the first Axes 
ax[0].plot(week,week_order) 
ax[0].set_xlabel('Week') 
ax[0].set_ylabel('Revenue') 
ax[0].set_title('Weekly income') 

#manipulating the second Axes 
ax[1].plot(month,month_order) 
ax[1].set_xlabel('Month') 
ax[1].set_ylabel('Revenue') 
ax[1].set_title('Monthly income') 

#save and display the plot 
plt.show();


# We can see an increasing trend in the number of food orders with the number of weeks and months, though the trend is not very strong.

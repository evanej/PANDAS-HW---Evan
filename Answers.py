#!/usr/bin/env python
# coding: utf-8

# HW #4 -- Pandas - School Data
# Evan Johnson
# June 20, 2019
# 
# # OVERALL FINDINGS: 
# 
# 1) Budget per pupil has little effect on test scores.  If anything, a slight negative relationship appears
# 2) School size appears to bear a strong negative relationship with test scores
# 3) Unsurprisingly, charter school students perform better on tests than public students, though the effect probably diminishes when school size is also taken into account.  

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# Specify file locations for data files

schools = "Instructions/PyCitySchools/Resources/schools_complete.csv"
students = "Instructions/PyCitySchools/Resources/students_complete.csv"


# In[3]:



# Read CSV Files

schools_df = pd.read_csv(schools)
students_df = pd.read_csv(students)
students_df.head()
schools_df


# In[4]:


students_df


# In[5]:


# Merge into one data frame:

merged = pd.merge(schools_df, students_df, on="school_name")
merged


# In[6]:


#count nuymber of schools
total_schools = schools_df["School ID"].count()
total_schools


# In[7]:


#count number of students
total_students = students_df["Student ID"].count()
total_students


# In[8]:


#Total Budget
total_budget = schools_df["budget"].sum()
total_budget

#Per student Budget
per_student_budget = total_budget/total_students

total_budget


# In[9]:


per_student_budget


# In[10]:


#Average Reading
average_reading = students_df['reading_score'].mean()
average_reading


# In[11]:


#Average Math
average_math = students_df['math_score'].mean()
average_math


# In[12]:


# % Passing Math
pass_math = (students_df['math_score']>=70).sum()/total_students
pass_math*100


# In[13]:


# % Passing Reading
pass_reading = (students_df['reading_score']>=70).sum()/total_students
pass_reading*100


# In[14]:


# Overall Passing Rate (Average of the above two)
pass_overall = (pass_math+pass_reading)/2
pass_overall*100


# In[15]:


district_summary_df = pd.DataFrame({
    "Total Schools":[total_schools],
    "Total Budget":[total_budget],
    "Total Students":[total_students],
    "Avg Math Score":[average_math],
    "Avg Reading Score":[average_reading],
    "Percentage Passing Math":[pass_math],
    "Percentage Passing Reading":[pass_reading],
    "Percentage Passing Overall":[pass_overall]
})
district_summary_df


# In[25]:


school = schools_df["school_name"]
school_type = schools_df["type"]
students = schools_df["size"]
budget = schools_df["budget"]
math_average = merged.groupby(["school_name"])["math_score"].mean()
reading_average = merged.groupby(["school_name"])["reading_score"].mean()
math_passing = merged[students_df.math_score>=70].groupby('school_name')['math_score'].count()/merged.groupby(["school_name"])["Student ID"].count()
math_passing = math_passing *100
reading_passing = merged[students_df.reading_score>=70].groupby('school_name')['reading_score'].count()/merged.groupby(["school_name"])["Student ID"].count()
reading_passing = reading_passing*100
overall_passing = (math_passing + reading_passing)/2

school_overview1_df = pd.DataFrame({
    "School":school,
    "School Type":school_type,
    "Total Students":students,
    "Total Budget":total_budget,
    "Budget Per School":budget
})
school_overview2_df = pd.DataFrame({
    "Avg Math Score":math_average,
    "Avg Reading Score":reading_average,
    "Percentage Passing Math":math_passing,
    "Percentage Passing Reading":reading_passing,
    "Percentage Passing Overall":overall_passing
})

school_overview = school_overview1_df.join(school_overview2_df,on='School',how='inner')
school_overview


# In[26]:



top5_df = school_overview.sort_values("Percentage Passing Overall", ascending=False)
top5_df = top5_df.head()
top5_df


# In[27]:



bottom5_df = school_overview.sort_values("Percentage Passing Overall", ascending=True)
bottom5_df = bottom5_df.head()
bottom5_df


# In[29]:


ninth = merged[(merged["grade"] == "9th")]
tenth = merged[(merged["grade"] == "10th")]
eleventh = merged[(merged["grade"] == "11th")]
twelfth = merged[(merged["grade"] == "12th")]

ninthscore = ninth.groupby("school_name")["math_score"].mean()
tenthscore = tenth.groupby("school_name")["math_score"].mean()
eleventhscore = eleventh.groupby("school_name")["math_score"].mean()
twelfthscore = twelfth.groupby("school_name")["math_score"].mean()

mathscores=pd.DataFrame({
    "9th":ninthscore,
    "10th":tenthscore,
    "11th":eleventhscore,
    "12th":twelfthscore
})
mathscores


# In[30]:


ninereading = ninth.groupby("school_name")["reading_score"].mean()
tenreading = tenth.groupby("school_name")["reading_score"].mean()
elevenreading = eleventh.groupby("school_name")["reading_score"].mean()
twelvereading = twelfth.groupby("school_name")["reading_score"].mean()

readingscores=pd.DataFrame({
    "9th":ninereading,
    "10th":tenreading,
    "11th":elevenreading,
    "12th":twelvereading
})
readingscores


# In[39]:


budget_per_student = budget/students
bins = [0,600,659,699,800]
labels = ["<600","600-659", "660-699","700-800"]
school_overview["Spending Ranges"] = pd.cut(budget_per_student,bins,labels=labels)

spendingmath = school_overview.groupby("Spending Ranges").mean()["Avg Math Score"]
spendingreading = school_overview.groupby("Spending Ranges").mean()["Avg Reading Score"]
spendingmathpass = school_overview.groupby("Spending Ranges").mean()["Percentage Passing Math"]
spendingreadpass = school_overview.groupby("Spending Ranges").mean()["Percentage Passing Reading"]
spendingoverallpass = (spendingmath+spendingreading)/2

spending_summary = pd.DataFrame({
    "Average Math Score":spendingmath,
    "Average Reading Score":spendingreading,
    "Passing Math":spendingmathpass,
    "Passing Reading":spendingreadpass,
    "Passing Overall":spendingoverallpass
})
spending_summary


# In[40]:



sizebins = [0,2000,4000,6000]
sizelabels = ["Small <2000","Medium 2000-4000","Large >4000"]
school_overview["Size Type"]=pd.cut(students,sizebins,labels=sizelabels)

sizemath = school_overview.groupby("Size Type").mean()["Avg Math Score"]
sizeread = school_overview.groupby("Size Type").mean()["Avg Reading Score"]
sizemathpass = school_overview.groupby("Size Type").mean()["Percentage Passing Math"]
sizereadpass = school_overview.groupby("Size Type").mean()["Percentage Passing Reading"]
sizeoverallpass = (sizemathpass+sizereadpass)/2

size_summary = pd.DataFrame({
    "Average Math Score":sizemath,
    "Average Reading Score":sizeread,
    "Passing Math":sizemathpass,
    "Passing Reading":sizereadpass,
    "Passing Overall":sizeoverallpass
})
size_summary


# In[37]:


mathtype = school_overview.groupby("School Type")["Avg Math Score"].mean()
readingtype = school_overview.groupby("School Type")["Avg Reading Score"].mean()
passmathtype = school_overview.groupby("School Type")["Percentage Passing Math"].mean() 
passreadtype = school_overview.groupby("School Type")["Percentage Passing Reading"].mean()

type_df = pd.DataFrame({
    "Average Math Score":mathtype,
    "Average Reading Score":readingtype,
    "Passing Math":passmathtype,
    "Passing Reading":passreadtype,
})
type_df


# In[ ]:





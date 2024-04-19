# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:58:15 2024

@author: pponnam
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\anude\Downloads\Untitled Folder\study_performance.csv")

df.describe()
df.info()

df = df.rename(columns = {'race_ethnicity' : 'group',
                          'parental_level_of_education' : 'parent_education_level',
                          'test_preparation_course' : 'test_preparation'})

# some high school replace with high school
df['parent_education_level'] = df['parent_education_level'].replace('some high school', 'high school')
df['parent_education_level'] = df['parent_education_level'].replace('some college', 'college')
df['parent_education_level'].value_counts()

df['total_score'] = df['math_score'] + df['reading_score'] + df['writing_score']
df['average_score'] = round(df['total_score'] / 3, 2)

print(df)

count_gender = df['gender'].value_counts()
gender = count_gender.index

plt.title('Distribution of Gender')
plt.pie(count_gender, labels = gender, autopct='%.1f%%')
plt.show()




mean_scores = df.groupby('parent_education_level')['average_score'].mean().round(2)

sns.barplot(x=mean_scores.index, y=mean_scores.values, color='skyblue')
plt.xticks(rotation=45)
plt.xlabel('Parent education level')
plt.ylabel('Average score')
plt.title('Average score by parental education level')
plt.show()


# Create a 3D scatter plot
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
ax.scatter(df['math_score'], df['reading_score'], df['writing_score'], c='blue', marker='o')

# Set labels and title
ax.set_xlabel('Math Score')
ax.set_ylabel('Reading Score')
ax.set_zlabel('Writing Score',labelpad=-1)
ax.set_title('3D Scatter Plot of Scores')
plt.show()


# Add result column based on average score
def categorize_result(score):
    if score > 75:
        return 'Distinction'
    elif score > 50:
        return 'Pass'
    else:
        return 'Fail'

df['result'] = df['average_score'].apply(categorize_result)

# Count number of students who achieved Distinction, Pass, or Fail based on preparation
result_prep_counts = df.groupby(['test_preparation', 'result']).size().unstack(fill_value=0)

# Plotting
ax = result_prep_counts.plot(kind='bar', stacked=True)

# Add annotations
for p in ax.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy() 
    ax.annotate(f'{height}', (x + width/2, y + height/2), ha='center', va='center')

plt.title('Students result based on Test Preparation')
plt.xlabel('Test Preparation')
plt.ylabel('Number of Students')
plt.xticks(rotation=0)
plt.legend(title='Result')
plt.show()


numeric_df = df.select_dtypes(include=['number'])
correlation_matrix = numeric_df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:58:15 2024

@author: pponnam
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

def download_data(url):
    """
    Function to downlaod the data from the url provided and 
    returns the data frame which has the downloaded data 

    """
    while(1):
        try:
        #fetch the data from url 
            response = requests.get(url)
            #check if we got a response from the url
            if response.status_code == 200:
            # Save the content of the response to a local CSV file
                with open("downloaded_data.csv", "wb") as f:
                    f.write(response.content)
                break
            else:
                print("Failed to download CSV file. Status code:",
                      response.status_code)
        #if exception is raised,continuing the loop
        except requests.exceptions.HTTPError :
            continue
        except requests.exceptions.ConnectionError :
            continue
        except requests.exceptions.Timeout :
            continue
        except requests.exceptions.RequestException :
            continue
    #moving data to dataframe from the downladed data
    df = pd.read_csv("downloaded_data.csv")
    return df



def categorize_result(score):
    """
    Function to return the result based on the score
    """
    if score > 75:
        return 'Distinction'
    elif score > 50:
        return 'Pass'
    else:
        return 'Fail'
    
    
def process_data(df):
    """ 
    Function to procees data like add/rename few columns
    """
    
    #renaming the columns
    df = df.rename(columns = {'race_ethnicity' : 'group',
                          'parental_level_of_education' : 'parent_education_level',
                          'test_preparation_course' : 'test_preparation'})

    # Replacing values of parent education level
    df['parent_education_level'] = df['parent_education_level'].replace(
                                        'some high school', 'high school')
    df['parent_education_level'] = df['parent_education_level'].replace(
                                        'some college', 'college')
    df['parent_education_level'].value_counts()

    #Adding total_score which is sum of all three scores
    df['total_score'] = df['math_score'] + df['reading_score'] + df['writing_score']

    #Adding average score column which is mean of all 3 scores
    df['average_score'] = round(df['total_score'] / 3, 2)

    # Add result column based on average score
    df['result'] = df['average_score'].apply(categorize_result)
    
    return df


def pie_chart(df):
    """
    Function to plot a pir chart which displays the gender distributions
    """
    
    # Count the number of males and females
    gender_counts = df['gender'].value_counts()

    # Create a pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(gender_counts, labels=gender_counts.index,
             autopct='%1.1f%%', startangle=140, colors=['lightblue', 'lightcoral'])
    #set the title
    plt.title('Distribution of Students by Gender')
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')  
    #show the plotg
    plt.show()
    return

def bar_chart(df):
    """ 
    Funtion to create a 3d sctter plot to understand the relation betwene the scores
    """
    
    # Calculate average score by parental education level
    avg_score_by_parent_education = df.groupby('parent_education_level')['average_score'].mean().reset_index()

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(avg_score_by_parent_education['parent_education_level'], 
            avg_score_by_parent_education['average_score'], color='skyblue')
    #set the labels,title
    plt.title('Average Score by Parental Education Level')
    plt.xlabel('Parental Education Level')
    plt.ylabel('Average Score')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    #show the plot
    plt.show()
    return

def scatter_plot(df):
    """ 
    Funtion to create a 3d sctter plot to understand the relation betwene the scores
    """
    # Create a 3D scatter plot
    fig = plt.figure(figsize=(9,6))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot
    ax.scatter(df['math_score'], df['reading_score'], 
                df['writing_score'], c='blue', marker='o')

    # Set labels and title
    ax.set_xlabel('Math Score')
    ax.set_ylabel('Reading Score')
    ax.set_zlabel('Writing Score',labelpad=-1)
    ax.set_title('3D Scatter Plot of Scores')
    #show the plot
    plt.show()
    return

def stacked_bar(df):
    """
    Function to display a stacked bar graphto display no of students
    based on test preparation
    """
    
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
    return

#url to download data
url = 'https://github.com/pratapponnam/DHS-Assignment/blob/main/study_performance.csv?raw=True'

#download data from url
df = download_data(url)

df = process_data(df)
#Using describe function for mean, stanadrd deviation, min and max value.
print('Stats of the data', end='\n')
df.describe()




#Display the table
print(df)

#display pie chart
pie_chart(df)

#display the bargraph
bar_chart(df)

#display the scatter plot
scatter_plot(df)

#display stacked bar graph
stacked_bar(df)

#df to have only numeric columns
numeric_df = df.select_dtypes(include=['number'])

#basic statistics of the data

print('Skewness of the data', end='\n')
print(numeric_df.skew() , end='\n\n')

print('Kurtosis of the data', end='\n')
print(numeric_df.kurtosis() , end='\n\n')

print('Correlation of the data', end='\n')
print(numeric_df.corr() , end='\n\n')

#display correlations of the data in heat map 
plt.figure(figsize=(10, 8))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()
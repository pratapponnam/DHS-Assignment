# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:58:15 2024

@author: pponnam
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import numpy as np

def download_data(url):
    """
    Function to download the data from the url provided and 
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
    Function to process data like add/rename a few columns
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
    Function to plot a pie chart which displays the gender distributions
    """
    
    # Count the number of males and females
    gender_counts = df['gender'].value_counts()
    
    explode = [0.1 if i == 0 else 0 for i in range(len(gender_counts))]

    # Create a pie chart
    plt.figure(figsize=(8, 6))
    patches,labels,_ = plt.pie(gender_counts, labels=gender_counts.index,
             autopct='%1.1f%%', startangle=140, colors=['lightpink','skyblue'],
             explode=explode )
    for label in labels:
        label.set_fontweight('bold')
    #set the title
    plt.title('Distribution of Students by Gender',fontsize=14,fontweight='bold')
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')  
    #Save and Show the plot
    plt.savefig('piechart.png')
    plt.show()    
    return


def bar_chart(df):
    """ 
    Function to create a bar chart to understand the relation between 
    average scores and parental education levels.
    """
    
    
    # Calculate average score by parental education level
    avg_score_by_parent_education = df.groupby('parent_education_level'
                                        )['average_score'].mean().reset_index()
    num_categories = df['parent_education_level'].nunique()
    # Create a color palette, using a colormap
    colors = plt.cm.viridis(np.linspace(0, 1, num_categories))
    # Create a list of patterns for bars
    patterns = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
    # Create a bar plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(avg_score_by_parent_education['parent_education_level'], 
               avg_score_by_parent_education['average_score'], 
               edgecolor='black', color=colors, hatch=patterns[:num_categories])
    
    
    # Set the font size of the values on the bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, round(height, 2),
                 ha='center', va='bottom', fontsize=12,fontweight='bold')
    #set the labels,title
    plt.title('Average score of Students by Parent Education Level',fontsize=14,fontweight='bold')
    plt.xlabel('Parent Education Level',fontsize=12,fontweight='bold')
    plt.ylabel('Average Score',fontsize=12,fontweight='bold')
    plt.xticks( ha='center',fontsize=12)
    plt.tight_layout()
    
    #Save and Show the plot
    plt.savefig('bargraph.png')
    plt.show()
    return


def scatter_plot(df):
    """ 
    Function to create a 3d scatter plot to understand the relation between the scores
    """
    # Create a 3D scatter plot
    fig = plt.figure(figsize=(9,6))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot
    ax.scatter(df['math_score'], df['reading_score'], 
                df['writing_score'], c='blue', marker='o')

    # Set labels and title
    ax.set_xlabel('Math Score',fontsize=12,fontweight='bold')
    ax.set_ylabel('Reading Score',fontsize=12,fontweight='bold')
    ax.set_zlabel('Writing Score',labelpad=-1,fontsize=12,fontweight='bold')
    ax.set_title('3D Scatter Plot of Scores',fontsize=14,fontweight='bold')
    
    #Save and Show the plot
    plt.savefig('Scatter.png')
    plt.show()
    return


def stacked_bar(df):
    """
    Function to display a stacked bar graph to display the number of students
    based on test preparation and results.
    """
        
    # Count number of students who achieved Distinction, Pass, or Fail based on preparation
    result_prep_counts = df.groupby(['test_preparation', 'result']).size().unstack(fill_value=0)

    # Calculate the percentages for each part of the stack
    result_prep_percentages = result_prep_counts.div(result_prep_counts.sum(axis=1), axis=0) * 100

    # Plotting a stacked bar with percentages
    plt.figure(figsize=(8, 5))

    # Create the stacked bar plot
    ax = result_prep_percentages.plot(kind='bar', stacked=True)

    # Add annotations
    for bars in ax.containers:
        ax.bar_label(bars, fmt='%.2f%%', label_type='center')
    # Calculate the total counts for test preparation
    totals = result_prep_counts.sum(axis=1)
    
    total_text ='No of Students:\n' + '\n'.join([f'{idx}: {val}' 
                                        for idx, val in totals.items()])

    
    plt.annotate(total_text, xy=(1.04, 0.40), 
                 xycoords='axes fraction', fontsize=11,
                 bbox=dict(boxstyle="round", facecolor='ivory',
                           alpha=0.8), horizontalalignment='left')
    #set titles, labels and legend
    plt.title('Student Results Based on Test Preparation', fontsize=14, fontweight='bold')
    plt.xlabel('Test Preparation', fontsize=12, fontweight='bold')
    plt.ylabel('Percentage of Students', fontsize=12, fontweight='bold')
    plt.legend(title='Result',bbox_to_anchor=(1.04, 1), loc='upper left')
    plt.xticks(rotation=0, ha='center', fontsize=12)
    
    #Save and Show the plot
    plt.savefig('Stackedbar.png')
    plt.show()
    return


def heatmap(df):
    """
    Function to display correlation between the scores
    """
    #display correlations of the data in heat map 
    plt.figure(figsize=(10, 8))
    mask = np.triu(np.ones_like(df.corr()))
    sns.heatmap(df.corr(), annot=True, cmap='viridis', fmt=".2f"
                ,mask=mask, linewidths=.5)
    # Set title and adjust font properties
    plt.title("Correlation between the scores",fontsize=12,fontweight='bold')

    # Make annotations bold
    for text in plt.gca().texts:
        text.set_fontweight('bold')
    #set ticks sizes and ticks   
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tick_params(axis='both', which='major', pad=10)
    #Save and Show the plot
    plt.savefig('Heatmap.png')
    plt.show()
    return


def histogram(df):
    """
    Defining a function to create a histogram 
    to understand the probability of scores
    """
    
    # Set up color palette suitable 
    color_palette = ["#0072B2", "#D55E00", "#009E73"]  

    # Create a 1x3 subplot structure, each representing a histogram for scores
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

    # List of subjects and their corresponding colors
    subjects = [('math_score', color_palette[0],'Maths Score'), 
            ('reading_score', color_palette[1],'Reading Score'), 
            ('writing_score', color_palette[2],'Writing Score')]

    # Plot histograms with KDE for each subject
    for ax, (subject, color, title) in zip(axes, subjects):
        sns.histplot(df[subject], kde=True, color=color, ax=ax, 
                 bins=20, line_kws={'linewidth': 2})
        ax.set_title(title+' Distribution', fontsize=12, fontweight='bold')
        ax.set_xlabel('Scores', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')

    #plt.grid(axis='y')
    #plt.legend()
    # Save the plot as histogram.png
    plt.savefig('histogram.png')
    # Show the plot
    plt.show()
    return

#url to download data
url = 'https://github.com/pratapponnam/DHV-Assignment/blob/main/study_performance.csv?raw=True'

#download data from url
df = download_data(url)

df = process_data(df)

#Using describe function for mean, stanadrd deviation, min and max value.
print('Stats of the data', end='\n')
print(df.describe())

#Display the table
print(df)


#plot the histrogram
histogram(df)

#display pie chart
pie_chart(df)

#display the bargraph
bar_chart(df)

#display stacked bar graph
stacked_bar(df)

#display the scatter plot
scatter_plot(df)


#df to have only numeric columns
numeric_df = df.select_dtypes(include=['number'])

#basic statistics of the data

print('Skewness of the data', end='\n')
print(numeric_df.skew() , end='\n\n')

print('Kurtosis of the data', end='\n')
print(numeric_df.kurtosis() , end='\n\n')

print('Correlation of the data', end='\n')
print(numeric_df.corr() , end='\n\n')

#display correlated Heatmap
heatmap(numeric_df)




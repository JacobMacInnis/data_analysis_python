import pandas as pd
from rich.console import Console
from rich.table import Table

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", 100)        # Prevent line breaks
pd.set_option("display.colheader_justify", "center")  # Center-align headers

console = Console()

def print_rich_table(df):
    table = Table(show_header=True, header_style="bold magenta")
    
    # Add columns
    for col in df.columns:
        table.add_column(col, justify="center")
    
    # Add rows
    for _, row in df.head().iterrows():
        table.add_row(*map(str, row.values))
    
    console.print(table)



def calculate_demographic_data(print_data=True):
    # Read data from file

    df = pd.read_csv('adult.data.csv')
    df.columns = df.columns.str.strip()
    
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(),1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((df['education'].value_counts()['Bachelors'] / df['education'].value_counts().sum()) * 100, 1)
    # print('percentage_bachelors', percentage_bachelors)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    # print(df.head())
    print_rich_table(df)
    higher_education = df[df['education'].isin(['Bachelors','Masters','Doctorate'])]
    lower_education = df[~df['education'].isin(['Bachelors','Masters','Doctorate'])]

    # percentage with salary >50K
    higher_education_rich = round(higher_education[higher_education['salary'] == '>50K'].shape[0] /higher_education.shape[0] * 100,1)
    lower_education_rich = round(lower_education[lower_education['salary'] == '>50K'].shape[0] /lower_education.shape[0] * 100,1)
    
    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_work_workers_df = df[df["hours-per-week"] == min_work_hours]
    num_min_workers = min_work_workers_df.shape[0]
    
    rich_percentage = min_work_workers_df[min_work_workers_df['salary'] == '>50K'].shape[0] / num_min_workers * 100

    print(df['native-country'].unique())

    high_salary_df = df[df['salary'] == '>50K']
    all_salaries_df = df.groupby('native-country').size().reset_index(name='total-salaries')
    good_salaries_df = high_salary_df.groupby('native-country').size().reset_index(name='good-salaries')

    merged_df = good_salaries_df.merge(all_salaries_df, on="native-country", how="left")
    
    merged_df['rich-percentage'] = round((merged_df['good-salaries'] / merged_df['total-salaries']) * 100,1)
    
    # What country has the highest percentage of people that earn >50K?
    highest_earning_country = merged_df.loc[merged_df['rich-percentage'].idxmax()]['native-country']
    highest_earning_country_percentage = merged_df.loc[merged_df['rich-percentage'].idxmax()]['rich-percentage']

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df["native-country"] == "India") & (df["salary"] == ">50K")]["occupation"].mode()[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

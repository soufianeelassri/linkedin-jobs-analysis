# Importing necessary libraries
import pandas as pd
import numpy as np
import re

### Data Preprocessing

# Load the dataset
df = pd.read_csv('../dataset/raw/jobsData-fr.csv')

# Display the first few rows of the dataset
df.head()

## Summary of the dataset

# Show the shape of the DataFrame
print(f"Data shape: {df.shape}")

# Display information about columns, including data types and non-null counts
df.info()

## Handling Unnecessary Columns

# Drop the first column, as it appears unnecessary
df.drop(df.columns[0], axis=1, inplace=True)

# Identify and count null values in "Unnamed" columns
unnamed_columns = df.columns[df.columns.str.contains('Unnamed')]
df[unnamed_columns].isnull().sum()

# Drop "Unnamed" columns to clean the dataset
df.drop(unnamed_columns, axis=1, inplace=True)

# Drop other unnecessary columns that are not needed for analysis
columns_to_drop = [
    'applyType', 'applyUrl', 'benefits', 'companyId', 'companyUrl',
    'id', 'jobUrl', 'postedTime', 'posterFullName', 'posterProfileUrl', 'workType'
]
df.drop(columns=columns_to_drop, inplace=True)

## Handling Missing Data

# Display the count of missing values in relevant columns
print(df.isnull().sum())

# Drop rows where critical columns have missing values
df.dropna(subset=['companyName', 'experienceLevel', 'location', 'sector', 'title'], inplace=True)

## Jobs titles and Salary Normalization and Conversion

# Function to categorize job titles
def categorize_title(title):
    if 'data analyst' in title.lower():
        return 'Data Analyst'
    elif 'data scientist' in title.lower():
        return 'Data Scientist'
    elif 'data engineer' in title.lower():
        return 'Data Engineer'
    elif 'cybersécurité' in title.lower():
        return 'Cybersecurity Engineer'
    else:
        return 'Other'

# Apply categorization function
df['job_category'] = df['title'].apply(categorize_title)

# Remove rows categorized as 'Other'
df = df[df['job_category'] != 'Other']

# Rename 'job_category' column for better readability
df.rename(columns={'job_category': 'job_title'}, inplace=True)

# Function to extract and convert salary values
def extract_salary(salary_str):
    if pd.isna(salary_str) or salary_str == 'nan':
        return np.nan
    
    # Regular expressions to capture salary values
    match = re.findall(r"€([\d,]+\.?\d*)", salary_str)
    
    if not match:
        return np.nan

    # Convert matched values to floats
    values = [float(s.replace(",", "")) for s in match]

    # Check if it's a monthly or yearly salary
    if "/mo" in salary_str:
        # Convert monthly to yearly
        values = [v * 12 for v in values]

    # Return the average if it's a range, otherwise the single value
    return np.mean(values) if len(values) > 1 else values[0]

# Apply the salary extraction function
df['numeric_salary'] = df['salary'].apply(extract_salary)

# Fill missing salaries with the median salary for each job category
df['salary'] = df.groupby('job_title')['numeric_salary'].transform(lambda x: x.fillna(x.median()))

# Drop temporary 'numeric_salary' column
df.drop(columns=['numeric_salary'], inplace=True)

## Extracting City Names from Location

# Extract city names from the 'location' column
df['location'] = df['location'].str.split(',', n=1).str[0].str.split(' ', n=1).str[0]

# Set default country as France for all jobs
df['country'] = 'France'

## Data Cleaning and Date Parsing

# Function to validate date strings
def is_valid_date(date_str):
    # Regular expression to match common date formats
    date_regex = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(\d{4}[/-]\d{1,2}[/-]\d{1,2})'
    return bool(re.match(date_regex, date_str))

# Apply function to check for valid date strings
df['valid_date'] = df['publishedAt'].apply(is_valid_date)

# Convert valid date strings to datetime format
df['publishedAt'] = pd.to_datetime(df['publishedAt'].where(df['valid_date']))

# Remove helper column
df.drop(columns=['valid_date'], inplace=True)

# Extract day, month, and year from the 'publishedAt' column
df['day'] = df['publishedAt'].dt.day
df['month'] = df['publishedAt'].dt.month
df['year'] = df['publishedAt'].dt.year

# Display the cleaned DataFrame
df.head()

# Save cleaned data to a new CSV
df.to_csv('../dataset/processed/jobsData-fr.csv', index=False)
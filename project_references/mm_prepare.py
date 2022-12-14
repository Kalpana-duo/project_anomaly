# .py file dependencies
import os
import pandas as pd
import numpy as np

from skimpy import clean_columns

import env_mm
from env_mm import user, password, host, get_connection


'''Function to retrieve Codeup Curriculum Logs and cache as .csv file'''
def get_logs_dataset():

    # creating the operating system filename for referencing
    filename = "curriculum_logs.csv"
    if os.path.isfile(filename):
        
        df = pd.read_csv(filename)

        # let's print the shape
        print(f'df shape: {df.shape}')

        return df

    else: 

        # creating the corriculum logs url for to retrieve from MySQL
        url = f'mysql+pymysql://{env_mm.user}:{env_mm.password}@{env_mm.host}/curriculum_logs'

        # creating the MySQL query
        query = '''
                SELECT 
                date, 
                time,
                path as endpoint,
                user_id,
                cohort_id,
                ip,
                name,
                slack,
                start_date,
                end_date,
                program_id,
                FROM curriculum_logs.logs
                LEFT JOIN curriculum_logs.cohorts ON curriculum_logs.logs.cohort_id = curriculum_logs.cohorts.id;
                '''

        # creating the df
        df = pd.read_sql(query, url)

        # cache the df to local repository 
        df.to_csv("curriculum_logs.csv", index = False)

        return df


'''function that takes in the dataframe and sets the date & time as
timestamp. function also creates new day & month columns'''
def clean_dates(df):

    # combining date and time & dropping previous columns
    df["datetime"] = df["date"] + " " + df["time"]
    df = df.drop(columns = ["date", "time"])

    # converting datetime column to proper pd.datetime 
    df["datetime"] = pd.to_datetime(df["datetime"])

    # setting the date column to index
    df = df.set_index("datetime").sort_index()
    
    # creating a day column 
    df["day"] = df.index.strftime("%A")

    # creating a month column 
    df["month"] = df.index.strftime("%B")

    # printing the new dataframe shape
    print(f'new df shape: {df.shape}')

    # return the dataframe
    return df


'''function that returns the endpoint class and topic'''
def get_endpoint_targets(df):

    topics = df["endpoint"].str.split("/", n = 2, expand = True).rename(columns = {0: "class", 1: "topic"})
    topics = topics.drop(columns = 2)
    
    # combining the two(2) dataframes
    new_df = pd.concat([df, topics], axis = 1)

    # printing the new dataframe shape
    print(f'df shape: {new_df.shape}')

    # returns the new df w/endpoint class and topics
    return new_df

def clean_anomalies(df):

    # setting the program_id to object type
    df[["user_id", "program_id"]] = df[["user_id", "program_id"]].astype(object)

    # drop single missing values in endpoint and class (same record)
    df = df.dropna(subset = "endpoint")

    # cleaning columns with empty class or nulls
    df = df.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('', None)


# Codeup program_id to program type map:
# 1 = "full-stack PHP program"
# 2 = "full-stack JAVA program"
# 3 = "Data Science"
# 4 = "Front-end Program"

'''function to label ea. observation with
the Codeup program associated to the program_id'''
def map_program_id(df):

    df["program_type"] = df["program_id"].map(
        {1: "FS_PHP_program", 
        2: "FS_JAVA_program", 
        3: "DS_program", 
        4: "Front_End_program", 
        np.nan: None})

    # drop redundant column 
    df = df.drop(columns = "program_id")

    # returning the dataframe
    return df

'''function to loop through discrete variables and prints variable, 
data type, number of unique observations, unique observations, and 
frequency of unique observations sorted (value_counts)'''
def print_variable_info(df):
    with pd.option_context("display.max_rows", None):
        for col in df.columns:
            if df[col].dtype != "number":
                print(f'feature: {col}')
                print(f'feature type: {df[col].dtype}')
                print(f'number of unique values: {df[col].nunique()}')
                print(f'unique values: {df[col].unique()}')
                print(f'value counts: {df[col].value_counts().sort_index(ascending = True).sort_values(ascending = False)}')


'''functiont to create a dataframe that captures the highest frequency value per column'''
def print_frequency_df(df):
    # container to hold metrics from for loop
    container = []

    for col in df.columns:

        metric = {  
            "feature": col,
            "data_type": df[col].dtype,
            "unique_values": df[col].nunique(),
            "most_freq_observation": df[col].value_counts().idxmax(),
            "total_observations": df[col].value_counts().max()
        }

        container.append(metric)

    freq_df = pd.DataFrame(container).sort_values("total_observations", ascending = False)

    return freq_df


'''function to deal with parsing one entry in our log data'''
def parse_log_entry(entry):
    parts = entry.split()
    output = {}
    output['ip'] = parts[0]
    output['timestamp'] = parts[3][1:].replace(':', ' ', 1)
    output['request_method'] = parts[5][1:]
    output['request_path'] = parts[6]
    output['http_version'] = parts[7][:-1]
    output['status_code'] = parts[8]
    output['size'] = int(parts[9])
    output['user_agent'] = ' '.join(parts[11:]).replace('"', '')
    return pd.Series(output)


'''function that cleans specific "lesson" column values'''
def clean_lesson(df):
    
    # Data Science program cleas clean up
    df['class'] = np.where((df['class'] == 'fundamentals') & (df.program_type == 'DS_program'), 'ds-fundamentals', df['class'])
    df['class'] = np.where((df['class'] == '1-fundamentals') & (df.program_type == 'DS_program'), 'ds-fundamentals', df['class'])
    df['class'] = np.where((df['class'] == 'storytelling') & (df.program_type == 'DS_program'), 'ds-storytelling', df['class'])
    df['class'] = np.where((df['class'] == '2-storytelling') & (df.program_type == 'DS_program'), 'ds-storytelling', df['class'])
    df['class'] = np.where((df['class'] == 'sql') & (df.program_type == 'DS_program'), 'ds-sql', df['class'])
    df['class'] = np.where((df['class'] == '3-sql') & (df.program_type == 'DS_program'), 'ds-sql', df['class'])
    df['class'] = np.where((df['class'] == 'python') & (df.program_type == 'DS_program'), 'ds-python', df['class'])
    df['class'] = np.where((df['class'] == '4-python') & (df.program_type == 'DS_program'), 'ds-python', df['class'])
    df['class'] = np.where((df['class'] == 'stats') & (df.program_type == 'DS_program'), 'ds-stats', df['class'])
    df['class'] = np.where((df['class'] == '5-stats') & (df.program_type == 'DS_program'), 'ds-stats', df['class'])
    df['class'] = np.where((df['class'] == '6-regression') & (df.program_type == 'DS_program'), 'ds-regression', df['class'])
    df['class'] = np.where((df['class'] == 'regression') & (df.program_type == 'DS_program'), 'ds-regression', df['class'])
    df['class'] = np.where((df['class'] == 'classification') & (df.program_type == 'DS_program'), 'ds-classification', df['class'])
    df['class'] = np.where((df['class'] == '7-classification') & (df.program_type == 'DS_program'), 'ds-classification', df['class'])
    df['class'] = np.where((df['class'] == 'clustering') & (df.program_type == 'DS_program'), 'ds-clustering', df['class'])
    df['class'] = np.where((df['class'] == '8-clustering') & (df.program_type == 'DS_program'), 'ds-clustering', df['class'])
    df['class'] = np.where((df['class'] == 'timeseries') & (df.program_type == 'DS_program'), 'ds-timeseries', df['class'])
    df['class'] = np.where((df['class'] == '9-timeseries') & (df.program_type == 'DS_program'), 'ds-timeseries', df['class'])
    df['class'] = np.where((df['class'] == 'anomaly-detection') & (df.program_type == 'DS_program'), 'ds-anomaly-detection', df['class'])
    df['class'] = np.where((df['class'] == '10-anomaly-detection') & (df.program_type == 'DS_program'), 'ds-anomaly-detection', df['class'])
    df['class'] = np.where((df['class'] == 'nlp') & (df.program_type == 'DS_program'), 'ds-nlp', df['class'])
    df['class'] = np.where((df['class'] == '11-nlp') & (df.program_type == 'DS_program'), 'ds-nlp', df['class'])
    df['class'] = np.where((df['class'] == 'distributed-ml') & (df.program_type == 'DS_program'), 'ds-distributed-ml', df['class'])
    df['class'] = np.where((df['class'] == '12-distributed-ml') & (df.program_type == 'DS_program'), 'ds-distributed-ml', df['class'])
    df['class'] = np.where((df['class'] == 'advanced-topics') & (df.program_type == 'DS_program'), 'ds-advanced-topics', df['class'])
    df['class'] = np.where((df['class'] == '13-advanced-topics') & (df.program_type == 'DS_program'), 'ds-advanced-topics', df['class'])
    df['class'] = np.where((df['class'] == 'appendix') & (df.program_type == 'DS_program'), 'ds-appendix', df['class'])
    
    # the rest class will belong to Full-Stack program
    df['class'] = np.where((df['class'] == '1-fundamentals'), 'fundamentals', df['class'])
    df['class'] = np.where((df['class'] == '10-anomaly-detection'), 'anomaly-detection', df['class'])
    df['class'] = np.where((df['class'] == '6-regression'), 'regression', df['class'])
    df['class'] = np.where((df['class'] == '3-sql'), 'sql', df['class'])
    df['class'] = np.where((df['class'] == '4-python'), 'python', df['class'])
    df['class'] = np.where((df['class'] == '5-stats'), 'stats', df['class'])
    df['class'] = np.where((df['class'] == '7-classification'), 'classification', df['class'])
    df['class'] = np.where((df['class'] == '2-storytelling'), 'storytelling', df['class'])
    df['class'] = np.where((df['class'] == '9-timeseries'), 'timeseries', df['class'])
    df['class'] = np.where((df['class'] == '8-clustering'), 'clustering', df['class'])
    df['class'] = np.where((df['class'] == '11-nlp'), 'nlp', df['class'])
    df['class'] = np.where((df['class'] == '12-distributed-ml'), 'distributed-ml', df['class'])
    df['class'] = np.where((df['class'] == '1._Fundamentals'), 'fundamentals', df['class'])
    df['class'] = np.where((df['class'] == '5-regression'), 'regression', df['class'])
    df['class'] = np.where((df['class'] == '6-classification'), 'classification', df['class'])
    df['class'] = np.where((df['class'] == '9-anomaly-detection'), 'anomaly-detection', df['class'])
    df['class'] = np.where((df['class'] == '3.0-mysql-overview'), 'mysql', df['class'])
    df['class'] = np.where((df['class'] == '13-advanced-topics'), 'advanced-topics', df['class'])
    df['class'] = np.where((df['class'] == '2-stats'), 'stats', df['class'])
    
    return df

'''function that returns a df of unique null feature records'''
def get_fifty_3(df):

    new_df = df.loc[df[[
        "name", 
        "slack", 
        "start_date", 
        "end_date", 
        "program_type"]].isnull().apply(lambda x: all(x), axis=1)]

    return new_df

'''Function that plots the post-grad topic revisits'''
def most_grad_revisits(df):
    # list of programs to plot (exludes null values)
    lst = ['FS_PHP_program', 'FS_JAVA_program', 'Front_End_program', 'DS_program']
    for program in lst:

        if program != "Front_End_program":
            plt.figure(figsize = (8, 4))
            sns.set(font_scale = 1)

            df1 = grad[grad["program_type"] == program]

            df1 = df1.applymap(lambda s: s.capitalize() if type(s) == str else s)

            sns.countplot(
                y = "topic", 
                data = df1,
                order = df1["topic"].value_counts()[0:11].index,
                palette = "crest_r")

            plt.ylabel(None)
            plt.xlabel("Count")
            plt.title(f'Top 10 Revisited Topics Post Graduation: {program}')
            plt.show()


# .py file dependencies

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


'''function that takes in the dataframe and sets the date & time as
timestamp. function also creates new day & month columns'''
def clean_dates(df):

    # combining date and time & dropping previous columns
    df["datetime"] = df["date"] + " " + df["time"]

    # converting datetime column to proper pd.datetime 
    df["datetime"] = pd.to_datetime(df["datetime"])

    # setting the date column to index
    df = df.set_index("datetime").sort_index()
    
    # return the dataframe
    return df


'''function that returns the endpoint class and topic'''
def get_endpoint_targets(df):

    topics = df["endpoint"].str.split("/", n = 2, expand = True).rename(columns = {0: "class", 1: "topic"})
    topics = topics.drop(columns = 2)
    
    # combining the two(2) dataframes
    new_df = pd.concat([df, topics], axis = 1)

    # returns the new df w/endpoint class and topics
    return new_df

def clean_anomalies(df):

    # setting the program_id to object type
    df[["user_id", "program_id"]] = df[["user_id", "program_id"]].astype(object)

    # cleaning columns with empty class or nulls
    df = df.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('', None)

    return df

'''function to handle missing values in log dataset.'''
def missing_values(df):

    # filling in null values with '0' value
    df["topic"] = df["topic"].fillna(0)

    df["class"] = df["class"].fillna(0)

    # dropping single record in 'endpoint' column 
    df = df.dropna(subset=['endpoint'])

    # returning the dataframe
    return df


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

    grad = df.copy()

    # list of programs to plot (exludes null values)
    lst = ['FS_PHP_program', 'FS_JAVA_program', 'Front_End_program', 'DS_program']
    
    for program in lst:

        if program != "Front_End_program":
            plt.figure(figsize = (8, 4))
            sns.set(font_scale = 1)

            df1 = grad[grad["program_type"] == program]

            df1 = df1.applymap(lambda s: s.capitalize() if type(s) == str else s)

            sns.countplot(
                y = "class", 
                data = df1,
                order = df1["class"].value_counts()[0:11].index,
                palette = "crest_r")

            plt.ylabel(None)
            plt.xlabel(None)
            plt.title(f'Top 10 Revisited Lessons Post Graduation: {program}')
            plt.show()

'''function to plot most revisited topics for alumni'''
def most_grad_revisits_topics(df):

    grad = df.copy()

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
            plt.xlabel(None)
            plt.title(f'Top 10 Revisited Topics Post Graduation: {program}')
            plt.show()

'''Function that plots the current topic revisits'''
def most_current_visits(df):

    curr = df.copy()

    # list of programs to plot (exludes null values)
    lst = ['FS_JAVA_program', 'DS_program']
    
    for program in lst:
        
        plt.figure(figsize = (8, 4))
        sns.set(font_scale = 1)

        df1 = curr[curr["program_type"] == program]

        df1 = df1.applymap(lambda s: s.capitalize() if type(s) == str else s)

        sns.countplot(
            y = "class", 
            data = df1,
            order = df1["class"].value_counts()[0:11].index,
            palette = "crest_r")

        plt.ylabel(None)
        plt.xlabel(None)
        plt.title(f'While Enrolled: Top-10 Lessons Visited: {program}')
        plt.show()


def value_counts_and_frequencies(s: pd.Series, dropna=True) -> pd.DataFrame:
    return pd.merge(
        s.value_counts(dropna=True)[0:6].rename('Count'),
        s.value_counts(dropna=True, normalize=True)[0:6].rename('Percentage').round(2),
        left_index=True,
        right_index=True,
    )


'''function that returns the top 30 most frequent classes as a plot'''
def return_most_visited_lessons_all_time(df):
    
    plt.figure(figsize=(14, 10))
    sns.set(font_scale = 1)

    sns.countplot(
        y = "topic", 
        data = df,
        order = df["topic"].value_counts(dropna = True)[0:31].index,
        palette = "crest_r")

    plt.ylabel(None)
    plt.title("Most Explored Codeup Topics: All Time")
    plt.show()
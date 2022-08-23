# .py file dependencies
import os
import pandas as pd
import numpy as np

from skimpy import clean_columns

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
                    SELECT date, 
                    time, 
                    path as endpoint, 
                    user_id, 
                    cohort_id, 
                    ip, 
                    name, 
                    slack, 
                    start_date,
                    end_date, 
                    program_id
                    FROM curriculum_logs.logs
                    LEFT JOIN curriculum_logs.cohorts ON curriculum_logs.logs.cohort_id = curriculum_logs.cohorts.id;
                    '''

        # creating the df
        df = pd.read_sql(query, url)

        # cache the df to local repository 
        df.to_csv("curriculum_logs.csv", index = False)

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
        np.nan: np.nan})

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


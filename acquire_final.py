# .py file dependencies
import os
import pandas as pd
import numpy as np

import env
from env import user, password, host


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
        url = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/curriculum_logs'

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
                program_id
                FROM logs
                LEFT JOIN cohorts ON logs.cohort_id = cohorts.id;
                '''

        # creating the df
        df = pd.read_sql(query, url)

        # cache the df to local repository 
        df.to_csv("curriculum_logs.csv", index = False)

        return df
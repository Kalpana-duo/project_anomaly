import numpy as np
import pandas as pd
import seaborn as sns
import env
import os

def get_logs_dataset():
    # creating the operating system filename for referencing
    filename = 'curriculum_logs.csv'
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        # let’s print the shape
        print(f'df shape: {df.shape}')
        return df
    else:
        # creating the corriculum logs url for to retrieve from MySQL
        url = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/curriculum_logs'
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

def set_timestamp(df):
    
    df['timestamp'] = df['date'] + ' ' + df['time']
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp')
    # col = ['date','time']
    # df.drop(columns=col, inplace = True)
    df['day'] = df.index.strftime('%A')
    df['month'] = df.index.strftime('%B')
    
    return df

def get_endpoint_targets(df):
    topics = df['endpoint']. str.split('/',n = 1,expand = True).rename(columns = {0: 'class', 1: 'topic'})
    new_df = pd.concat([df, topics], axis = 1)
    # returns the new df w/endpoint class and topics
    return new_df

def map_program_id(df):
    
    df['program_type'] = df['program_id'].map(
        {1: 'FS_PHP_program',
        2: 'FS_JAVA_program',
        3: 'DS_program',
        4: 'Front_End_program',
        np.nan: np.nan})
    # returning the dataframe
    return df

def handle_missing(df):
    # fill the topic null with 0 now
    df = df.fillna({'topic':0})
    # drop one row that endpoint is null
    df = df.dropna(subset=['endpoint'])
    
    return df

def clean_lesson(df):
    
    # Data Science program cleas clean up
    df['class'] = np.where((df['class'] == 'fundamentals') & (df.program_type == 'DS_program'), 'ds-fundamentals', df['class'])
    df['class'] = np.where((df['class'] == '1-fundamentals') & (df.program_type == 'DS_program'), 'ds-fundamentals',df['class'])
    df['class'] = np.where((df['class'] == 'storytelling') & (df.program_type == 'DS_program'), 'ds-storytelling', df['class'])
    df['class'] = np.where((df['class'] == '2-storytelling') & (df.program_type == 'DS_program'), 'ds-storytelling',df['class'])
    df['class'] = np.where((df['class'] == 'sql') & (df.program_type == 'DS_program'), 'ds-sql', df['class'])
    df['class'] = np.where((df['class'] == '3-sql') & (df.program_type == 'DS_program'), 'ds-sql', df['class'])
    df['class'] = np.where((df['class'] == 'python') & (df.program_type == 'DS_program'), 'ds-python', df['class'])
    df['class'] = np.where((df['class'] == '4-python') & (df.program_type == 'DS_program'), 'ds-python', df['class'])
    df['class'] = np.where((df['class'] == 'stats') & (df.program_type == 'DS_program'), 'ds-stats', df['class'])
    df['class'] = np.where((df['class'] == '5-stats') & (df.program_type == 'DS_program'), 'ds-stats', df['class'])
    df['class'] = np.where((df['class'] == '6-regression') & (df.program_type == 'DS_program'), 'ds-regression', df['class'])
    df['class'] = np.where((df['class'] == 'regression') & (df.program_type == 'DS_program'), 'ds-regression', df['class'])
    df['class'] = np.where((df['class'] == 'classification') & (df.program_type == 'DS_program'), 
                           'ds-classification',df['class'])
    df['class'] = np.where((df['class'] == '7-classification') & (df.program_type == 'DS_program'), 
                           'ds-classification',df['class'])
    df['class'] = np.where((df['class'] == 'clustering') & (df.program_type == 'DS_program'), 'ds-clustering', df['class'])
    df['class'] = np.where((df['class'] == '8-clustering') & (df.program_type == 'DS_program'), 'ds-clustering', df['class'])
    df['class'] = np.where((df['class'] == 'timeseries') & (df.program_type == 'DS_program'), 'ds-timeseries', df['class'])
    df['class'] = np.where((df['class'] == '9-timeseries') & (df.program_type == 'DS_program'), 'ds-timeseries', df['class'])
    df['class'] = np.where((df['class'] == 'anomaly-detection') & (df.program_type == 'DS_program'), 
                           'ds-anomaly-detection', df['class'])
    df['class'] = np.where((df['class'] == '10-anomaly-detection') & (df.program_type == 'DS_program'), 
                           'ds-anomaly-detection', df['class'])
    df['class'] = np.where((df['class'] == 'nlp') & (df.program_type == 'DS_program'), 'ds-nlp', df['class'])
    df['class'] = np.where((df['class'] == '11-nlp') & (df.program_type == 'DS_program'), 'ds-nlp', df['class'])
    df['class'] = np.where((df['class'] == 'distributed-ml') & (df.program_type == 'DS_program'), 
                           'ds-distributed-ml', df['class'])
    df['class'] = np.where((df['class'] == '12-distributed-ml') & (df.program_type == 'DS_program'), 
                           'ds-distributed-ml', df['class'])
    df['class'] = np.where((df['class'] == 'advanced-topics') & (df.program_type == 'DS_program'), 
                           'ds-advanced-topics', df['class'])
    df['class'] = np.where((df['class'] == '13-advanced-topics') & (df.program_type == 'DS_program'), 
                           'ds-advanced-topics', df['class'])
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


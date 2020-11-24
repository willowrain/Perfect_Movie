import pandas as pd

movie_data = pd.read_csv('compiled_dataframe_1.csv')
for i in range (2,31):
    file_name = 'compiled_dataframe_' +str(i) + '.csv'
    next_df = pd.read_csv(file_name)
    movie_data = pd.concat([movie_data,next_df])

failed_data = pd.read_csv('failed_codes_1.csv')
for i in range (2,31):
    file_name = 'failed_codes_' + str(i) + '.csv'
    next_df = pd.read_csv(file_name)
    failed_data = pd.concat([failed_data,next_df])

movie_data.to_csv(r'movie_data.csv')
failed_data.to_csv(r'failed_data.csv')

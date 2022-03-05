import numpy as np
import pandas as pd
from functools import reduce


def clean_data(df):
    df_min = df.resample('D').min()
    df_max = df.resample('D').max()
    df_avg = df.resample('D').mean()
    df_min = df_min.drop(['Unnamed: 0', 'Unnamed: 0.1',
                          'location_x', 'location_y'], axis=1)
    df_max = df_max.drop(['Unnamed: 0', 'Unnamed: 0.1',
                          'location_x', 'location_y'], axis=1)
    df_avg = df_avg.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)
    df_min.rename(columns={'PM2.5': 'PM2.5 (min)',
                           'PM10': 'PM10 (min)', 'Total': 'Total (min)'}, inplace=True)
    df_max.rename(columns={'PM2.5': 'PM2.5 (max)',
                           'PM10': 'PM10 (max)', 'Total': 'Total (max)'}, inplace=True)
    df_avg.rename(columns={'PM2.5': 'PM2.5 (avg)',
                           'PM10': 'PM10 (avg)', 'Total': 'Total (avg)'}, inplace=True)
    dataframe = [df_min, df_max, df_avg]
    df_merged = reduce(lambda left, right: pd.merge(
        left, right, on=['utc'], how='outer'), dataframe)
    return df_merged


if __name__ == '__main__':
    df = pd.read_csv('data/all.csv', parse_dates=['utc'], index_col=['utc'])

# London
df1 = df[df['location_x'].str.match('London')]
df_1 = clean_data(df1)
df_1.insert(0, 'Location', 'London')
df_1.insert(1, 'Latitude', '51.50853')
df_1.insert(2, 'Longitude', '-0.12574')

# Manchester
df2 = df[df['location_x'].str.match('Manchester')]
df_2 = clean_data(df2)
df_2.insert(0, 'Location', 'Manchester')
df_2.insert(1, 'Latitude', '53.479489')
df_2.insert(2, 'Longitude', '-2.245115')

# Cardiff
df3 = df[df['location_x'].str.match('Cardiff')]
df_3 = clean_data(df3)
df_3.insert(0, 'Location', 'Cardiff')
df_3.insert(1, 'Latitude', '51.481583')
df_3.insert(2, 'Longitude', '-3.17909')

# Edinburgh
df4 = df[df['location_x'].str.match('Edinburgh')]
df_4 = clean_data(df4)
df_4.insert(0, 'Location', 'Edinburgh')
df_4.insert(1, 'Latitude', '55.948612')
df_4.insert(2, 'Longitude', '-3.200833')

frames = [df_1, df_2, df_3, df_4]
df_merge = pd.concat(frames)
df_merge.reset_index(inplace=True)
df['utc'] = pd.to_datetime(df['utc']).dt.date
df['Total (avg)'].replace('', np.nan, inplace=True)
df.dropna(subset=['Total (avg)'], inplace=True)
df.to_csv('data/min-max-avg.csv', index=True, header=True)

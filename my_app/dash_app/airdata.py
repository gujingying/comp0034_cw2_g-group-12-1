from pathlib import Path
import datetime
import pandas as pd


class AirQualityData:
    """
    Class for retrieving and structuring the data.
    """

    def __init__(self):
        self.AirQuality = None
        self.AirQuality = pd.DataFrame()
        self.area_list = []
        self.AirQuality_eng = []
        self.AirQuality_area = []
        self.day_data = []
        self.get_data()

    def get_data(self):
        datafolder = Path('../my_app/dash_app/data')
        csvfile = 'all.csv'
        self.AirQuality= pd.read_csv(datafolder/csvfile)
        self.area_list = self.AirQuality["location_x"].unique().tolist()

    def process_data_for_area(self, area, start_date, end_date):
        self.AirQuality['utc'] = pd.to_datetime(self.AirQuality['utc'])
        mask_1 = (self.AirQuality['utc'] > start_date) & (
                self.AirQuality['utc'] <= end_date) & (self.AirQuality['location_x'] == 'London')
        mask_2 = (self.AirQuality['utc'] > start_date) & (
                self.AirQuality['utc'] <= end_date) & (self.AirQuality['location_x'] == area)

        # Data for London
        self.AirQuality_eng = self.AirQuality.loc[mask_1]

        # Data for the selected area
        self.AirQuality_area = self.AirQuality.loc[mask_2]

    def process_data_for_single_day(self, area, start_date_str):
        start_date = pd.to_datetime(start_date_str)
        end_date = start_date+datetime.timedelta(days=1)
        end_date_str = end_date.strftime('%B %d, %Y')
        mask = (self.AirQuality['utc'] > start_date_str) & (
                self.AirQuality['utc'] <= end_date_str) & (self.AirQuality['location_x'] == area)
        self.day_data = self.AirQuality.loc[mask]

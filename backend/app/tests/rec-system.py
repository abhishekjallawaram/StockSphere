import yfinance as yf
from typing import Optional, Union
import pandas as pd

def get_historical_market_data(ticker: str, start: str, end: str, interval: str, data_type: str) -> Optional[Union[pd.DataFrame, float]]:
    
    yf_ticker = yf.Ticker(ticker)
    if data_type == 'price':
        return yf_ticker.history(start=start, end=end, interval=interval)
    elif data_type in ['plynch', 'eps']:
        print(f"{data_type} data type is not supported yet.")
        return None
    else:
        raise ValueError(f"Unsupported data type '{data_type}'. Available types are 'price', 'plynch', 'eps'.")

import pandas as pd
import requests
import json
from typing import List, Optional, Union

# Constants
_EXCHANGE_LIST = ['nyse', 'nasdaq', 'amex']
_SECTORS_LIST = {'Consumer Non-Durables', 'Capital Goods', 'Health Care', 'Energy', 'Technology', 'Basic Industries', 'Finance', 'Consumer Services', 'Public Utilities', 'Miscellaneous', 'Consumer Durables', 'Transportation'}
_ANALYST_RATINGS_LIST = {'Strong Buy', 'Hold', 'Buy', 'Sell', 'Strong Sell'}
_REGIONS_LIST = {'AFRICA', 'EUROPE', 'ASIA', 'AUSTRALIA AND SOUTH PACIFIC', 'CARIBBEAN', 'SOUTH AMERICA', 'MIDDLE EAST', 'NORTH AMERICA'}
_COUNTRIES_LIST = {'Argentina', 'Armenia', 'Australia', 'Austria', 'Belgium', 'Bermuda', 'Brazil', 'Canada', 'Cayman Islands', 'Chile', 'Colombia', 'Costa Rica', 'Curacao', 'Cyprus', 'Denmark', 'Finland', 'France', 'Germany', 'Greece', 'Guernsey', 'Hong Kong', 'India', 'Indonesia', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Japan', 'Jersey', 'Luxembourg', 'Macau', 'Mexico', 'Monaco', 'Netherlands', 'Norway', 'Panama', 'Peru', 'Philippines', 'Puerto Rico', 'Russia', 'Singapore', 'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Taiwan', 'Turkey', 'United Kingdom', 'United States'}

# NASDAQ header to mimic a browser request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def build_params(exchange: str = 'NYSE', regions: Optional[List[str]] = None, sectors: Optional[List[str]] = None, countries: Optional[List[str]] = None, analyst_ratings: Optional[List[str]] = None) -> dict:
    """
    Construct the parameters for the API request based on the given criteria.
    """
    params = {'exchange': exchange, 'download': 'true', 'tableonly': 'true'}
    if regions:
        if not _REGIONS_LIST.issuperset(regions):
            raise ValueError('Some regions included are invalid')
        params['region'] = '|'.join(regions)
    if sectors:
        if not _SECTORS_LIST.issuperset(sectors):
            raise ValueError('Some sectors included are invalid')
        params['sector'] = '|'.join(sectors)
    if countries:
        if not _COUNTRIES_LIST.issuperset(countries):
            raise ValueError('Some countries included are invalid')
        params['country'] = '|'.join(countries)
    if analyst_ratings:
        if not _ANALYST_RATINGS_LIST.issuperset(analyst_ratings):
            raise ValueError('Some ratings included are invalid')
        params['recommendation'] = '|'.join(analyst_ratings)
    return params

def fetch_stock_data(params: dict) -> pd.DataFrame:
    """
    Fetch stock data from NASDAQ API and return as DataFrame.
    """
    response = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=HEADERS, params=params)
    json_data = json.loads(response.text)
    if not json_data['data']['headers']:
        return pd.DataFrame()
    columns = list(json_data['data']['headers'].keys())
    return pd.DataFrame(json_data['data']['rows'], columns=columns)

def filter_by_market_cap(df: pd.DataFrame, min_cap: Optional[float] = None, max_cap: Optional[float] = None) -> pd.DataFrame:
    """
    Filter the DataFrame by minimum and maximum market capitalization, handling non-numeric values.
    """
    # Convert marketCap to float, using 0.0 for non-convertible values
    df['marketCap'] = pd.to_numeric(df['marketCap'], errors='coerce').fillna(0.0)

    if min_cap is not None:
        df = df[df['marketCap'] > min_cap]
    if max_cap is not None:
        df = df[df['marketCap'] < max_cap]
    return df


def get_tickers_by_filter(exchanges: Optional[List[str]], min_cap: Optional[float] = None, max_cap: Optional[float] = None, **filters) -> List[str]:
    """
    Get tickers filtered by exchanges and other criteria including optional market cap filtering.
    """
    tickers = []
    for exchange in exchanges:
        # Build parameters excluding market cap filters
        params = build_params(exchange=exchange, **filters)
        # Fetch stock data using the parameters
        df = fetch_stock_data(params)
        # Apply market cap filtering if specified
        df = filter_by_market_cap(df, min_cap, max_cap)
        tickers.extend(df['symbol'].tolist())
    return tickers

import yfinance as yf

def get_recommendations(ticker: str, convert_type: str = 'normal'):
    """
    Fetches the stock recommendations from upgrades_downgrades and normalizes them based on a given conversion type.

    Args:
        ticker (str): The stock ticker symbol.
        convert_type (str): The type of conversion to normalize recommendation grades.
                            Options are 'normal', 'simple', 'reduced'.

    Returns:
        DataFrame or None: Normalized recommendations or None if no data is available.
    """
    yf_ticker = yf.Ticker(ticker)
    recommendations = yf_ticker.upgrades_downgrades
    record = yf_ticker.recommendations

    # Print the raw recommendations data
    #print("Raw Recommendations Data:")
    # print(recommendations)
    print(record.info())

    # Check if recommendations DataFrame is not empty and has the expected columns
    if recommendations is not None and 'ToGrade' in recommendations.columns and 'FromGrade' in recommendations.columns:
        # Normalize the recommendations
        recommendations['ToGrade'] = recommendations['ToGrade'].apply(normalize_recommendations, args=(convert_type,))
        recommendations['FromGrade'] = recommendations['FromGrade'].apply(normalize_recommendations, args=(convert_type,))

        print("\nNormalized Recommendations:")
        #print(recommendations.head())
        return recommendations
    else:
        print(f"No valid recommendations data available for {ticker}.")
        return None

def normalize_recommendations(rec: str, convert_type: str = 'normal') -> str:
    """
    Normalizes stock recommendation terms to a smaller set of understood terms based on conversion type.

    Args:
        rec (str): Recommendation term.
        convert_type (str): Conversion type ('normal', 'simple', 'reduced').

    Returns:
        str: Normalized recommendation or 'Invalid' if term cannot be normalized.
    """
    rec = rec.lower().strip()
    mapping = get_mapping(convert_type)

    for grade, terms in mapping.items():
        if rec in terms:
            return grade

    return 'Invalid'

def get_mapping(convert_type: str) -> dict:
    """
    Returns a dictionary of terms mapped to normalized grades based on the conversion type.

    Args:
        convert_type (str): Conversion type ('normal', 'simple', 'reduced').

    Returns:
        dict: Mapping of terms to grades.
    """
    base_mapping = {
        'Strong Sell': ['strong sell', 'focus reduce'],
        'Sell': ['sell', 'overweight', 'negative', 'reduce', 'underperform', 'cautious', 'below average', 'tender', 'underperformer'],
        'Hold': ['hold', 'neutral', 'equal-weight', 'market perform', 'fair', 'mixed', 'average'],
        'Buy': ['buy', 'positive', 'accumulate', 'outperform', 'add', 'above average'],
        'Strong Buy': ['strong buy', 'top pick', 'action list buy']
    }

    if convert_type == 'simple':
        base_mapping['Sell'].extend(base_mapping.pop('Strong Sell'))
        base_mapping['Buy'].extend(base_mapping.pop('Strong Buy'))
    elif convert_type == 'reduced':
        # Exclude specific terms
        for term in ['long-term buy', 'speculative buy', 'speculative sell']:
            for key in base_mapping.keys():
                if term in base_mapping[key]:
                    base_mapping[key].remove(term)

    return base_mapping

# from .get_stock_data import get_historical_market_data
# from .get_recommendations import get_recommendations,get_convert_type_keys
# from .get_tickers import get_tickers_filtered,SectorConstants
# from .custom_scale import CustomScale
import yfinance as yf
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
import matplotlib.ticker
from matplotlib import scale as mscale
import warnings
from tqdm import tqdm

def get_recommendations_performance(tickers,start,end,performance_test_period,early_stop,data_type,convert_type,get_upgrade_downgrade,verbose):


    convert_type_list = get_mapping(convert_type=convert_type)

    df_firm_perf = pd.DataFrame(columns=convert_type_list)
    df_time_total = pd.DataFrame(columns=convert_type_list)

    if verbose:
        print('Total tickers: '+str(len(tickers)))

    for tick in tickers:
        if verbose:
            print("Geting data for ticker: " + tick + "...")

        #get historical data
        data = get_historical_market_data(ticker = tick,start=start,end=end,interval='1d',data_type=data_type)
        data['Date'] = data.index

        # make sure no nan or inf values exists, replace nan values will most recent value unless value is first is dataframe then replace with next value
        data = data.replace(np.inf, np.nan)
        data = data.fillna(method='ffill')
        data = data.fillna(method='bfill')

        #no data
        if len(data.index) == 0:
            continue

        #get recommendations
        recommendations_df = get_recommendations(ticker=tick,convert_type=convert_type)
        #no recommendations for stock
        if recommendations_df is None:
            continue
        recommendations_df['Date'] = recommendations_df.index

        #get list of firms
        yf_firms_set = set(recommendations_df['Firm'].values)
        firm_list = list(yf_firms_set)

        #add firms not already in datafram
        for firm in firm_list:
            if firm not in df_firm_perf.index:
                new_firm_perf = pd.Series(name=firm, data=[np.nan]*len(convert_type_list), index=convert_type_list)
                new_time_total = pd.Series(name=firm, data=[np.nan]*len(convert_type_list), index=convert_type_list)
                df_firm_perf = pd.concat([df_firm_perf, new_firm_perf.to_frame().T], ignore_index=False)
                df_time_total = pd.concat([df_time_total, new_time_total.to_frame().T], ignore_index=False)

        results = []

        if early_stop:

            #create dictionary which groups all firms recommendations together
            yf_recommendations_dict = {}
            for yf_firm in firm_list:
                yf_recommendations_dict[yf_firm] = recommendations_df.loc[recommendations_df['Firm'] == yf_firm]


            for firm in yf_recommendations_dict.keys():
                firm_recommendations = yf_recommendations_dict[firm]

                # track last grade and date
                last_date_val = 0
                last_to_grade_val = 0

                last2_date_val = 0
                last2_to_grade_val = 0
                wait_once = True
                for date_val, to_grade_val in zip(firm_recommendations['Date'],firm_recommendations['ToGrade']):

                    if wait_once:
                        last_date_val = date_val
                        last_to_grade_val = to_grade_val
                        wait_once = False
                        continue
                    else:

                        result = calculate_performance(data=data,performance_test_period=performance_test_period,date=last_date_val, next_date=date_val, firm=firm, to_grade=last_to_grade_val)

                        if get_upgrade_downgrade:
                            if result is not None:
                                if last2_to_grade_val != last_to_grade_val and last2_to_grade_val != 0 and last_to_grade_val != 'Invalid' and last_to_grade_val != 'Dont Include' and last2_to_grade_val != 'Invalid' and last2_to_grade_val != 'Dont Include':
                                    new_result = result.copy()
                                    new_result[2] = last2_to_grade_val + '->' + last_to_grade_val
                                    results.append(new_result)

                        last2_date_val = last_date_val
                        last2_to_grade_val = last_to_grade_val
                        last_date_val = date_val
                        last_to_grade_val = to_grade_val
                        results.append(result)

                result = calculate_performance(data=data,performance_test_period=performance_test_period,date=last_date_val, next_date=None, firm=firm, to_grade=last_to_grade_val)

                if get_upgrade_downgrade:
                    if result is not None:
                        if last2_to_grade_val != last_to_grade_val and last2_to_grade_val != 0 and last_to_grade_val != 'Invalid' and last_to_grade_val != 'Dont Include' and last2_to_grade_val != 'Invalid' and last2_to_grade_val != 'Dont Include':
                            new_result = result.copy()
                            new_result[2] = last2_to_grade_val + '->' + last_to_grade_val
                            results.append(new_result)

                results.append(result)
        else:
            if get_upgrade_downgrade:
                #create dictionary which groups all firms recommendations together
                yf_recommendations_dict = {}
                for yf_firm in firm_list:
                    yf_recommendations_dict[yf_firm] = recommendations_df.loc[recommendations_df['Firm'] == yf_firm]


                for firm in yf_recommendations_dict.keys():
                    firm_recommendations = yf_recommendations_dict[firm]


                    for date_val, to_grade_val, last_to_grade_val in zip(firm_recommendations['Date'],firm_recommendations['ToGrade'],firm_recommendations['From Grade']):

                        result = calculate_performance(data=data,performance_test_period=performance_test_period,date=date_val, next_date=None, firm=firm, to_grade=to_grade_val)

                        if get_upgrade_downgrade:
                            if result != None:
                                if to_grade_val != last_to_grade_val and last_to_grade_val != 'Invalid' and last_to_grade_val != 'Dont Include' and to_grade_val != 'Invalid' and to_grade_val != 'Dont Include':
                                    new_result = result.copy()
                                    new_result[2] = last_to_grade_val + '->' + to_grade_val
                                    results.append(new_result)

                        results.append(result)

            else:
                results = [calculate_performance(data=data,performance_test_period=performance_test_period,date=date_val, next_date=None, firm=firm_val, to_grade=to_grade_val) for date_val, firm_val, to_grade_val in zip(recommendations_df['Date'], recommendations_df['Firm'],recommendations_df['To Grade'])]

        for result in results:
            if result != None:
                performance = result[0]
                firm = result[1]
                grade = result[2]
                time_dif = result[3]

                if grade != 'Invalid' and grade != 'Dont Include':
                    if get_upgrade_downgrade:
                        if grade not in df_firm_perf.columns:
                            df_firm_perf[grade] = 0.0
                            df_time_total[grade] = 0.0

                    if not isinstance(df_firm_perf.at[firm,grade],np.ndarray):
                        df_firm_perf.at[firm,grade] = np.array([performance])
                        df_time_total.at[firm,grade] = np.array([time_dif])
                    else:
                        temp_val_1 = df_firm_perf.at[firm,grade]
                        temp_val_2 = df_time_total.at[firm,grade]
                        df_firm_perf.at[firm,grade] = np.append(temp_val_1,performance)
                        df_time_total.at[firm,grade] = np.append(temp_val_2,time_dif)
    
    df_firm_perf.to_csv("df_firm_perf.csv")
    df_time_total.to_csv("df_time_total.csv")

    return df_firm_perf,df_time_total


def calculate_performance(data, performance_test_period, date, next_date, firm, to_grade):


    start_date = date.replace(tzinfo=None)
    end_date = (date + relativedelta(months=+performance_test_period)).replace(tzinfo=None)

    if next_date is not None:
        next_date = next_date.replace(tzinfo=None)
        if next_date < end_date:
            end_date = next_date

    # Ensure data['Date'] is tz-naive for comparison
    data['Date'] = pd.to_datetime(data['Date']).dt.tz_localize(None)

    # Check if there's data to examine
    if data.empty:
        return None
    if start_date < data['Date'].iloc[0] or end_date > data['Date'].iloc[-1]:
        return None

    # Calculate the differences in times
    data['dif_start_date'] = abs(data['Date'] - start_date)
    data['dif_end_date'] = abs(data['Date'] - end_date)

    start_index = data['dif_start_date'].idxmin()
    end_index = data['dif_end_date'].idxmin()

    start_value = data.loc[start_index, 'Close']
    end_value = data.loc[end_index, 'Close']

    performance = (end_value - start_value) / start_value
    time_dif_sec = (end_date - start_date).total_seconds()
    return [performance, firm, to_grade, time_dif_sec]

def measure_firm_performance(tickers=[], start='2022-01-01', end='2023-01-01', data_type='price', 
                             performance_test_period=24, early_stop=True, metric='geometric mean', convert_type='simple',
                             min_recommendations=21, save=None, get_upgrade_downgrade=False, verbose=False):
    convert_keys = get_mapping(convert_type=convert_type)

    if metric == 'mean' and early_stop:
        warnings.warn('Calculating average rate of return over variable period lengths will yield bad results')
    if isinstance(min_recommendations, dict):
        if (convert_type == 'normal' and len(min_recommendations) != 5) or \
           (convert_type == 'reduced' and len(min_recommendations) != 5) or \
           (convert_type == 'simple' and len(min_recommendations) != 3):
            raise ValueError(f"{convert_type} recommendation conversion needs a dictionary with {len(convert_keys)} integer values")
        if set(min_recommendations.keys()) != set(convert_keys):
            raise ValueError('Invalid value for some min_recommendation key')
    if metric not in ['mean', 'geometric mean']:
        raise ValueError('Invalid metric')
    if not isinstance(performance_test_period, int) or performance_test_period <= 0:
        raise ValueError('Invalid performance_test_period')

    df_firm_perf, df_time_total = get_recommendations_performance(tickers=tickers, start=start, end=end, 
                                                                  performance_test_period=performance_test_period, 
                                                                  early_stop=early_stop, data_type=data_type, convert_type=convert_type, 
                                                                  get_upgrade_downgrade=get_upgrade_downgrade, verbose=verbose)

    df_new_firm_perf = df_firm_perf.copy()
    to_drop = []

    for firm_name, firm_perf in tqdm(df_firm_perf.iterrows(), total=df_firm_perf.shape[0], desc="Processing firms"):
        total_recommendations = len(firm_perf)

        for rec in convert_keys:
            if rec in firm_perf and isinstance(firm_perf[rec], np.ndarray) and firm_perf[rec] is not None:
                perf_array = firm_perf[rec]
                if metric == 'mean':
                    annual_returns = np.power(perf_array + 1.0, 12.0 / performance_test_period) - 1.0
                    df_new_firm_perf.at[firm_name, rec] = annual_returns.mean()
                elif metric == 'geometric mean':
                    log_returns = np.log(perf_array + 1.0)
                    time_weights = df_time_total.at[firm_name, rec] / df_time_total.at[firm_name, rec].sum()
                    weighted_average_log = (log_returns * time_weights).sum()
                    geometric_avg_return = np.exp(weighted_average_log) - 1.0
                    df_new_firm_perf.at[firm_name, rec] = geometric_avg_return

    df_new_firm_perf.drop(to_drop, inplace=True)

    if save:
        df_new_firm_perf.to_csv(save)

    return df_new_firm_perf


if __name__ == '__main__':

    #Tests

    tickers_simple = get_tickers_by_filter(exchanges=['NYSE', 'NASDAQ'],min_cap=5e11, max_cap=2e12)
    measure_firm_performance(tickers=tickers_simple, start='2012-01-01', end='2020-01-01', performance_test_period=12, early_stop=True, 
                             data_type='price', metric='geometric mean', min_recommendations={'Sell': 20, 'Hold': 20, 'Buy': 20}, 
                             convert_type='simple', save='Test1.csv', get_upgrade_downgrade=False, verbose=True)




#to load data from json files, extract desired fields and save to CSV

import numpy as np
import pandas as pd
import json

def load_json_data(fn: str) -> dict:
    """Load json file from directory"""
    with open(fn) as f:
        data = json.load(f)
        if 'assets' in data:
            return data['assets'].pop()
        else:
            return data['asset_events']


def get_max_sale(sales: dict) -> dict:
    """Return the sale metadata which had the highest USD transaction value"""
    greatest_sale: dict
    greatest_sale_price = -1
    for sale in sales.values():
        sale_price = sale['total_price'] / 10**sale['decimals']
        usd_value = sale_price * sale['usd_price']
        if usd_value > greatest_sale_price:
            greatest_sale = sale
            greatest_sale_price = usd_value
    return greatest_sale



def create_formatted_dict(traits: dict, events: dict) -> dict:
    """Transform dictionary format"""
    sales = {}
    d = {}
    for i, event in enumerate(events):
        # gather only data relating to the most recent sale of the nft
        sales[f'sale_{i+1}'] = {'total_price': float(event['total_price']),
                                'decimals': float(event['payment_token']['decimals']),
                                'token_name': event['payment_token']['name'],
                                'usd_price': float(event['payment_token']['usd_price']),
                                'num_sales': len(events),
                                'created_date': event['created_date']}

    if not sales:
        d['LastSalePrice'] = 'NaN'
    else:
        sale = get_max_sale(sales)
        d['LastSalePrice'] = sale['total_price'] / 10**sale['decimals']
        d['LastSaleToken'] = sale['token_name']
        d['NumberOfSales'] = sale['num_sales']
        d['USDPrice'] = d['LastSalePrice'] * sale['usd_price']
        d['SaleDate'] = sale['created_date']

    for trait in traits:
        d[trait['trait_type']] = trait['value']
        d[trait['trait_type']+'Rarity'] = trait['trait_count']/10000
    return d

def create_pandas_df(n: int) -> pd.DataFrame:
    df = pd.DataFrame()
    for i in range(n):
        fn1 = f'asset_data/asset_data_{i}.json'
        fn2 = f'events_data/events_data_{i}.json'
        asset_raw_data = load_json_data(fn=fn1)
        events_raw_data = load_json_data(fn=fn2)
        asset_formatted_data = create_formatted_dict(
            asset_raw_data['traits'], events=events_raw_data
            )

        df = df.append(asset_formatted_data, ignore_index=True)
    return df

df = create_pandas_df(10000)
# df_filtered = df.loc[df['LastSalePrice'] != 'NaN']  # data that has a sale
df = df.reset_index(level=0)

df.to_csv('bored_apes.csv', index=False)
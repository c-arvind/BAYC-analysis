import os
import requests

# rate throttle wait time
FIFTEEN_MINUTES = 900
# store your OpenSea API key in a .env file or export it in your shell
api_key = os.environ.get("API_KEY")

def call_api(url, params):
    """Retrieve asset data"""
    headers = {"X-API-KEY": api_key}
    response = requests.get(url=url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response


def create_asset_params(token_id: str) -> dict:
    """Create query parameters for assets request"""
    return {
        "token_ids": token_id,
        "asset_contract_address": "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",
        "order_direction": "desc",
        "offset": 0,
        "limit": 1,
        "collection": "boredapeyachtclub",
    }


def write_to_json_file(fn: str, data: str) -> None:
    with open(fn, 'wb') as f:
        f.write(data)


def process_many(token_ids: list, files: list, base_url: str) -> None:
    for id in token_ids:
        fn = f'asset_data/asset_data_{id}.json'
        if not fn in files:
            resp = call_api(base_url, params=create_asset_params(token_id=id))
            data = resp.content
            write_to_json_file(fn=fn, data=data)
            print(f'Processed {fn}!')
    print("Done")


assets_url = "https://api.opensea.io/api/v1/assets"
files = [f'asset_data/{f}' for f in os.listdir('./asset_data')]
token_ids = [f'{i}' for i in range(730, 10001)]
process_many(token_ids=token_ids, files=files, base_url=assets_url)



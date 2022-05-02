import json
import os
from get_assets import call_api, write_to_json_file

def create_event_params(token_id: str) -> dict:
    #Create query parameters for assets request
    return {
        "token_id": token_id,
        "asset_contract_address": "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",
        "offset": 0,
        "limit": 100,
        "event_type": "successful"
    }


def process_many(token_ids: list, files: list, base_url: str) -> None:
    for id in token_ids:
        fn = f'events_data/events_data_{id}.json'
        if not fn in files:
            resp = call_api(base_url, params=create_event_params(token_id=id))
            data = resp.content
            write_to_json_file(fn=fn, data=data)
            print(f'Processed {fn}!')
    print("Done")

events_url = "https://api.opensea.io/api/v1/events"
files = [f'events_data/{f}' for f in os.listdir('./events_data')]
token_ids = [f'{i}' for i in range(0, 10001)]
process_many(token_ids=token_ids, files=files, base_url=events_url)


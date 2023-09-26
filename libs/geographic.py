import requests
import json

EXCLUDE_ADDRESS = ['localhost', '127.0.0.1', '0.0.0.0']
API_ENDPOINT = 'http://ip-api.com/json'


def get_position_by_ip_address(address: str, exclude: list[str] = []) -> str:
    '''
    https://ip-api.com/docs/api:json
    '''
    if address in EXCLUDE_ADDRESS + exclude:
        return ''

    try:
        response = requests.request('get', f'{API_ENDPOINT}/{address}')
        result: dict = json.loads(response.content)
    except:
        return ''

    if result.get('status') == 'success':
        return f'''{result.get('country')}/{result.get('regionName')}/{result.get('city')}'''
    else:
        return ''

'''
Module to pull keys from test geckoboard widgets.
'''
import os
import json

def get_keys():
    settings_folder = os.path.dirname(__file__)
    settings_file = os.path.join(settings_folder,'gecko_settings.json')

    with open(settings_file, 'r') as file:
        json_data = json.load(file)
        return json_data

if __name__ == '__main__':
    print(get_keys())
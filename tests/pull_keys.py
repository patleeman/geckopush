import os
import json

def get_keys():
    settings_folder = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    __file__
                )
            )
        ),"geckoboard_push_settings"
    )

    settings_file = os.path.join(settings_folder,'gecko_settings.json')

    with open(settings_file, 'r') as file:
        json_data = json.load(file)
        return json_data

if __name__ == '__main__':
    print(get_keys())
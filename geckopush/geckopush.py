import urllib.request
import json

class Dashboard(object):
    " Dashboard Object.  Used to house account API Key only."
    def __init__(self, api_key):
        self.api_key = api_key


    def __repr__(self):
        return "<DASHBOARD OBJECT, API KEY: {api_key}>".format(
            api_key=self.api_key)


class Widget(object):
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.api_key = dashboard.api_key
        self.widget_key = None
        self.payload = {
            "api_key": self.api_key,
            "data": {
                "item": [

                ]
            }
        }

    def _assemble_payload(self, _item_module):
        self.payload["data"]["item"].append(_item_module)

    def _assemble_item(self):
        pass

    def push(self):
        self._assemble_item()
        _api_endpoint = 'https://push.geckoboard.com/v1/send/'\
                        '{widget_key}'.format(widget_key=self.widget_key)
        _payload_json = json.dumps(self.payload).encode('utf-8')
        _request = urllib.request.Request(url=_api_endpoint,
                                          data=_payload_json
                                          )
        _request.add_header('Content-Type', 'application/json')
        _response = urllib.request.urlopen(_request)
        _api_status = _response.read()
        print(_api_status)
        # Todo: add error handling for non 200 codes to _response


class BarChart(Widget):
    def __init__(self, widget_key, data, *args, **kwargs):
        super(BarChart, self).__init__(*args, **kwargs)
        self.widget_key = widget_key
        self.data = data
        self.x_axis_labels = None
        self.x_axis_type = None
        self.y_axis_format = None
        self.y_axis_unit = None

    def _assemble_item(self):
        _item = {
            "x_axis": {},
            "y_axis": {},
            "series": [
                {
                    "data": self.data
                }
            ]
        }

        if self.x_axis_labels is not None:
            _item["x_axis"]["labels"] = self.x_axis_labels

        if self.x_axis_type is not None:
            _item["x_axis"]["type"] = self.x_axis_type

        if self.y_axis_format is not None:
            _item["y_axis"]["format"] = self.y_axis_format

        if self.y_axis_unit is not None:
            _item["y_axis"]["unit"] = self.y_axis_unit

        self._assemble_payload(_item)

